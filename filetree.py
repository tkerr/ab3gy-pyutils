###############################################################################
# filetree.py
# Author: Tom Kerr AB3GY
#
# filetree class.
# The filetree class provides an iterator to loop through all files in a 
# directory tree.
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
import os
import sys


##############################################################################
# Local envrionment setup.
##############################################################################

scriptname = os.path.basename(sys.argv[0])


##############################################################################
# filetree class.
##############################################################################
class filetree(object):
    """
    filetree class.
    Provides an iterator to loop through all files in a directory tree.
    Only files are returned; directories are ignored.
    """
    
    # ------------------------------------------------------------------------
    def __init__(self, dir):
        """
        Class constructor.
        Must provide a top-level directory for initialization.
        """
        self.dir = dir
        
    # ------------------------------------------------------------------------
    def __iter__(self):
        """
        Initializes the iterator.
        """
        self.root   = ''
        self.dirs   = []
        self.files  = []
        self.index  = 0
        self.length = len(self.files)
        self.walk   = os.walk(self.dir)
        return self

    # ------------------------------------------------------------------------
    def __next__(self):
        """
        Computes and returns the next file in the sequence.
        Raises the StopIteration exception when complete.
        """
        file = self.next_file()
        if len(file) > 0:
            return file
        else:
            raise StopIteration

    # ------------------------------------------------------------------------
    def all_files(self):
        """
        The iterator function to use in a for() loop.
        
        Example usage:
            myFileTree = filetree(sys.argv[1])
            for file in myFileTree.all_files():
                do_stuff()
        """
        return iter(self)

    # ------------------------------------------------------------------------
    def next_file(self):
        """
        Computes the next file in the directory hierarchy.
        Returns the full path to the next file as a string.
        Returns an empty string ('') when all files have been returned.
        """
        file = ''
        if self.index >= self.length:
            try:
                (self.root, self.dirs, self.files) = next(self.walk)
                self.index = 0
                self.length = len(self.files)
                file = self.next_file()
            except StopIteration:
                file = ''
        else:
            file = os.path.join(self.root, self.files[self.index])
            self.index += 1
        return file


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":

    if (len(sys.argv) < 2):
        print('Usage:', scriptname, '<top-level-dir>')
        sys.exit(1)
        
    file_count = 0
    myFileTree = filetree(sys.argv[1])
    
    for file in myFileTree.all_files():
        file_count += 1
        print(file)
        
    print(str(file_count), 'files found.')
   