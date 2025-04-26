###############################################################################
# qrzlookup.py
# Author: Tom Kerr AB3GY
#
# Class to perform QRZ.com XML database callsign lookups.
# Use of this class requires at least a QRZ.com XML logbook data subscription.
#
# QRZ.COM website: https://www.qrz.com/
# QRZ XML Interface Specification: https://www.qrz.com/XML/current_spec.html
#
# Designed for personal use by the author, but available to anyone under the
# license terms below.
###############################################################################

###############################################################################
# License
# Copyright (c) 2020 Tom Kerr AB3GY (ab3gy@arrl.net).
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,   
# this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,  
# this list of conditions and the following disclaimer in the documentation 
# and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without 
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
###############################################################################
import os
import re
import sys
import traceback

##############################################################################
# Runtime environment checks.
##############################################################################
basename  = os.path.basename(sys.argv[0])
major_ver = sys.version_info[0]
minor_ver = sys.version_info[1]
micro_ver = sys.version_info[2]

# Check for proper Python version.
if (major_ver < 3):
    print('Python version: ' + str(major_ver) + '.' + str(minor_ver) + '.' + str(micro_ver))
    print(basename + ' error: Python major version must be 3.x.x or greater.')
    sys.exit(1)
    
# These packages require Python 3 or greater.
import urllib.request
import urllib.error

# Additional local packages.
import xmlnode


##############################################################################
# Functions.
##############################################################################


##############################################################################
# qrzlookup class.
##############################################################################
class qrzlookup(object):
    """
    A class used to perform QRZ.COM XML database callsign lookups.
    Use of this class requires a QRZ.com XML logbook data subscription.
    This class also requires Python 3.x.x or greater.
    
    General usage:
    1. Call set_credentials() to set the username/password for the query session.
    2. Call start_session() to establish a session key.
    3. Call lookup_callsign() to perform a lookup of a specific callsign.
    4. Call call_data() to return a dictionary of the callsign information.
    5. Repeat steps 3 and 4 as needed.
    6. Call get_error() and get_message() to retrieve the QRZ error and
       message strings from steps 1 and 2.
    """
    
    # ------------------------------------------------------------------------
    def __init__(self, verbose=False):
        """
        Class constructor.
        """
        # Variable initialization.
        self.__version__ = str("0.1")  # Version per PEP 396
        
        self.Verbose  = verbose  # Verbose printing flag
        
        self._qrzUser   = ""  # QRZ database username
        self._qrzPass   = ""  # QRZ database password
        self._qrzKey    = ""  # QRZ database session key
        self._qrzAgent = ""  # Optional agent string (client program name and version)
        self._qrzError = ""  # Error text returned by QRZ
        self._qrzMsg   = ""  # Message text returned by QRZ
        self._qrzSub   = ""  # QRZ subscription expiration info
        
        self._status   = 0   # HTML request status
        self._body     = ""  # HTML response body
        self._info     = ""  # HTML request/response info
        self._reqUrl   = ""  # HTML request URL
        self._rspUri   = ""  # HTML response URL, used to detect redirection
        self._timeout  = 5   # HTML request timeout in seconds

        self._BASEURL  = 'http://xmldata.qrz.com/xml/current/'
        self._INVKEY   = 'Invalid session key'
        self._INVUSER  = 'Username/password incorrect'
        self._NONSUB   = 'non-subscriber'
        
        self._calldata = {}  # Dictionary of callsign data
        
        self._xml = xmlnode.xmlnode()  # XML node used for QRZ parsing        
        
    ###########################################################################
    # Class methods intended to be private.
    ###########################################################################
    
    # ------------------------------------------------------------------------    
    def _print_msg(self, msg):
        """
        Print a formatted message.  Used internally for verbose printing.

        Parameters
        ----------
        msg : str
            The message text to print.
        
        Returns
        -------
        None
        """
        cl = type(self).__name__                         # This class name
        fn = str(traceback.extract_stack(None, 2)[0][2]) # Calling function name
        print(cl + '.' + fn + ': ' + msg)
        
    # ------------------------------------------------------------------------    
    def _http_request(self, uri):
        """
        Perform an HTTP request.

        Parameters
        ----------
        uri : str
            The HTTP request URI.
        
        Returns
        -------
        bool : True if request completed successfully, False otherwise.
        """
        ok = False
        self._body = ""
        self._rspUri = uri
        try:
            resp = urllib.request.urlopen(uri, timeout=self._timeout)   # Returns a HTTPResponse object
            self._status = resp.status
            self._info   = resp.info()
            self._rspUri = resp.geturl() # Look for redirection
            self._body   = resp.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            self._status = e.code
            self._info   = e.reason
        except urllib.error.URLError as e:
            self._status = e.errno
            self._info   = str(e.reason) # This could be text or another exception object
        except Exception as e:
            self._status = -1
            self._info   = str(e)
            
        if (self._status == 200): ok = True
        return ok 
        
    # ------------------------------------------------------------------------    
    def _parse_callsign(self, content):
        """
        Parse the callsign information from the XML data returned by QRZ.

        Parameters
        ----------
        content : str
            The XML data returned by QRZ.  This is expected to contain the
            <QRZDatabase> and <Callsign> nodes.
        
        Returns
        -------
        bool : True if parsing completed successfully, False otherwise.
        """
        ok = True
        self._calldata = {}  # Clear the callsign data
        if (self._xml.parse('QRZDatabase', content)):
            if (self._xml.parse('Callsign', self._xml.node_text())):
                callData = self._xml.node_text()
                
                # Get callsign data.
                elementList = self._xml.element_names(callData)
                
                # Populate the dictionary of the callsign information.
                for e in elementList:
                    if self._xml.parse(e, callData):
                        self._calldata[e] = self._xml.node_text()
                    else:
                        if self.Verbose: self._print_msg('Error parsing ' + e)
            else: 
                self._qrzError = 'QRZ Callsign node not found'
                ok = False
        else: 
            self._qrzError = 'QRZ QRZDatabase node not found'
            
        return ok
    
    # ------------------------------------------------------------------------    
    def _parse_session(self, content):
        """
        Parse the session information from the XML data returned by QRZ.

        Parameters
        ----------
        content : str
            The XML data returned by QRZ.  This is expected to contain the
            <QRZDatabase> and <Session> nodes.
        
        Returns
        -------
        bool : True if parsing completed successfully, False otherwise.
        """
        ok = True
        self._qrzError = ''
        self._qrzMsg   = ''
        self._qrzSub   = ''
        if (self._xml.parse('QRZDatabase', content)):
            if (self._xml.parse('Session', self._xml.node_text())):
                session = self._xml.node_text()
                
                # Get session data.
                if (self._xml.parse('Key', session)):
                    self._qrzKey = self._xml.node_text().strip()
                if (self._xml.parse('Message', session)):
                    self._qrzMsg = self._xml.node_text().strip()
                if (self._xml.parse('SubExp', session)):
                    self._qrzSub = self._xml.node_text().strip()
                if (self._xml.parse('Error', session)):
                    self._qrzError = self._xml.node_text().strip()
                    ok = False
            else: 
                self._qrzError = 'QRZ Session node not found'
                ok = False
        else: 
            self._qrzError = 'QRZ QRZDatabase node not found'
            ok = False
            
        return ok
        
    # ------------------------------------------------------------------------ 
    def _qrz_lookup(self, call):
        """
        Lookup a callsign in the QRZ database and parse the information.
        
        Prerequisites
        -------------
        1. Need a valid QRZ session key in order to perform the lookup. This
           is obtained through a call to _qrz_start_session() or a previous 
           successful call to _qrz_lookup()

        Parameters
        ----------
        call : str
            The callsign to lookup.
        
        Returns
        -------
        bool : True if lookup and parsing completed successfully, False otherwise.
        """
        ok = False
        
        # Need a session key to perform lookup.
        if len(self._qrzKey) == 0:
            self._qrzError = self._INVKEY
            return False
        
        uri = self._BASEURL + '?s=' + self._qrzKey + '&callsign=' + call
        ok = self._http_request(uri)
        if ok:
            if self.Verbose: self._print_msg('HTTP success')
            
            # HTTP request successful, get session info.
            ok = self._parse_session(self._body)
            if len(self._qrzMsg) > 0:
                if self.Verbose: self._print_msg('Msg: ' + self._qrzMsg)
            if not ok:
                # QRZ session error.
                if self.Verbose: self._print_msg('Error: ' + self._qrzError)
                return ok
                
            # Got session info, get callsign info.
            ok = self._parse_callsign(self._body)
            if not ok:
                # QRZ callsign lookup error.
                if self.Verbose: self._print_msg('Error: ' + self._qrzError)
                
        return ok
        
    
        
    ###########################################################################
    # Class methods intended to be public.
    ###########################################################################
    
    def call_data(self):
        """
        Return the dictionary of callsign data.
        """
        return self._calldata
        
    # ------------------------------------------------------------------------     
    def get_error(self):
        """
        Return the QRZ error string.
        """
        return self._qrzError
        
    # ------------------------------------------------------------------------     
    def get_field(self, field):
        """
        Return the field data if found, or an empty string if not found.
        """
        value = ''
        if field in self._calldata.keys():
            value = self._calldata[field]
        return value
        
    # ------------------------------------------------------------------------     
    def get_file(self, filename):
        """
        Load QRZ credentials from the specified XML file.
        
        Parameters
        ----------
        filename : str
            The XML filename to load.  The file must contain <User> and <Pass>
            nodes, and may optionally contain a <Key> node.
        
        Returns
        -------
        bool : True if credentials loaded successfully, False otherwise.
        """
        ok        = False
        xml_found = False
        xml_data  = ''
        xml_node  = xmlnode.xmlnode()
        
        # Open the XML file and get the data.
        try:
            f_xml = open(filename, 'r')
            for line in f_xml:
                if xml_found:
                    xml_data += str(line).strip()
                    # Look for end of XML data.
                    if '</QRZLookup>' in line:
                        xml_found = False
                        break
                else:
                    # Look for start of XML data.
                    if '<QRZLookup>' in line:
                        xml_data += str(line).strip()
                        xml_found = True
            f_xml.close()
        
        except Exception as e:
            self._qrzError = str(e)
            return ok
            
        # Process the session data.
        if (xml_node.parse('QRZLookup', xml_data)):
            if (xml_node.parse('Session', xml_node.node_text())):
                session = xml_node.node_text()
                if (xml_node.parse('User', session)):
                    self._qrzUser = xml_node.node_text()
                if (xml_node.parse('Pass', session)):
                    self._qrzPass = xml_node.node_text()
                if (xml_node.parse('SessKey', session)):
                    self._qrzKey = xml_node.node_text()
                ok = True
            else:
                self._qrzError = 'Session node not found'
        else:
            self._qrzError = 'QRZLookup node not found'

        return ok
        
    # ------------------------------------------------------------------------     
    def get_message(self):
        """
        Return the QRZ message string.
        """
        return self._qrzMsg
        
    # ------------------------------------------------------------------------ 
    def lookup_callsign(self, call):
        """
        Lookup the callsign in the QRZ database.
        
        If the lookup is successful, then use call_data() to retrieve the
        callsign data.
        
        Prerequisites
        -------------
        1. Need a valid QRZ session key in order to perform a complete lookup.
           Call set_credentials() prior to calling this method to set the
           username and password.  You can also optionally call start_session()
           to explicitly establish a session key.  If a session key does not exist
           or is not valid, then this method will call start_session().

        Parameters
        ----------
        call : str
            The callsign to lookup.
        
        Returns
        -------
        bool : True if a QRZ lookup succeeded, False otherwise.
        """
        trace = False # Used for debugging
        
        # Step 1. Check for a session key; start a new session if empty
        if trace: 
            if self.Verbose: print('1')
        if len(self._qrzKey) == 0:
            if trace: 
                if self.Verbose: print('1A')
            ok = self.start_session()
            if not ok:
                if self.Verbose: self._print_msg('Failed to start session')
                return False
        
        # Step 2. Check again for a session key.
        if trace:
            if self.Verbose: print('2')
        if len(self._qrzKey) == 0:
            if self.Verbose: self._print_msg('No session key')
            return False
            
        # Step 3. Have session key, attempt lookup.
        if trace:
            if self.Verbose: print('3')
        ok = self._qrz_lookup(call)
        if ok:
            return True
        else:
            if (self._qrzError == self._INVKEY):
            
                # Step 4. Session key is invalid; attempt to start a new session.
                if trace:
                    if self.Verbose: print('4')
                ok = self.start_session()
                if not ok:
                    if self.Verbose: self._print_msg('Failed to start session')
                    return False
            else:
                # Some other error occurred.
                return False
            
                
        # Step 5. Check again for a session key.
        if trace:
            if self.Verbose: print('5')
        if len(self._qrzKey) == 0:
            if self.Verbose: self._print_msg('No session key')
            return False
            
        # Step 6. Final lookup attempt.
        if trace:
            if self.Verbose: print('6')
        ok = self._qrz_lookup(call)
        
        return ok

    # ------------------------------------------------------------------------ 
    def set_credentials(self, username, password, *, key="", agent=""):
        """
        Set the QRZ database credentials for a query session.

        Parameters
        ----------
        username : str
            The QRZ database username.
        password : str
            The QRZ database password.
        agent : str
            Optional QRZ database agent string. This is typically the client
            program name and version used by QRZ for debugging purposes.
        
        Returns
        -------
        None
        """
        self._qrzUser  = str(username)
        self._qrzPass  = str(password)
        self._qrzAgent = str(agent)
        
    # ------------------------------------------------------------------------ 
    def start_session(self):
        """
        Start a QRZ database query session.  A valid session with a session
        key is needed to perform QRZ database queries.
        
        Prerequisites
        -------------
        1. Need a valid QRZ username and password in order to start a session.
           Call set_credentials() prior to calling this method to set the
           username and password.

        Parameters
        ----------
        None
        
        Returns
        -------
        bool : True if a QRZ session was established successfully, False otherwise.
        """
        ok = False
        
        # Need a username and password.
        if len(self._qrzUser) == 0:
            self._qrzError = 'QRZ username not set'
            if self.Verbose: self._print_msg(self._qrzError)
            return False
        if len(self._qrzPass) == 0:
            self._qrzError = 'QRZ password not set'
            if self.Verbose: self._print_msg(self._qrzError)
            return False
        
        # Request a new session.
        uri = self._BASEURL + '?username=' + self._qrzUser + '&password=' + self._qrzPass
        if len(self._qrzAgent) > 0:
            uri += '&agent=' + self._qrzAgent  
        ok = self._http_request(uri)
        
        if ok:
            if self.Verbose: self._print_msg('HTTP success')
            
            # HTTP request successful, get session info.
            ok = self._parse_session(self._body)
            if len(self._qrzMsg) > 0:
                if self.Verbose: self._print_msg('Msg: ' + self._qrzMsg)
            if not ok:
                # QRZ session error.
                if self.Verbose: self._print_msg('Error: ' + self._qrzError)
        else:
            # HTTP request failed.
            if self.Verbose:
                err = 'Error = ' + str(self._status) + ' ' + self._info
                self._print_msg(err)
                
        return ok

        
###########################################################################
# Main program example test script.
########################################################################### 
if __name__ == "__main__":

    if len(sys.argv) < 4:
        print('Usage: ' + basename + ' username password call')
        sys.exit(1)
    
    myQrz = qrzlookup(True)
    myQrz.set_credentials(sys.argv[1], sys.argv[2])
    
    #myQrz._qrzKey = '2331uf894c4bd29f3923f3bacf02c532d7bd9'
    ok = myQrz.lookup_callsign(sys.argv[3])
    
    msg = myQrz.get_message()
    if len(msg) > 0:
        print('\nMsg: ' + msg)

    if (ok):
        data = myQrz.call_data()
        print()
        for e in data:
            print(e + ': ' + data[e])
        print()
        print(myQrz._body)
    else:
        print('Error: ' + myQrz.get_error())
    
    sys.exit(0) 
    