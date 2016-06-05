import foursquare
import urllib2
import json
import time
from django.utils.encoding import smart_str, smart_unicode
import numpy as np



# Foursquare access 
CLIENT_ID = #### HIDDEN ####
CLIENT_SECRET = #### HIDDEN ####
VERSION = time.strftime("%Y%m%d") # most recent database version


### Construct the client object
client = foursquare.Foursquare(CLIENT_ID, CLIENT_SECRET, redirect_uri='http://fondu.com/oauth/authorize')


### Search in radius around each of these lat, lon grid points
lat_grid = np.arange(32.09,32.36,0.01)
lon_grid = np.arange(-111.15,-110.5,0.01)
print "Searching at", len(lat_grid)*len(lon_grid) ,"grid locations"


# max radius in meters foursquare allows
radius = 2000
radius = str(radius)


### Store unique venues here
venue_dict = { }

for lat in lat_grid:
    for lon in lon_grid:

        print "Current location:", lat,lon
        ll = str(lat) + "," + str(lon)

        ### Pull all venues within radius of lat, lon with catergoryId==Grocery store
        venues = client.venues.search(params={'v': VERSION, 'll': ll, 'intent': 'browse', 
                                         'radius': radius, 'limit': 100,
                                         'categoryId': '4bf58dd8d48988d118951735' })["venues"]
    
    
        print len(venues) ,"grocery stores found"

        cnt_repeat = 0
        for ven in venues:
    
            name = ven["name"]
            ven_lat = ven["location"]["lat"]
            ven_lng = ven["location"]["lng"]
            distance = ven["location"]["distance"]
            addr = distance = ven["location"]["formattedAddress"][0]
        
            ### Deal with repeatedly found stores by checking if unique
            ### key already added to dictionary
            create_unique_key = str(ven_lat) + ',' + str(ven_lng) + '-' , name
        
        
            if create_unique_key in venue_dict:
                cnt_repeat += 1
            else:
                venue_dict[create_unique_key] = [(ven_lat,ven_lng), name, addr]
            
        print cnt_repeat ,"venues already in dict\n"
print "Total number of unique grocery stores:", len(venue_dict)


### Write to csv
f = open('grocery_stores.csv', 'w')
f.write("lat,lon,name,addr\n")
for ven_key, ven_data in venue_dict.items():

    lat = ven_data[0][0]
    lon = ven_data[0][1]
    name = ven_data[1]
    addr = ven_data[2]
    
    # remove any commas from address so csv file isn't messed up
    addr = addr.replace(',','')
    
    f.write(smart_str(lat) + "," + smart_str(lon) + "," + smart_str(name) + "," + 
            smart_str(addr) + "\n")

f.close()

