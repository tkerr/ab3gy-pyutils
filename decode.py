###############################################################################
# decode.py
# Author: Tom Kerr AB3GY
#
# Functions to convert arrays of bytes to numeric and string data formats.
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

import struct

DECODE_DEFAULT_ENDIAN = 'big'

#-----------------------------------------------------------------------------
def string(data, datalen, enc='utf-8'):
    """
    Convert an array of bytes to a Python string.
    Default encoding type is UTF-8.
    """
    return data[0:datalen].decode(enc)
    
#-----------------------------------------------------------------------------
def char(data, endian=DECODE_DEFAULT_ENDIAN):
    """
    Convert a 1-byte signed char to a signed Python integer.
    Default byteorder is defined by DECODE_DEFAULT_ENDIAN.
    """
    if endian == 'big':
        return struct.unpack('>b', data[0:1])[0]
    else:
        return struct.unpack('<b', data[0:1])[0]
        
#-----------------------------------------------------------------------------    
def byte(data, endian=DECODE_DEFAULT_ENDIAN):
    """
    Convert a 1-byte unsigned char to an unsigned Python integer.
    Default byteorder is defined by DECODE_DEFAULT_ENDIAN.
    """
    if endian == 'big':
        return struct.unpack('>B', data[0:1])[0]
    else:
        return struct.unpack('<B', data[0:1])[0]

#-----------------------------------------------------------------------------        
def word(data, endian=DECODE_DEFAULT_ENDIAN):
    """
    Convert a 2-byte array to a signed Python integer.
    Default byteorder is defined by DECODE_DEFAULT_ENDIAN.
    """
    if endian == 'big':
        return struct.unpack('>h', data[0:2])[0]
    else:
        return struct.unpack('<h', data[0:2])[0]

#-----------------------------------------------------------------------------        
def uword(data, endian=DECODE_DEFAULT_ENDIAN):
    """
    Convert a 2-byte array to an unsigned Python integer.
    Default byteorder is defined by DECODE_DEFAULT_ENDIAN.
    """
    if endian == 'big':
        return struct.unpack('>H', data[0:2])[0]
    else:
        return struct.unpack('<H', data[0:2])[0]

#-----------------------------------------------------------------------------        
def long(data, endian=DECODE_DEFAULT_ENDIAN):
    """
    Convert a 4-byte array to a signed Python integer.
    Default byteorder is defined by DECODE_DEFAULT_ENDIAN.
    """
    if endian == 'big':
        return struct.unpack('>l', data[0:4])[0]
    else:
        return struct.unpack('<l', data[0:4])[0]

#-----------------------------------------------------------------------------        
def ulong(data, endian=DECODE_DEFAULT_ENDIAN):
    """
    Convert a 4-byte array to an unsigned Python integer.
    Default byteorder is defined by DECODE_DEFAULT_ENDIAN.
    """
    if endian == 'big':
        return struct.unpack('>L', data[0:4])[0]
    else:
        return struct.unpack('<L', data[0:4])[0]

#-----------------------------------------------------------------------------        
def quad(data, endian=DECODE_DEFAULT_ENDIAN):
    """
    Convert an 8-byte array to a signed Python integer.
    Default byteorder is defined by DECODE_DEFAULT_ENDIAN.
    """
    if endian == 'big':
        return struct.unpack('>q', data[0:8])[0]
    else:
        return struct.unpack('<q', data[0:8])[0]

#-----------------------------------------------------------------------------        
def uquad(data, endian=DECODE_DEFAULT_ENDIAN):
    """
    Convert an 8-byte array to an unsigned Python integer.
    Default byteorder is defined by DECODE_DEFAULT_ENDIAN.
    """
    if endian == 'big':
        return struct.unpack('>Q', data[0:8])[0]
    else:
        return struct.unpack('<Q', data[0:8])[0]

#-----------------------------------------------------------------------------        
def float(data, endian=DECODE_DEFAULT_ENDIAN):
    """
    Convert a 4-byte array to a Python float.
    Default byteorder is defined by DECODE_DEFAULT_ENDIAN.
    """
    if endian == 'big':
        return struct.unpack('>f', data[0:4])[0]
    else:
        return struct.unpack('<f', data[0:4])[0]

#-----------------------------------------------------------------------------        
def double(data, endian=DECODE_DEFAULT_ENDIAN):
    """
    Convert an 8-byte array to a Python float.
    Default byteorder is defined by DECODE_DEFAULT_ENDIAN.
    """
    if endian == 'big':
        return struct.unpack('>d', data[0:8])[0]
    else:
        return struct.unpack('<d', data[0:8])[0]
        