###############################################################################
# encode.py
# Author: Tom Kerr AB3GY
#
# Functions to convert numeric and string data formats to arrays of bytes.
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

ENCODE_DEFAULT_ENDIAN = 'big'

#-----------------------------------------------------------------------------
def string(data, enc='utf-8'):
    """
    Convert a Python string to a byte array.
    Default encoding type is UTF-8.
    """
    return bytearray(data, enc)

#-----------------------------------------------------------------------------
def char(data, endian=ENCODE_DEFAULT_ENDIAN):
    """
    Convert a signed Python integer to a 1-byte array.
    Default byteorder is defined by ENCODE_DEFAULT_ENDIAN.
    """
    if endian == 'big':
        return struct.pack('>b', data)
    else:
        return struct.pack('<b', data)

#-----------------------------------------------------------------------------        
def byte(data, endian=ENCODE_DEFAULT_ENDIAN):
    """
    Convert an unsigned Python integer to a 1-byte array.
    Default byteorder is defined by ENCODE_DEFAULT_ENDIAN.
    """
    if endian == 'big':
        return struct.pack('>B', data)
    else:
        return struct.pack('<B', data)

#-----------------------------------------------------------------------------        
def word(data, endian=ENCODE_DEFAULT_ENDIAN):
    """
    Convert a signed Python integer to a 2-byte array.
    Default byteorder is defined by ENCODE_DEFAULT_ENDIAN.
    """
    if endian == 'big':
        return struct.pack('>h', data)
    else:
        return struct.pack('<h', data)

#-----------------------------------------------------------------------------        
def uword(data, endian=ENCODE_DEFAULT_ENDIAN):
    """
    Convert an unsigned Python integer to a 2-byte array.
    Default byteorder is defined by ENCODE_DEFAULT_ENDIAN.
    """
    if endian == 'big':
        return struct.pack('>H', data)
    else:
        return struct.pack('<H', data)

#-----------------------------------------------------------------------------        
def long(data, endian=ENCODE_DEFAULT_ENDIAN):
    """
    Convert a signed Python integer to a 4-byte array.
    Default byteorder is defined by ENCODE_DEFAULT_ENDIAN.
    """
    if endian == 'big':
        return struct.pack('>l', data)
    else:
        return struct.pack('<l', data)

#-----------------------------------------------------------------------------        
def ulong(data, endian=ENCODE_DEFAULT_ENDIAN):
    """
    Convert an unsigned Python integer to a 4-byte array.
    Default byteorder is defined by ENCODE_DEFAULT_ENDIAN.
    """
    if endian == 'big':
        return struct.pack('>L', data)
    else:
        return struct.pack('<L', data)

#-----------------------------------------------------------------------------        
def quad(data, endian=ENCODE_DEFAULT_ENDIAN):
    """
    Convert a signed Python integer to an 8-byte array.
    Default byteorder is defined by ENCODE_DEFAULT_ENDIAN.
    """
    if endian == 'big':
        return struct.pack('>q', data)
    else:
        return struct.pack('<q', data)
        
#-----------------------------------------------------------------------------        
def uquad(data, endian=ENCODE_DEFAULT_ENDIAN):
    """
    Convert an unsigned Python integer to an 8-byte array.
    Default byteorder is defined by ENCODE_DEFAULT_ENDIAN.
    """
    if endian == 'big':
        return struct.pack('>Q', data)
    else:
        return struct.pack('<Q', data)

#-----------------------------------------------------------------------------        
def float(data, endian=ENCODE_DEFAULT_ENDIAN):
    """
    Convert a Python float to a 4-byte array.
    Default byteorder is defined by ENCODE_DEFAULT_ENDIAN.
    """
    if endian == 'big':
        return struct.pack('>f', data)
    else:
        return struct.pack('<f', data)

#-----------------------------------------------------------------------------        
def double(data, endian=ENCODE_DEFAULT_ENDIAN):
    """
    Convert a Python float to an 8-byte array.
    Default byteorder is defined by ENCODE_DEFAULT_ENDIAN.
    """
    if endian == 'big':
        return struct.pack('>d', data)
    else:
        return struct.pack('<d', data)
        