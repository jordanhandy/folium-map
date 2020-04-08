##################################################################
# Map Renderer 
# Description:
# This program renders a map with various layers:
# Capital cities
# Volcanoes
# Map is saved as HTML and generated as a saved file
##################################################################

# import modules 
import folium
import pandas

# Pandas data frames:
# data_cities
# data_volcanoes
data_cities = pandas.read_csv("worldcities.csv")
data_volcanoes = pandas.read_csv("volcanoes.txt")

# HTML styling for popup 
html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""
# volcano latitude
# volcano longitude
# volcano elevation
# volcano name
lat = list(data_volcanoes["LAT"])
lon = list(data_volcanoes["LON"])
elev = list(data_volcanoes["ELEV"])
name = list(data_volcanoes["NAME"])

# capital city latitude
# capital city longitude
# capital city name
lat_list= list(data_cities["Latitude"])
lon_list= list(data_cities["Longitude"])
city_list=list(data_cities["Capital"])

# test feature group 
fg_test = folium.FeatureGroup("Test Markers")
# cities feature group
fg_cities = folium.FeatureGroup(name="Capital Cities")
# volcanoes feature group
fg_volcanoes = folium.FeatureGroup(name="Volcanoes")
# population lines feature group
fg_pop = folium.FeatureGroup(name="Population")

# colour function, to alter colour based open
# population levels
def colourMarker(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "crimson"

# Generate map with starting point, and starting zoom level
map = folium.Map(location=[43.760563, -79.453620], zoom_start=6, tiles="Stamen Terrain")

# map test marker
fg_test.add_child(folium.Marker(location=[33.5,-73.2], popup=f"This is a test popup!",icon=folium.Icon(color='green')))

# Using the data from the cities data csv, map all city markers
for lt, ln, city in zip(lat_list,lon_list, city_list):
    # location uses lat and lon, popup uses the city name from worldcities.csv 
    fg_cities.add_child(folium.Marker(location=[lt,ln], popup=folium.Popup(str(city),parse_html=True), icon=folium.Icon(color='red')))

# Using the data from the volcanoes data txt file, map all the volcanoes
for nm, lt, ln, el in zip(name, lat,lon,elev):
    # Create an iframe for HTML styling
    iframe = folium.IFrame(html=html % (nm, nm, el), width=200, height=100)
    # location uses lat and lon, and uses the iframe for the popup
    fg_volcanoes.add_child(folium.CircleMarker(radius=7,location=[lt,ln], popup=folium.Popup(iframe), color="grey", fill_color=colourMarker(el),fill_opacity=0.7))

# population lines
# use lambda function to style the colouring of land masses based on population level 
fg_pop.add_child(folium.GeoJson(data=open("world.json", "r", encoding="utf-8-sig").read(),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 1000000
 else 'orange' if 1000000 <- x['properties']['POP2005'] < 2000000 else 'red' }))

# Add children to map, consisting of Feature Groups
map.add_child(fg_cities)
map.add_child(fg_test)
map.add_child(fg_volcanoes)
map.add_child(fg_pop)
# Add a layer control to control different feature groups
map.add_child(folium.LayerControl())
# save the map
map.save("Capital-Cities-Map.html")
