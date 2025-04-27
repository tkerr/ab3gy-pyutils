# AB3GY Python Utilities  
A set of Python utility scripts that I have found useful for my amateur radio hobby application development.  

Many were designed to solve a specific problem and may not provide general purpose functionality.  Feel free to use these as a starting point for your project and tailor them to your needs.  

Developed for personal use by the author, but available to anyone under the license terms below.  

## Scripts  

### ConfigFile.py  
Implements a .INI configuration file for saving/restoring configuration parameters. File format is similar to Microsoft Windows .INI files.  

### encode.py  
Functions to convert numeric and string data formats to arrays of bytes.  

### decode.py  
Functions to convert arrays of bytes to numeric and string data formats.  

### filetree.py  
The filetree class provides an iterator to loop through all files in a directory tree.  

### n1mmmon.py
A class used to receive contacts from N1MM+ over a UDP connection.

### great_circle.py  
Functions for performing Great Circle calculations.  

### qrzlookup.py  
Class to perform QRZ.COM XML database callsign lookups. Use of this class requires a QRZ.com XML logbook data subscription.  

### qrzupload.py
Class to perform QRZ.com ADIF QSO upload. Use of this class requires a a QRZ.com logbook data subscription.

### strutils.py  
Various string utility functions, mostly for date and time formatting and UTF-8 encoding.  

### TextFile.py  
Implements a class for reading simple text files, such as configuration files.  Comments and blank lines are
automatically stripped during the read operation.  

### xmlnode.py  
Class used to parse simple XML nodes for amateur radio purposes.  

## Dependencies  
Written for Python 3.x.  
No other known dependencies.  
 
## Author  
Tom Kerr AB3GY  
ab3gy@arrl.net  

## License  
Released under the 3-clause BSD license.  
See license.txt for details.  
