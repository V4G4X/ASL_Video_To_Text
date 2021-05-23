import geocoder
from geopy.geocoders import Nominatim
  
# g = geocoder.ip('me')
# print(g.latlng)
# print(type(g))
# Initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiExercises")
   
# Get location with geocode
#location = geolocator.geocode(Latitude+","+Longitude)
# location = geolocator.reverse(g.latlng) 

# Dsiplay location
# print("\nLatitude and Longitude: ")
# print(type(g.latlng))
# print(str(location))

def getLocation():
    g = geocoder.ip('me')
    return tuple(g.latlng)