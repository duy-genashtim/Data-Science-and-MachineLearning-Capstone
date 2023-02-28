import folium
import wget
import pandas as pd
import webbrowser

# Import folium MarkerCluster plugin
from folium.plugins import MarkerCluster
# Import folium MousePosition plugin
from folium.plugins import MousePosition
# Import folium DivIcon plugin
from folium.features import DivIcon

# ## Task 1: Mark all launch sites on a map
# First, let's try to add each site's location on a map using site's latitude and longitude coordinates

# The following dataset with the name `spacex_launch_geo.csv` is an augmented dataset with latitude and longitude added for each site.

# Download and read the `spacex_launch_geo.csv`
spacex_csv_file = wget.download('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv')
spacex_df=pd.read_csv(spacex_csv_file)

# Now, you can take a look at what are the coordinates for each site.
# Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]
# print(launch_sites_df)

# 100% [................................................................................] 7710 / 7710    Launch Site        Lat        Long
# 0   CCAFS LC-40  28.562302  -80.577356
# 1  CCAFS SLC-40  28.563197  -80.576820
# 2    KSC LC-39A  28.573255  -80.646895
# 3   VAFB SLC-4E  34.632834 -120.610746


# Above coordinates are just plain numbers that can not give you any intuitive insights about where are those launch sites. If you are very good at geography, you can interpret those numbers directly in your mind. If not, that's fine too. Let's visualize those locations by pinning them on a map.

# We first need to create a folium `Map` object, with an initial center location to be NASA Johnson Space Center at Houston, Texas.

# Start location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)

# We could use `folium.Circle` to add a highlighted circle area with a text label on a specific coordinate. For example,
# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name
circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))
# Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name
marker = folium.map.Marker(
    nasa_coordinate,
    # Create an icon as a text label
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
        )
    )
site_map.add_child(circle)
site_map.add_child(marker)


# and you should find a small yellow circle near the city of Houston and you can zoom-in to see a larger circle.
# Now, let's add a circle for each launch site in data frame `launch_sites`

# Initial the map
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)
# For each launch site, add a Circle object based on its coordinate (Lat, Long) values. In addition, add Launch site name as a popup label

for index, row in launch_sites_df.iterrows():
    coordinate = [row['Lat'],row['Long']]
    # print(row)
#     Launch Site    VAFB SLC-4E
# Lat                34.6328
# Long              -120.611
# Name: 3, dtype: object
    circle = folium.Circle(coordinate, radius=1000,color='#000000',fill=True).add_child(folium.Popup(row['Launch Site']))
    marker = folium.map.Marker(coordinate,icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0), html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % row['Launch Site'], ))
    site_map.add_child(circle)
    site_map.add_child(marker)

# Task 2: Mark the success/failed launches for each site on the map
# Next, let's try to enhance the map by adding the launch outcomes for each site, and see which sites have high success rates.
# Recall that data frame spacex_df has detailed launch records, and the `class` column indicates if this launch was successful or not

# print(spacex_df.tail(10))
# Launch Site        Lat       Long  class
# 46    KSC LC-39A  28.573255 -80.646895      1
# 47    KSC LC-39A  28.573255 -80.646895      1
# 48    KSC LC-39A  28.573255 -80.646895      1
# 49  CCAFS SLC-40  28.563197 -80.576820      1
# 50  CCAFS SLC-40  28.563197 -80.576820      1
# 51  CCAFS SLC-40  28.563197 -80.576820      0
# 52  CCAFS SLC-40  28.563197 -80.576820      0
# 53  CCAFS SLC-40  28.563197 -80.576820      0
# 54  CCAFS SLC-40  28.563197 -80.576820      1
# 55  CCAFS SLC-40  28.563197 -80.576820      0
# Next, let's create markers for all launch records.
# If a launch was successful `(class=1)`, then we use a green marker and if a launch was failed, we use a red marker `(class=0)`

# Note that a launch only happens in one of the four launch sites, which means many launch records will have the exact same coordinate. Marker clusters can be a good way to simplify a map containing many markers having the same coordinate.
marker_cluster = MarkerCluster()
def assign_marker_color(launch_outcome):
    if launch_outcome == 1:
        return 'green'
    else:
        return 'red'

spacex_df['marker_color'] = spacex_df['class'].apply(assign_marker_color)
# print(spacex_df.tail(10))
# Launch Site        Lat       Long  class marker_color
# 46    KSC LC-39A  28.573255 -80.646895      1        green
# 47    KSC LC-39A  28.573255 -80.646895      1        green
# 48    KSC LC-39A  28.573255 -80.646895      1        green
# 49  CCAFS SLC-40  28.563197 -80.576820      1        green
# 50  CCAFS SLC-40  28.563197 -80.576820      1        green
# 51  CCAFS SLC-40  28.563197 -80.576820      0          red
# 52  CCAFS SLC-40  28.563197 -80.576820      0          red
# 53  CCAFS SLC-40  28.563197 -80.576820      0          red
# 54  CCAFS SLC-40  28.563197 -80.576820      1        green
# 55  CCAFS SLC-40  28.563197 -80.576820      0          red

# *TODO:* For each launch result in `spacex_df` data frame, add a `folium.Marker` to `marker_cluster`
# Add marker_cluster to current site_map
site_map.add_child(marker_cluster)


# for each row in spacex_df data frame
# create a Marker object with its coordinate
# and customize the Marker's icon property to indicate if this launch was successed or failed, 
# e.g., icon=folium.Icon(color='white', icon_color=row['marker_color']

for index, record in spacex_df.iterrows():
    # TODO: Create and add a Marker cluster to the site map
    # marker = folium.Marker(...)
    coordinate = [record['Lat'],record['Long']]
    marker = folium.Marker(coordinate, icon=folium.Icon(color='white', icon_color=record['marker_color']) )
    marker_cluster.add_child(marker)

# From the color-labeled markers in marker clusters, you should be able to easily identify which launch sites have relatively high success rates.
# TASK 3: Calculate the distances between a launch site to its proximities
# Next, we need to explore and analyze the proximities of launch sites.
# Let's first add a `MousePosition` on the map to get coordinate for a mouse over a point on the map. As such, while you are exploring the map, you can easily find the coordinates of any points of interests (such as railway)
# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)

site_map.add_child(mouse_position)

# Now zoom in to a launch site and explore its proximity to see if you can easily find any railway, highway, coastline, etc. Move your mouse to these points and mark down their coordinates (shown on the top-left) in order to the distance to the launch site.
# You can calculate the distance between two points on the map based on their `Lat` and `Long` values using the following method:
from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance
# *TODO:* Mark down a point on the closest coastline using MousePosition and calculate the distance between the coastline point and the launch site.
# find coordinate of the closet coastline
# e.g.,: Lat: 28.56367  Lon: -80.57163
# distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)
launch_site_lat = 28.563197
launch_site_lon = -80.576820
coastline_lat = 28.56334
coastline_lon = -80.56799
distance_coastline = calculate_distance(launch_site_lat,launch_site_lon,coastline_lat,coastline_lon)
# print(distance_coastline)
# 0.8627671182499878
# *TODO:* After obtained its coordinate, create a `folium.Marker` to show the distance
# Create and add a folium.Marker on your selected closest coastline point on the map
# Display the distance between coastline point and launch site using the icon property 
# for example
# distance_marker = folium.Marker(
#    coordinate,
#    icon=DivIcon(
#        icon_size=(20,20),
#        icon_anchor=(0,0),
#        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance),
#        )
#    )
coordinate = [coastline_lat,coastline_lon]
distance_marker = folium.Marker(coordinate, icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0),html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_coastline),))
site_map.add_child(distance_marker)

# *TODO:* Draw a `PolyLine` between a launch site to the selected coastline point
# Create a `folium.PolyLine` object using the coastline coordinates and launch site coordinate
# lines=folium.PolyLine(locations=coordinates, weight=1)
coordinates = [(launch_site_lat,launch_site_lon),(coastline_lat,coastline_lon)]
lines = folium.PolyLine(locations=coordinates, color='red',weight=1)
site_map.add_child(lines)
# *TODO:* Similarly, you can draw a line betwee a launch site to its closest city, railway, highway, etc. You need to use `MousePosition` to find the their coordinates on the map first



# Create a marker with distance to a closest city, railway, highway relative to CCAFS SLC-40
# Draw a line between the marker to the launch site
closest_highway = 28.56335, -80.57085
closest_railroad = 28.57206, -80.58525
closest_city = 28.10473, -80.64531

distance_highway = calculate_distance(launch_site_lat,launch_site_lon,closest_highway[0],closest_highway[1])
print('closest highway ',distance_highway)

distance_railroad = calculate_distance(launch_site_lat,launch_site_lon,closest_railroad[0],closest_railroad[1])
print('closest railroad ',distance_railroad)

distance_city = calculate_distance(launch_site_lat,launch_site_lon,closest_city[0],closest_city[1])
print('closest city ',distance_city)

highway_num = folium.Marker(closest_highway, icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0),html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_highway),))
site_map.add_child(highway_num)

coordinates = [(launch_site_lat,launch_site_lon),(closest_highway)]
lines = folium.PolyLine(locations=coordinates, color='green',weight=1)
site_map.add_child(lines)


# exit(0)
# display the map
site_map.save('site_map.html')
webbrowser.open('site_map.html')