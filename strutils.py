###############################################################################
# strutils.py
# Author: Tom Kerr AB3GY
#
# Python string utility functions that I have found useful for my amateur
# radio application development.
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

# System level packages.
import locale

# Get the encoding used for text data on this computer.
enc_in = locale.getpreferredencoding()


##############################################################################
# Functions.
##############################################################################

# ----------------------------------------------------------------------------
def format_date(date_in):
    """
    Format a raw date string with dashes.
    
    Parameters
    ----------
    date_in : str
        The input date string in YYYYMMDD format.
        
    Returns
    -------
    date_out : str
        The formatted date string in YYYY-MM-DD format.
    """
    date_out = date_in[0:4] + '-' + date_in[4:6] + '-' + date_in[6:8]
    return date_out
    
# ----------------------------------------------------------------------------
def format_time(time_in):
    """
    Format a raw time string with colons.
    
    Parameters
    ----------
    time_in : str
        The input time string in HHMM or HHMMSS format.
        
    Returns
    -------
    time_out : str
        The formatted time string in HH:MM:00 or HH:MM:SS format.
    """
    time_out = time_in[0:2] + ':' + time_in[2:4] + ':'
    if (len(time_in) >= 6): 
        time_out += time_in[4:6]
    else:
        time_out += '00'
    return time_out
    
# ----------------------------------------------------------------------------
def format_timestamp(timestamp_in):
    """
    Format a raw timestamp string with dashes and colons.
    
    Parameters
    ----------
    timestamp_in : str
        The input timestamp string in YYYYMMDDHHMM or YYYYMMDDHHMMSS format.
        
    Returns
    -------
    timestamp_out : str
        The formatted time string in "YYYY-MM-DD HH:MM:00" or "YYYY-MM-DD HH:MM:SS" format.
    """
    date_in = timestamp_in[0:8]
    time_in = timestamp_in[8:14]
    timestamp_out = format_date(date_in) + ' ' + format_time(time_in)
    return timestamp_out

# ----------------------------------------------------------------------------
def make_utf8(string_in):
    """
    Ensure a string is encoded as UTF-8.
    
    QRZ lookups can return special characters in foreign names that can't be
    printed or written to a file (at least on Windows machines).
    
    Special characters that can't be converted to UTF-8 are silently ignored 
    and dropped from the string.
    
    TODO: Attempts to use 'replace' instead of 'ignore' don't work, at least
    on Windows 10.  The replaced character is not a question mark.
    
    Parameters
    ----------
    string_in : str
        The input string to convert.
        
    Returns
    -------
    string_out : str
        The converted string.
    """
    global enc_in
    return string_in.encode(enc_in, errors='replace').decode('utf-8', errors='replace')

# ----------------------------------------------------------------------------
def unformat_date(date_in):
    """
    Remove dashes from a date string to create a numeric date string.
    
    Parameters
    ----------
    date_in : str
        The input formatted date string in YYYY-MM-DD format.
        
    Returns
    -------
    date_out : str
        The un-formatted date string in YYYYMMDD format.
    """
    date_out = date_in[0:4] + date_in[5:7] + date_in[8:10]
    return date_out

# ----------------------------------------------------------------------------
def unformat_time(time_in):
    """
    Remove colons from a time string to create a numeric time string.
    
    Parameters
    ----------
    time_in : str
        The input time string in HH:MM or HH:MM:SS format.
        
    Returns
    -------
    time_out : str
        The un-formatted time string in HHMM or HHMMSS format.
    """
    time_out = time_in[0:2] + time_in[3:5]
    if (len(time_in) >= 5): 
        time_out += time_in[6:8]
    return time_out

##############################################################################
# Main test program
##############################################################################
if __name__ == "__main__":
    txt = 'My name is Ståle, and this is a bit möre cömplex sentence.'
    date = '19991231'
    time1 = '2359'
    time2 = '235901'
    
    print('Original:         ', txt)
    print('UTF-8:            ', make_utf8(txt))
    
    print('Unformatted date: ', date)
    print('Formatted date:   ', format_date(date))
    print('Unformatted date: ', unformat_date(format_date(date)))
    
    print('Unformatted time: ', time1)
    print('Formatted time:   ', format_time(time1))
    print('Unformatted time: ', unformat_time(format_time(time1)))
    
    print('Unformatted time: ', time2)
    print('Formatted time:   ', format_time(time2))
    print('Unformatted time: ', unformat_time(format_time(time2)))
