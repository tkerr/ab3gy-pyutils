###############################################################################
# xmlnode.py
# Author: Tom Kerr AB3GY
#
# Class used to parse simple XML nodes for amateur radio purposes.
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
import re
import sys


##############################################################################
# Functions.
##############################################################################

  
##############################################################################
# xmlnode class.
##############################################################################
class xmlnode(object):
    """
    A class used to perform simple XML parsing of amateur radio application data.
    
    An xmlnode object represents a node of an XML tree structure.  It can be
    a root element, a parent element, or a child element.
    
    This class parses an XML node as a text string and can return items such
    as the node name, node parameters, and the node contents.
    
    This class expects well-formed XML, and may not work otherwise.
    
    Limitations
    -----------
    1. The parser only handles nodes/elements with start and end tags, e.g.,
    <foo></foo>.  Single tag elements such as <foo /> are not supported.
    
    2. The parser does not ignore XML comments.  Keywords in comments may 
    cause the parser to fail.
    """
    # ------------------------------------------------------------------------
    def __init__(self):
        """
        Class constructor.
        """
        # Variable initialization.
        self.__version__ = str("0.1")  # Version per PEP 396
        self._node_name  = ""          # The last node name that was parsed
        self._node_attrs = ""          # Node attribute values as a single string
        self._node_text  = ""          # Node text - everything except the opening/closing tags
        
    # ------------------------------------------------------------------------
    def element_names(self, content):
        """
        Return a list of all element names in the provided content.  All element
        names are returned regardless of the XML tree hierarchy.
        """
        name_list = []
        pattern = '\<(\w+)\s*(.*?)\>'
        
        m = re.search(pattern, content, re.DOTALL)
        
        while m:
            name_list.append(m.group(1))
            content = content[m.end(1):]
            m = re.search(pattern, content, re.DOTALL)
        return name_list
    
    # ------------------------------------------------------------------------
    def node_name(self):
        """
        Return the last node name that was parsed as a string.
        
        Use parse() to parse the node, then call this method to return the
        node name.
        """
        return self._node_name
        
    # ------------------------------------------------------------------------
    def node_attrs(self):
        """
        Return all of the node attributes as a single string.
        
        Use parse() to parse the node, then call this method to return the
        node attributes.
        """
        return self._node_attrs
        
    # ------------------------------------------------------------------------
    def node_text(self):
        """
        Return all of the node text as a single string.
        
        Use parse() to parse the node, then call this method to return the
        node text.
        
        If there are nested elements, then their XML tags will be contained in
        the string.
        """    
        return self._node_text
        
    # ------------------------------------------------------------------------
    def parse(self, node, content):
        """
        Find and parse the node into its name, attributes, and text content.
        
        Parameters
        ----------
        node : string : The node name to parse
        content : string : The node content to parse, including all XML tags
        
        Returns True if the node was found, False otherwise.
        """
        found = False
        pattern = '\<(' + node + ')\s*(.*?)\>(.*)\<\/' + node + '\>'
        m = re.search(pattern, content, re.DOTALL)
        if m:
            self._node_name  = m.group(1)
            self._node_attrs = m.group(2)
            self._node_text  = m.group(3).strip()
            found       = True;
        else:
            self._node_name  = node
            self._node_attrs = ""
            self._node_text  = ""
        return found
        
        
###########################################################################
# Main program example test script.
########################################################################### 
if __name__ == "__main__":

    # Sample XML node used to test the parser.
    # Taken from the QRZ XML Interface specification.
    # https://www.qrz.com/XML/current_spec.html
    node_qrz = \
        '<?xml version="1.0" ?>\n \
        <QRZDatabase version="1.33">\n \
          <Callsign>\n \
            <call>AA7BQ</call>\n \
            <fname>FRED L</fname>\n \
            <name>LLOYD</name>\n \
            <addr1>8711 E PINNACLE PEAK RD 193</addr1>\n \
            <addr2>SCOTTSDALE</addr2>\n \
            <state>AZ</state>\n \
            <zip>85255</zip>\n \
            <GMTOffset>-7</GMTOffset>\n \
          </Callsign>\n \
          <Session>\n \
           <Key>2331uf894c4bd29f3923f3bacf02c532d7bd9</Key>\n \
           <Count>123</Count>\n \
           <SubExp>Wed Jan 1 12:34:03 2013</SubExp>\n \
           <GMTime>Sun Nov 16 04:13:46 2012</GMTime>\n \
         </Session>\n \
        </QRZDatabase>'
        
    myXmlNode = xmlnode()
    
    myXmlNode.parse('QRZDatabase', node_qrz)
    if myXmlNode.node_name()  != 'QRZDatabase' : print('Error parsing QRZDatabase')
    if myXmlNode.node_attrs() != 'version="1.33"' : print('Error parsing QRZDatabase attributes')
    
    # Extract the Callsign node.
    found = myXmlNode.parse('Callsign', node_qrz)
    if not found : print('Error parsing Callsign')
    node_callsign = myXmlNode.node_text()
    
    # Check elements in the Callsign node.
    
    myXmlNode.parse('call', node_callsign)
    print('call:      ' + myXmlNode.node_text())
    if not found : print('Error parsing call')
    if myXmlNode.node_name()  != 'call'  : print('Error parsing call name')
    if myXmlNode.node_attrs() != ''      : print('Error parsing call attributes')
    if myXmlNode.node_text()  != 'AA7BQ' : print('Error parsing call text')
    
    # Check case sensitivity
    found = myXmlNode.parse('CALL', node_callsign)
    if found : print('Error 1 parsing CALL - must be case sensitive')
    if myXmlNode.node_text() != '' : print('Error 2 parsing CALL - must be case sensitive')
    
    myXmlNode.parse('fname', node_callsign)
    print('fname:     ' + myXmlNode.node_text())
    if myXmlNode.node_text() != 'FRED L' : print('Error parsing fname')
    
    myXmlNode.parse('name', node_callsign)
    print('name:      ' + myXmlNode.node_text())
    if myXmlNode.node_text() != 'LLOYD' : print('Error parsing name')
    
    myXmlNode.parse('addr1', node_callsign)
    print('addr1:     ' + myXmlNode.node_text())
    if myXmlNode.node_text() != '8711 E PINNACLE PEAK RD 193' : print('Error parsing addr1')
    
    myXmlNode.parse('addr2', node_callsign)
    print('addr2:     ' + myXmlNode.node_text())
    if myXmlNode.node_text() != 'SCOTTSDALE' : print('Error parsing addr2')
    
    myXmlNode.parse('state', node_callsign)
    print('state:     ' + myXmlNode.node_text())
    if myXmlNode.node_text() != 'AZ' : print('Error parsing state')
    
    myXmlNode.parse('zip', node_callsign)
    print('zip:       ' + myXmlNode.node_text())
    if myXmlNode.node_text() != '85255' : print('Error parsing zip')
    
    myXmlNode.parse('GMTOffset', node_callsign)
    print('GMTOffset: ' + myXmlNode.node_text())
    if myXmlNode.node_text() != '-7' : print('Error parsing GMTOffset')
    
    # Make sure Session elements are not in the callsign string.
    found = myXmlNode.parse('Session', node_callsign)
    if found : print('Error 1 parsing Session - should not be present')
    if myXmlNode.node_text() != '' : print('Error 2 parsing Session - should not be present')
    found = myXmlNode.parse('Key', node_callsign)
    if found : print('Error 1 parsing Key - should not be present')
    if myXmlNode.node_text() != '' : print('Error 2 parsing Key - should not be present')
    
    # Parse the Session node.
    found = myXmlNode.parse('Session', node_qrz)
    if not found : print('Error parsing Session')
    node_session = myXmlNode.node_text()
    
    myXmlNode.parse('Key', node_session)
    print('Key:       ' + myXmlNode.node_text())
    if myXmlNode.node_text() != '2331uf894c4bd29f3923f3bacf02c532d7bd9' : print('Error parsing Key')
    
    # Print the list of Callsign element names.
    sys.stdout.write('Callsign elements: ')
    print(myXmlNode.element_names(node_callsign))
    
    sys.exit(0) 
    