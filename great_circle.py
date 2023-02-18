##############################################################################
# great_circle.py
# Author: Tom Kerr AB3GY
# 
# Functions for performing Great Circle calculations.
#
# Reference: https://www.movable-type.co.uk/scripts/latlong.html
#
# Designed for personal use by the author, but available to anyone under the
# license terms below.
##############################################################################

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

import math
import sys

###########################################################################
#  Constants and variables
###########################################################################
EARTH_RADIUS_KM = 6371.0088  # Earth mean radius in kilometers
EARTH_RADIUS_MI = 3958.7613  # Earth mean radius in miles

distance_is_miles = True     # True = miles, False = kilometers


###########################################################################
#  Functions
###########################################################################

#-----------------------------------------------------------------------------
def bearing(lat1, lon1, lat2, lon2):
    """
    Calculate the compass bearing from point 1 to point 2.
    All units are in decimal degrees.
    North/East = positive, South/West = negative
    
    Returns a compass bearing in the range 0 - 360 degrees
    """
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    dlon = lon2_rad - lon1_rad
    y = math.sin(dlon) * math.cos(lat2_rad)
    x = (math.cos(lat1_rad) * math.sin(lat2_rad)) \
        - (math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon))
    b_rad = math.atan2(y, x)
    b_deg = math.degrees(b_rad)
    b_deg = math.fmod(b_deg + 360.0, 360.0)
    return b_deg
    
#-----------------------------------------------------------------------------
def destination(lat1, lon1, brng, dist):
    """
    Calculate destination point (lat/lon) from a start point, initial bearing
    and distance.
    
    lat, lon, bearing are in decimal degrees.  
    North/East = positive, South/West = negative
    
    Bearing is clockwise from North (0 - 360).
    
    Distance is either miles or km depending on the 'distance_is_miles' setting.
    """
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    brng_rad = math.radians(brng)
    delta = 0.0
    if distance_is_miles:
        delta = dist / EARTH_RADIUS_MI
    else:
        delta = dist / EARTH_RADIUS_KM
    
    c1 = math.cos(lat1_rad)
    s1 = math.sin(lat1_rad)
    cd = math.cos(delta)
    sd = math.sin(delta)
    
    a1 = (s1 * cd) + (c1 * sd * math.cos(brng_rad))
    lat2_rad = math.asin(a1)
    
    y = math.sin(brng_rad) * sd * c1
    x = cd - (s1 * math.sin(lat2_rad))
    lon2_rad = lon1_rad + math.atan2(y, x)
    return [math.degrees(lat2_rad), math.degrees(lon2_rad)]
    
#-----------------------------------------------------------------------------
def distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points using the
    haversine formula.
    
    Input latitude and longitude are expected to be in decimal degrees.
    
    Latitude:  positive = North, negative = South
    Longitude: positive = East, negative = West
    
    Returns the great-circle distance in units of miles/km depending
    on the setting of 'distance_is_miles' variable
    """
    d = 0.0
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    a1 = math.sin((lat2_rad - lat1_rad)/2.0)
    a2 = math.sin((lon2_rad - lon1_rad)/2.0)
    a  = (a1 * a1) + (math.cos(lat1_rad) * math.cos(lat2_rad) * a2 * a2)
    c  = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    if distance_is_miles:
        d = EARTH_RADIUS_MI * c
    else:
        d = EARTH_RADIUS_KM * c
    return math.fabs(d)


###########################################################################
#  Main program 
###########################################################################
    
if __name__ == "__main__":
    # Nothing to do.
    sys.exit(0)