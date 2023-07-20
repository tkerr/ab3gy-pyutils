###############################################################################
# TextFile.py
# Author: Tom Kerr AB3GY
#
# TextFile class.
# Implements a class for reading simple text files, such as configuration files.
# Lines starting with '#' as the first non-whitespece character are considered
# comments.
#
# Designed for personal use by the author, but available to anyone under the
# license terms below.
###############################################################################

###############################################################################
# License
# Copyright (c) 2023 Tom Kerr AB3GY (ab3gy@arrl.net).
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

# Local packages.


##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################


##############################################################################
# TextFile class.
##############################################################################
class TextFile(object):
    """
    TextFile class.
    Implements a class for reading simple text files, such as configuration files.
    Lines starting with '#' as the first non-whitespece character are considered
    comments.
    """
    
    # ------------------------------------------------------------------------
    def __init__(self, filename='', open=True, close_on_eof=True):
        """
        Class constructor.
    
        Parameters
        ----------
        filename : str
            Optional name of the text file.
        open : bool
            If filename is supplied, then the file will be opened if True.
        close_on_eof : bool
            If True, file will automatically be closed when end-of-file is reached or on error.
            If False, the user must explicitly call the close() method.
        
        Returns
        -------
        None.
        """
        self._filename = filename
        self._fd = None
        self._close_on_eof = close_on_eof
        self._my_class = self.__class__.__name__
        self._COMMENT = '#'
        
        # Optionally open the file.
        if (len(self._filename) > 0) and open:
            self.open()

    # ------------------------------------------------------------------------
    def __del__(self):
        """
        Class destructor.
        """
        self.close()

    # ------------------------------------------------------------------------
    def _print_msg(self, msg):
        """
        Print an error message.
        
        Parameters
        ----------
        msg : str
            The error message to print.
        
        Returns
        -------
        None
        """
        print('{}: {}'.format(self._my_class, msg))

    # ------------------------------------------------------------------------
    def close(self):
        """
        Close the text file.
        """
        try:
            if self._fd is not None:
                self._fd.close()
        except Exception:
            pass
        self._fd = None
    
    # ------------------------------------------------------------------------
    def open(self, name='', close_on_eof=True):
        """
        Open the text file.
        
        Parameters
        ----------
        name : str
            Optional file name.  Uses self.filename if not specified.
        close_on_eof : bool
            If True, file will automatically be closed when end-of-file is reached or on error.
            If False, the user must explicitly call the close() method.
        
        Returns
        -------
        ok : bool
            True if file open is successful, False otherwise.
        """
        self._close_on_eof = close_on_eof
        ok = False
        if (len(name) > 0):
            self._filename = name
        if (len(self._filename) == 0):
            self.print_msg('No filename specified')
            return ok
        
        self.close()
        
        try:
            self._fd = open(self._filename, 'r')
            ok = True
        except Exception as err:
            self._print_msg('Error opening {}: {}'.format(self._filename, str(err)))
        return ok
    
    # ------------------------------------------------------------------------
    def readline(self, ignore_comments=True):
        """
        Read a line from the file.
        
        Parameters
        ----------
        ignore_comments : bool
            Returns the first non-blank, non-comment line if True.
            Returns the first non-blank line if False.
        
        Returns
        -------
        line : str
            The line from the file.  Returns a blank line if end-of-file is reached.
            All leading and trailing whitespace is stripped from non-blank lines.
        """
        line = ''
        if self._fd is not None:
            reading = True
            try:
                while reading:
                    line = self._fd.readline()
                    if (len(line) == 0):
                        # End of file. Done reading.
                        reading = False
                        if self._close_on_eof:
                            self.close()
                    else:
                        line = line.strip()
                        if (len(line) > 0):
                            if ignore_comments:
                                if not line.startswith(self._COMMENT):
                                    # Line is not a comment. Done reading.
                                    reading = False
                            else:
                                # Line is not blank. Done reading.
                                reading = False
            except Exception as err:
                self._print_msg('Error reading {}: {}'.format(self._filename, str(err)))
                line = ''
                if self._close_on_eof:
                    self.close()
        else:
            self._print_msg('File {} is not open.'.format(self._filename))
        return line
    
    # ------------------------------------------------------------------------
    def readlines(self, ignore_comments=True):
        """
        Read each non-blank line from the file into a list.
        
        Parameters
        ----------
        ignore_comments : bool
            Do not add comment lines if True.
        
        Returns
        -------
        lines : list
            A list of strings from the file.  Each list item is a line from the file.
            All leading and trailing whitespace is stripped from non-blank lines.
        """
        line_list = []
        line = self.readline(ignore_comments=ignore_comments)
        while (len(line) > 0):
            line_list.append(line)
            line = self.readline(ignore_comments=ignore_comments)
        return line_list
        
        
##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    
    my_filename = 'TextFile.py'
    my_file = TextFile(my_filename)
    line = my_file.readline()
    while (len(line) > 0):
        print(line)
        line = my_file.readline()
    
    my_file.open()
    my_list = my_file.readlines()
    print('\nList length: {} lines'.format(len(my_list)))
    print('First line: {}\n'.format(my_list[0]))
    
    my_file.readline() # This should print an error message
