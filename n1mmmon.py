###############################################################################
# n1mmmon.py
# Author: Tom Kerr AB3GY
#
# Python class for monitoring N1MM+ external UDP contact broadcasts.
# See # See https://n1mmwp.hamdocs.com/appendices/external-udp-broadcasts/
#
# Designed for personal use by the author, but available to anyone under the
# license terms below.
###############################################################################

###############################################################################
# License
# Copyright (c) 2025 Tom Kerr AB3GY (ab3gy@arrl.net).
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

# System level packages.
import getopt
import os
import socket
import sys

# Local packages.
import _env_init
from adif import adif
from xmlnode import xmlnode
from strutils import unformat_date, unformat_time


##############################################################################
# Global objects and data.
##############################################################################


##############################################################################
# Functions.
##############################################################################
def convert_band(n1mm_band):
    """
    Convert an N1MM+ band string to an ADIF compatible band string.
    """
    adif_band = ''
    if (n1mm_band == '1.8'):
        adif_band = '160m'
    elif (n1mm_band == '3.5'):
        adif_band = '80m'
    elif (n1mm_band == '7'):
        adif_band = '40m'
    elif (n1mm_band == '10'):
        adif_band = '30m'
    elif (n1mm_band == '14'):
        adif_band = '20m'
    elif (n1mm_band == '18'):
        adif_band = '17m'
    elif (n1mm_band == '21'):
        adif_band = '15m'    
    elif (n1mm_band == '24'):
        adif_band = '12m'
    elif (n1mm_band == '28'):
        adif_band = '10m'
    elif (n1mm_band == '50'):
        adif_band = '6m'
    elif (n1mm_band == '144'):
        adif_band = '2m'
    elif (n1mm_band == '420'):
        adif_band = '70cm'
    return adif_band


###############################################################################
# n1mmmon class.
###############################################################################
class n1mmmon (object):
    """
    N1MM+ external UDP contact broadcast monitoring class.
    Listens on a UDP port as a server and parses N1MM+ contacts as they arrive.
    """

    # ------------------------------------------------------------------------
    def __init__(self, verbose=False):
        """
        Class constructor.
        
        Parameters
        ----------
        verbose : bool
            Prints verbose debug messages if True.
        
        Returns
        -------
        None
        """
        
        # Variable initialization.
        self.__version__ = '0.1'  # Version per PEP 396
        self.class_name  = str(type(self).__name__)
        self.ipAddr  = ''
        self.ipPort  = 0
        self.dstAddr = ''
        self.verbose = verbose        
        self.message = ''
        self.timeout = 10
        
        # Initialize the UDP socket.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # ------------------------------------------------------------------------
    def __del__(self):
        """
        Class destructor.
        Closes the UDP port.
        """ 
        self.socket.close()

    # ------------------------------------------------------------------------
    def getxml(self, node, xml_in):
        """
        Get a text string from an XML node.
        
        Parameters
        ----------
        node : str
            The node name to search for in the xml string.
        xml_in : str
            The XML contact string broadcast by N1MM+ to search.
        
        Returns
        -------
        (status, text) : tuple
            status : bool
                True if a nonempty text field found in the specified node
            text : str
                The XML node text if successful.
        """
        status = False
        text = ''
        myXml = xmlnode()
        found = myXml.parse(node, xml_in)
        if found:
            text = myXml.node_text()
            if (len(text) > 0):
                status = True
        return (status, text)

    # ------------------------------------------------------------------------
    def xml2adif(self, xml_in):
        """
        Convert an XML contact string to an adif record.
        
        Parameters
        ----------
        xml_in : str
            The XML contact string broadcast by N1MM+
        
        Returns
        -------
        (status, adif) : tuple
            status : bool
                True if conversion successful, False otherwise.
            adif : str
                A properly formatted ADIF record if successful, undefined otherwise.
        """
        status = False
        myAdif = adif()
        
        # Get minimum QSO information.
        (call_found, text) = self.getxml('call', xml_in)
        if call_found: myAdif.set_field('CALL', text)
        (band_found, text) = self.getxml('band', xml_in)
        if band_found:
            band = convert_band(text)
            if (len(band) > 0):
                myAdif.set_field('BAND', band)
            else:
                band_found = False
        (mode_found, text) = self.getxml('mode', xml_in)
        if mode_found: myAdif.set_field('MODE', text)
        (timestamp_found, text) = self.getxml('timestamp', xml_in)
        if timestamp_found:
            qso_date = unformat_date(text[0:10])
            qso_time = unformat_time(text[11:])
            myAdif.set_field('QSO_DATE', qso_date)
            myAdif.set_field('TIME_ON', qso_time)
        
        # Get additional QSO information.
        (found, text) = self.getxml('txfreq', xml_in)
        if found:
            freq_mhz = float(text)/100000.
            myAdif.set_field('FREQ', '{:0.6f}'.format(freq_mhz))
        (found, text) = self.getxml('rxfreq', xml_in)
        if found:
            freq_mhz = float(text)/100000.
            myAdif.set_field('FREQ_RX', '{:0.6f}'.format(freq_mhz))
        (found, text) = self.getxml('rcv', xml_in)
        if found:
            myAdif.set_field('RST_RCVD', text)
        (found, text) = self.getxml('snt', xml_in)
        if found:
            myAdif.set_field('RST_SENT', text)
        (found, text) = self.getxml('gridsquare', xml_in)
        if found:
            myAdif.set_field('GRIDSQUARE', text)
        (found, text) = self.getxml('mycall', xml_in)
        if found:
            myAdif.set_field('OPERATOR', text)
        (found, text) = self.getxml('stationprefix', xml_in)
        if found:
            myAdif.set_field('STATION_CALLSIGN', text)
        (found, text) = self.getxml('comment', xml_in)
        if found:
            myAdif.set_field('COMMENT', text)
        
        status = call_found and band_found and mode_found and timestamp_found
        return (status, myAdif.get_adif())


    # ------------------------------------------------------------------------
    def bind(self, ip_addr, ip_port, timeout=10):
        """
        Bind the UDP socket to the specified IP address and port.
        
        Parameters
        ----------
        ip_addr : str
            The local IP address to monitor.  
            N1MM+ must be configured to send packets to this address.
        ip_port : int
            The local port number to monitor.
            N1MM+ must be configured to send packets to this port.
        timeout : int
            The socket listen timeout in seconds.
        
        Returns
        -------
        (status, err_msg) : tuple
            status : bool
                True if bind was successful, False otherwise.
            err_msg : str
                Error message if bind was unsuccessful.
        """
        status = False
        err_msg = ''
        
        # We are the server and listen on our IP address.
        # N1MM+ must be configured to send packets to our address.
        self.ipAddr  = str(ip_addr)
        self.ipPort  = int(ip_port)
        self.timeout = int(timeout)
        
        # Close existing socket.
        # Ignore errors.
        try:
            self.socket.close()
        except Exception as err:
            pass
        
        # Initialize the UDP socket and bind to the IP address and port.
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.settimeout(self.timeout)
            self.socket.bind((self.ipAddr, self.ipPort))
            status = True
        except Exception as err:
            err_msg = str(err)
            
        return (status, err_msg)

    # ------------------------------------------------------------------------    
    def get_message(self):
        """
        Get the next N1MM+ contact message from the UDP port.
        Blocks until message received, socket timeout, or socket error.
        Message is available in the self.message variable.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        status : bool
            True if successful, False otherwise.
            Returns True on a timeout and False if a socket error occurs.
        """
        ok = False
        self.message = ''
        try:
            data, self.dstAddr = self.socket.recvfrom(4096) # buffer size is 4096 bytes
            utf8_data = data.decode('utf-8')
            #print(utf8_data)
            (status, self.message) = self.xml2adif(utf8_data)
            ok = status
        except socket.timeout as err:
            self.message = 'timeout'
            ok = True
        except Exception as err:
            self.message = str(err)
        return ok


###############################################################################
# Main program.
# Monitor the UDP port and print messages.
###############################################################################

if __name__ == "__main__":

    udp_ip   = "127.0.0.1"
    udp_port = 12060
    timeout  = 16
    verbose  = False

    # Get command line options and arguments.
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], "a:p:t:v")
    except (getopt.GetoptError) as err:
        print(str(err))
        sys.exit(1)

    for (o, a) in opts:
        if (o == "-a"):
            udp_ip = a
        elif (o == "-p"):
            udp_port = int(a, 10)
        elif (o == "-t"):
            timeout = int(a, 10)
        elif (o == "-v"):
            verbose = True

    monitor = n1mmmon(verbose)
    (status, err_msg) = monitor.bind(udp_ip, udp_port, timeout)
    if not status:
        print('n1mmmon bind error: ' + err_msg)
        sys.exit(1)

    # Loop forever.
    # Can also use CTRL-C to interrupt and exit.
    ok = True
    print ('Monitoring {}:{}'.format(udp_ip, udp_port))
    while ok:
        ok = monitor.get_message()
        print(monitor.message)

# End of file.
    