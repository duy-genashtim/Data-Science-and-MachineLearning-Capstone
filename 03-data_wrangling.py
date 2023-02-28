# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np

### Data Analysis
# Load Space X dataset, from last section.
df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")
# Identify and calculate the percentage of the missing values in each attribute
# print(df.isnull().sum()/df.count()*100)
# FlightNumber       0.000
# Date               0.000
# BoosterVersion     0.000
# PayloadMass        0.000
# Orbit              0.000
# LaunchSite         0.000
# Outcome            0.000
# Flights            0.000
# GridFins           0.000
# Reused             0.000
# Legs               0.000
# LandingPad        40.625
# Block              0.000
# ReusedCount        0.000
# Serial             0.000
# Longitude          0.000
# Latitude           0.000
# print(df.dtypes)
# FlightNumber        int64
# Date               object
# BoosterVersion     object
# PayloadMass       float64
# Orbit              object
# LaunchSite         object
# Outcome            object
# Flights             int64
# GridFins             bool
# Reused               bool
# Legs                 bool
# LandingPad         object
# Block             float64
# ReusedCount         int64
# Serial             object
# Longitude         float64
# Latitude          float64
# dtype: object


# The data contains several Space X  launch facilities: <a href='https://en.wikipedia.org/wiki/List_of_Cape_Canaveral_and_Merritt_Island_launch_sites?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork26802033-2022-01-01'>Cape Canaveral Space</a> Launch Complex 40  <b>VAFB SLC 4E </b> , Vandenberg Air Force Base Space Launch Complex 4E <b>(SLC-4E)</b>, Kennedy Space Center Launch Complex 39A <b>KSC LC 39A </b>.The location of each Launch Is placed in the column <code>LaunchSite</code>

### TASK 1: Calculate the number of launches on each site

# Next, let's see the number of launches for each site.

# Use the method  <code>value_counts()</code> on the column <code>LaunchSite</code> to determine the number of launches  on each site:

# Apply value_counts() on column LaunchSite
print(df['LaunchSite'].value_counts())
# CCAFS SLC 40    55
# KSC LC 39A      22
# VAFB SLC 4E     13


### TASK 2: Calculate the number and occurrence of each orbit
# Use the method  <code>.value_counts()</code> to determine the number and occurrence of each orbit in the  column <code>Orbit</code>

print(df['Orbit'].value_counts())
# GTO      27
# ISS      21
# VLEO     14
# PO        9
# LEO       7
# SSO       5
# MEO       3
# SO        1
# GEO       1
# ES-L1     1
# HEO       1

### TASK 3: Calculate the number and occurence of mission outcome per orbit type
# Use the method <code>.value_counts()</code> on the column <code>Outcome</code> to determine the number of <code>landing_outcomes</code>.Then assign it to a variable landing_outcomes.
landing_outcomes = df['Outcome'].value_counts()
# print(landing_outcomes)
# True ASDS      41
# None None      19
# True RTLS      14
# False ASDS      6
# True Ocean      5
# None ASDS       2
# False Ocean     2
# False RTLS      1

# <code>True Ocean</code> means the mission outcome was successfully  landed to a specific region of the ocean while <code>False Ocean</code> means the mission outcome was unsuccessfully landed to a specific region of the ocean. <code>True RTLS</code> means the mission outcome was successfully  landed to a ground pad <code>False RTLS</code> means the mission outcome was unsuccessfully landed to a ground pad.<code>True ASDS</code> means the mission outcome was successfully  landed to a drone ship <code>False ASDS</code> means the mission outcome was unsuccessfully landed to a drone ship. <code>None ASDS</code> and <code>None None</code> these represent a failure to land.
# for i, outcome in enumerate(landing_outcomes.keys()):
#      print(i,outcome)
# 0 True ASDS
# 1 None None
# 2 True RTLS
# 3 False ASDS
# 4 True Ocean
# 5 False Ocean
# 6 None ASDS
# 7 False RTLS

# We create a set of outcomes where the second stage did not land successfully:
bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])
# print(bad_outcomes)
# {'False Ocean', 'None None', 'False ASDS', 'False RTLS', 'None ASDS'}

### TASK 4: Create a landing outcome label from Outcome column
# Using the <code>Outcome</code>,  create a list where the element is zero if the corresponding  row  in  <code>Outcome</code> is in the set <code>bad_outcome</code>; otherwise, it's one. Then assign it to the variable <code>landing_class</code>:
# landing_class = []
# for outcome in df['Outcome']:
#     if outcome in bad_outcomes:
#         landing_class.append(0)
#     else:
#         landing_class.append(1)
landing_class = [0 if x in bad_outcomes else 1 for x in df['Outcome']]
# print(landing_class)
df['Class']=landing_class
# print(df[['Class']].head(8))
#    Class
# 0      0
# 1      0
# 2      0
# 3      0
# 4      0
# 5      0
# 6      1
# 7      1

# We can use the following line of code to determine  the success rate:
print(df["Class"].mean())
df.to_csv("dataset_part_2.csv", index=False)