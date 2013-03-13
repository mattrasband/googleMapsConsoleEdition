#!/usr/bin/env python

#   File:   local_maps.pub.py
#   Author: Matt Rasband (nerdwaller)
#   Description:
#       This is a quickly made console based google maps client.  It allows for
#       searches, directions, lat/lon generation from address, and address (nearest)
#       generation from lat/lon coordinates.

import urllib2, urllib, json, re
from googlemaps import GoogleMaps

# Google Maps API Key Required for use: https://code.google.com/apis/console/
key = '<get a key>'
gmaps = GoogleMaps(key)

# Pause function, saves typing.
def pause():
    print
    raw_input("(Press [enter] to continue...)")

# Get the User Action.
def getAction():
    print
    print "What would you like to do?"
    print "\tA - Get latitude/longitude of address."
    print "\tB - Get address from latitude/longutude"
    print "\tC - Locate something near an address"
    print "\tD - Get directions"
    print "\tQ - Terminate the program"
    return (raw_input('Selection: ')).upper()

# Obtain the Latitude/Longitude from the Provided address.
def getLatLng(address):
    lat, lng = gmaps.address_to_latlng(address)
    print "For address: ",  address.upper()
    print "\tLatitude,Longitude: ", str(lat) + ',' + str(lng)
    pause()

# Get the nearest address from the provided latitude/longitude
# Entry Format Example: -104.123,39.223
def getAddress(latlng):
    latlng = latlng.split(',')
    address = gmaps.latlng_to_address(float(latlng[0]), float(latlng[1]))
    print "For Coordinates: ", str(latlng[0]) + str(latlng[1])
    print "\tAddress: ", address
    pause()

# Get a directions list between two points.  Provides options for
# various routes and estimated times.
def getDirections(fromLoc, toLoc):
    directions = gmaps.directions(fromLoc, toLoc)
    numRoutes = len(directions['Directions']['Routes'])
    print
    print "Route Options: "
    for i in range(0, numRoutes):
        print '\tRoute ' + str(i) + ': {}'.format(directions['Directions']['Routes'][i]['Duration']['html'])
    selectedRoute = int(raw_input('Select a route: '))
    numSteps = len(directions['Directions']['Routes'][selectedRoute]['Steps'])
    thisRoute = directions['Directions']['Routes'][selectedRoute]['Steps']
    thisInfo = directions['Directions']['Routes'][selectedRoute]
    print
    print "Directions (total distance: {}; total time: {})".format(re.sub('&nbsp;', ' ', thisInfo['Distance']['html']), thisInfo['Duration']['html'])
    for i in range(0, numSteps):
        print '\tStep ' + str(i) + ': ' + re.sub('<[^>]+>', '', thisRoute[i]['descriptionHtml']) + ' ({})'.format(re.sub('&nbsp;', ' ', thisRoute[i]['Distance']['html']))

    pause()
    
# Search for stuff, such as a McDonald's in Denver, Co.
# User will get a list of locations, phone numbers & addresses
# and be allowed to get directions from an entered position to the
# selected index.
def searchFor(searchTerm, locale):
        options = gmaps.local_search(('{} near {}'.format(searchTerm, locale)))
        numOptions = len(options['responseData']['results'])
        print "{} {}'s near {}".format(numOptions, searchTerm, locale.upper())
        print
        for i in range(0, numOptions):
            this = options['responseData']['results'][i]
            print '\t' + str(i) + ' - ' + this['titleNoFormatting'] + ' ' + this['phoneNumbers'][0]['number']
            print '\t\t' + this['addressLines'][0] + ' ' + this['addressLines'][1]
        print
        whatNext = (raw_input('Get directions to a point (# or Q to exit): ')).upper()
        if (whatNext == 'Q'):
            return
        else:
            getDirections(raw_input("Starting Location: "), options['responseData']['results'][int(whatNext)]['addressLines'][0] + ' ' + options['responseData']['results'][int(whatNext)]['addressLines'][1])

def main():
    print "This is a console based google maps application, you can use various features of google maps using it."
    action = getAction()
    while (action != 'Q'):
        print
        if (action == 'A'):
            getLatLng(raw_input('Enter the address: '))
        elif (action == 'B'):
            getAddress(raw_input('Enter the latitude/longutude (format: 123.1234,-123.1234): '))
        elif (action == 'C'):
            searchFor(raw_input('What would you like to find (i.e. cafe, gas station, etc.): '), raw_input('Near (gps, address, city, zip): '))
        elif (action == 'D'):
            getDirections(raw_input('Start Location: '), raw_input('End Locations: '))
        else:
            exit
        
        action = getAction()
    
if __name__ == '__main__':
    main()
