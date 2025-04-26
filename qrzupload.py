###############################################################################
# qrzupload.py
# Author: Tom Kerr AB3GY
#
# Class to perform QRZ.com ADIF QSO upload.
# Use of this class requires a a QRZ.com logbook data subscription.
#
# QRZ.COM website: https://www.qrz.com/
# QRZ Logbook API Developer Guide: https://www.qrz.com/docs/logbook/QRZLogbookAPI.html
# QRZ XML Interface Specification: https://www.qrz.com/XML/current_spec.html
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
import os
import sys

import urllib.request
import urllib.parse
import urllib.error
import ssl


##############################################################################
# Global objects and data.
##############################################################################
qrz_upload_url = r'https://logbook.qrz.com/api'
scriptname = os.path.basename(sys.argv[0])


##############################################################################
# Functions.
##############################################################################


###############################################################################
# qrzupload class.
###############################################################################
class qrzupload (object):
    """
    Class to perform QRZ.COM ADIF QSO upload.
    Use of this class requires a a QRZ.com logbook data subscription.
    """

    # ------------------------------------------------------------------------
    def __init__(self, call, qrz_key, verbose=False):
        """
        Class constructor.
        
        Parameters
        ----------
        call : str
            Call sign of the QRZ.com logbook owner.
        qrz_key : str
            QRZ.com logbook key.
        verbose : bool
            Print verbose debug messages if True.
        
        Returns
        -------
        None
        """
        global qrz_upload_url
        global scriptname
        
        self.call = call
        self.qrz_key = qrz_key
        self.verbose = verbose
        self.__version__ = '1.0.0'
        
        # Do not authenticate the SSL certificate, otherwise the urllib request will fail.
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # Create a Request object.
        # QRZ requires applications to provide an identifiable user agent header.
        # See https://www.qrz.com/docs/logbook/QRZLogbookAPI.html
        self.req = urllib.request.Request(qrz_upload_url)
        self.req.add_header('User-Agent', '{}/{} ({})'.format(scriptname, self.__version__, self.call))
    
    # ------------------------------------------------------------------------
    def upload(self, adif_qso):
        """
        Upload a single ADIF QSO record to a QRZ.com logbook.
        
        Parameters
        ----------
        adif_qso : str
            A complete and correctly formatted ADIF QSO record.

        Returns
        -------
        (upload_count, status, info) : tuple
          upload_count : int
            Count of successful uploads (0 or 1)
          status : int
            Upload HTTP status code, 200 = success (OK)
          info : str
            Upload response informational string (could be empty)
        """
        # Create an HTML POST form for uploading to QRZ.com.
        form_args = {
            'KEY' : self.qrz_key, 
            'ACTION' : 'INSERT',
            'ADIF' : str(adif_qso),
        }
        query_string = urllib.parse.urlencode(form_args)    
        post_data = query_string.encode('ascii')
        
        # Attempt to upload to QRZ.com.
        status = 0
        info = ''
        reply = ''
        reply_body = ''
        upload_count = 0
        try:
            resp = urllib.request.urlopen(
                self.req, 
                data=post_data, 
                timeout=10)
            status = resp.status
            reply = resp.read().decode('utf-8').strip()
            if self.verbose:
                print('****** URL:\n{}\n******'.format(resp.geturl()))
                print('****** INFO:\n{}\n******'.format(resp.info()))
                print('****** REPLY:\n{}\n******'.format(reply))
        except urllib.error.HTTPError as e:
            status = e.code
            info   = 'Exception: HTTPError: {}'.format(str(e.reason))
            if self.verbose:
                print(info)
        except urllib.error.URLError as e:
            status = e.errno
            reason = str(e.reason) # This could be text or another exception object
            info   = 'Exception: URLError: {}'.format(reason)
            if self.verbose:
                print(info)
        except Exception as e:
            status = -1
            info   = 'Exception: Other: {}'.format(str(e))
            if self.verbose:
                print(info)
        
        if (status == 200):
            # Parse the reply as URL encoded POST data.
            # Example: COUNT=1&LOGID=785458361&RESULT=OK
            reply_data = {}
            reply_list = reply.split('&')
            for r in reply_list:
                s = r.split('=')
                reply_data[s[0]] = str(s[1])
            
            # Check for failures.
            qrz_result = ''
            if 'STATUS' in reply_data.keys():
                qrz_result = reply_data['STATUS']
                if (qrz_result == 'FAIL'):
                    info = 'Upload failed: {}'.format(reply_data['REASON'])
                    if (reply_data['EXTENDED'] != ''): 
                        info += '\n{}'.format(reply_data['EXTENDED'])
                elif (qrz_result == 'OK') or (qrz_result == 'REPLACE'):
                    upload_count = 1
            elif 'RESULT' in reply_data.keys():
                qrz_result = reply_data['RESULT']
                if (qrz_result == 'FAIL'):
                    info = 'Upload failed: {}'.format(reply_data['REASON'])
                    if (reply_data['EXTENDED'] != ''): 
                        info += '\n{}'.format(reply_data['EXTENDED'])
                elif (qrz_result == 'OK') or (qrz_result == 'REPLACE'):
                    upload_count = 1
            else:
                info = 'QRZ insert result not found in reply'
            
            # Check if QSO was overwritten
            if (qrz_result == 'REPLACE'):
                if (len(info) > 0):
                    info += '\n'
                info += 'QSO {} replaced'.format(reply_data['LOGID'])
        else:
            if (status == None): 
                status = -999
                if (info == ''):
                    info = 'URL request error'
        return (upload_count, status, info)


###############################################################################
# Main program.
# Perform a QRZ.com upload from an ADIF file.
###############################################################################

if __name__ == "__main__":

    import getopt
    
    import _env_init
    from adif import adif
    from adif_iter import adif_iter
    from strutils import format_date, format_time
    
    qrz_call = ''
    qrz_key = ''
    verbose = False
    qso_count = 0
    upload_count = 0
    error_count = 0
    warning_count = 0

    # Get command line options and arguments.
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], "c:k:v")
    except (getopt.GetoptError) as err:
        print(str(err))
        sys.exit(1)

    for (o, a) in opts:
        if (o == "-c"):
            qrz_call = str(a).upper()
        elif (o == "-k"):
            qrz_key = str(a)
        elif (o == "-v"):
            verbose = True
    
    if (len(args) < 1):
        print('No ADIF file specified.')
        print('Syntax: {} [-v] -c <call> -k <key> <ADIF-file>'.format(scriptname))
        sys.exit(1)
    if (len(qrz_call) == 0):
        print('No QRZ.com logbook callsign specified.')
        print('Syntax: {} [-v] -c <call> -k <key> <ADIF-file>'.format(scriptname))
        sys.exit(1)
    if (len(qrz_key) == 0):
        print('No QRZ.com logbook key specified.')
        print('Syntax: {} [-v] -c <call> -k <key> <ADIF-file>'.format(scriptname))
        sys.exit(1)
    
    adif_filename = args[0]
    myQrz = qrzupload(qrz_call, qrz_key, verbose)
    
    # Iterate through all QSOs in the ADIF file.
    adif_file = adif_iter(adif_filename)
    for qso in adif_file.all_qsos():
        qso_count += 1
        myAdif = adif(qso)
        qso_summary = \
            myAdif.get_field('CALL') + ' ' + \
            myAdif.get_field('BAND') + ' ' + \
            myAdif.get_field('MODE') + ' ' + \
            format_date(myAdif.get_field('QSO_DATE')) + ' ' + \
            format_time(myAdif.get_field('TIME_ON'))
        adif_qso = myAdif.get_adif()
        (count, status, info) = myQrz.upload(adif_qso)
        upload_count += count
        if verbose:
            if (status != 200):
                print('status: {}'.format(status))
            if (len(info) > 0):
                print('info: {}'.format(info))
            if (count == 0):
                print(qso_summary)
    # Done.
    print('{} QSOs found in ADIF file.'.format(qso_count))
    print('{} QSOs successfully uploaded.'.format(upload_count))
    sys.exit(0)


# End of file.
    