# Lab 1: Collecting the data
## Import Libraries and Define Auxiliary Functions
# Requests allows us to make HTTP requests which we will use to get data from an API
import requests
# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Datetime is a library that allows us to represent dates
import datetime

# Setting this option will print all collumns of a dataframe
pd.set_option('display.max_columns', None)
# Setting this option will print all of the data in a feature
pd.set_option('display.max_colwidth', None)

# Below we will define a series of helper functions that will help us use the API to extract information using identification numbers in the launch data.

# From the <code>rocket</code> column we would like to learn the booster name.

# Takes the dataset and uses the rocket column to call the API and append the data to the list
def getBoosterVersion(data):
    for x in data['rocket']:
        if x:
            response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
            BoosterVersion.append(response['name'])

# From the <code>launchpad</code> we would like to know the name of the launch site being used, the logitude, and the latitude.
# Takes the dataset and uses the launchpad column to call the API and append the data to the list
def getLaunchSite(data):
    for x in data['launchpad']:
        if x:
            response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
            Longitude.append(response['longitude'])
            Latitude.append(response['latitude'])
            LaunchSite.append(response['name'])

# From the <code>payload</code> we would like to learn the mass of the payload and the orbit that it is going to.
# Takes the dataset and uses the payloads column to call the API and append the data to the lists
def getPayloadData(data):
    for load in  data['payloads']:
        if load:
            response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
            PayloadMass.append(response['mass_kg'])
            Orbit.append(response['orbit'])
# From <code>cores</code> we would like to learn the outcome of the landing, the type of the landing, number of flights with that core, whether gridfins were used, wheter the core is reused, wheter legs were used, the landing pad used, the block of the core which is a number used to seperate version of cores, the number of times this specific core has been reused, and the serial of the core.
# Takes the dataset and uses the cores column to call the API and append the data to the lists
def getCoreData(data):
    for core in data['cores']:
            if core['core'] != None:
                response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
                Block.append(response['block'])
                ReusedCount.append(response['reuse_count'])
                Serial.append(response['serial'])
            else:
                Block.append(None)
                ReusedCount.append(None)
                Serial.append(None)
            Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
            Flights.append(core['flight'])
            GridFins.append(core['gridfins'])
            Reused.append(core['reused'])
            Legs.append(core['legs'])
            LandingPad.append(core['landpad'])

# Now let's start requesting rocket launch data from SpaceX API with the following URL:
spacex_url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'

# spacex_url="https://api.spacexdata.com/v4/launches/past"
response = requests.get(spacex_url)
# print(response.status_code)

# Check the content of the response
# print(response.content)
# You should see the response contains massive information about SpaceX launches. Next, let's try to discover some more relevant information for this project.

# static_json_url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'

# We should see that the request was successfull with the 200 status response code

df = pd.json_normalize(response.json())
# print(df.head())

# You will notice that a lot of the data are IDs. For example the rocket column has no information about the rocket just an identification number.

# We will now use the API again to get information about the launches using the IDs given for each launch. Specifically we will be using columns <code>rocket</code>, <code>payloads</code>, <code>launchpad</code>, and <code>cores</code>.
# Lets take a subset of our dataframe keeping only the features we want and the flight number, and date_utc.
data = df[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]
# print(data.head())
#                     rocket  \
# 0  5e9d0d95eda69955f709d1eb   
# 1  5e9d0d95eda69955f709d1eb   
# 2  5e9d0d95eda69955f709d1eb   
# 3  5e9d0d95eda69955f709d1eb   
# 4  5e9d0d95eda69955f709d1eb   

#                                                payloads  \
# 0                            [5eb0e4b5b6c3bb0006eeb1e1]
# 1                            [5eb0e4b6b6c3bb0006eeb1e2]
# 2  [5eb0e4b6b6c3bb0006eeb1e3, 5eb0e4b6b6c3bb0006eeb1e4]
# 3                            [5eb0e4b7b6c3bb0006eeb1e5]
# 4                            [5eb0e4b7b6c3bb0006eeb1e6]

#                   launchpad  \
# 0  5e9e4502f5090995de566f86
# 1  5e9e4502f5090995de566f86
# 2  5e9e4502f5090995de566f86
# 3  5e9e4502f5090995de566f86
# 4  5e9e4502f5090995de566f86

                                                                                                                                                   
#                                            cores  \
# 0  [{'core': '5e9e289df35918033d3b2623', 'flight': 1, 'gridfins': False, 'legs': False, 'reused': False, 'landing_attempt': False, 'landing_success': None, 'landing_type': None, 'landpad': None}]
# 1  [{'core': '5e9e289ef35918416a3b2624', 'flight': 1, 'gridfins': False, 'legs': False, 'reused': False, 'landing_attempt': False, 'landing_success': None, 'landing_type': None, 'landpad': None}]
# 2  [{'core': '5e9e289ef3591814873b2625', 'flight': 1, 'gridfins': False, 'legs': False, 'reused': False, 'landing_attempt': False, 'landing_success': None, 'landing_type': None, 'landpad': None}]
# 3  [{'core': '5e9e289ef3591855dc3b2626', 'flight': 1, 'gridfins': False, 'legs': False, 'reused': False, 'landing_attempt': False, 'landing_success': None, 'landing_type': None, 'landpad': None}]
# 4  [{'core': '5e9e289ef359184f103b2627', 'flight': 1, 'gridfins': False, 'legs': False, 'reused': False, 'landing_attempt': False, 'landing_success': None, 'landing_type': None, 'landpad': None}]

#    flight_number                  date_utc
# 0              1  2006-03-24T22:30:00.000Z
# 1              2  2007-03-21T01:10:00.000Z
# 2              3  2008-08-03T03:34:00.000Z
# 3              4  2008-09-28T23:15:00.000Z
# 4              5  2009-07-13T03:35:00.000Z

# We will remove rows with multiple cores because those are falcon rockets with 2 extra rocket boosters and rows that have multiple payloads in a single rocket.
data = data[data['cores'].map(len) == 1]
data = data[data['payloads'].map(len) == 1]

# Since payloads and cores are lists of size 1 we will also extract the single value in the list and replace the feature.
data['cores'] = data['cores'].map(lambda x : x[0])
data['payloads'] = data['payloads'].map(lambda x : x[0])

# We also want to convert the date_utc to a datetime datatype and then extracting the date leaving the time
data['date'] = pd.to_datetime(data['date_utc']).dt.date

# Using the date we will restrict the dates of the launches
data = data[data['date'] <= datetime.date(2020, 11, 13)]
# print(data.head())
# * From the <code>rocket</code> we would like to learn the booster name

# * From the <code>payload</code> we would like to learn the mass of the payload and the orbit that it is going to

# * From the <code>launchpad</code> we would like to know the name of the launch site being used, the longitude, and the latitude.

# * From <code>cores</code> we would like to learn the outcome of the landing, the type of the landing, number of flights with that core, whether gridfins were used, whether the core is reused, whether legs were used, the landing pad used, the block of the core which is a number used to seperate version of cores, the number of times this specific core has been reused, and the serial of the core.

# The data from these requests will be stored in lists and will be used to create a new dataframe.
#Global variables 
BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []

# These functions will apply the outputs globally to the above variables. Let's take a looks at <code>BoosterVersion</code> variable. Before we apply  <code>getBoosterVersion</code> the list is empty:
# Now, let's apply <code> getBoosterVersion</code> function method to get the booster version
getBoosterVersion(data)
# Call getLaunchSite
getLaunchSite(data)
# Call getPayloadData
getPayloadData(data)
# Call getCoreData
getCoreData(data)

# Finally lets construct our dataset using the data we have obtained. We we combine the columns into a dictionary.

launch_dict = {'FlightNumber': list(data['flight_number']),
'Date': list(data['date']),
'BoosterVersion':BoosterVersion,
'PayloadMass':PayloadMass,
'Orbit':Orbit,
'LaunchSite':LaunchSite,
'Outcome':Outcome,
'Flights':Flights,
'GridFins':GridFins,
'Reused':Reused,
'Legs':Legs,
'LandingPad':LandingPad,
'Block':Block,
'ReusedCount':ReusedCount,
'Serial':Serial,
'Longitude': Longitude,
'Latitude': Latitude}

df = pd.DataFrame(launch_dict)
# print(df.describe())
#       FlightNumber   PayloadMass    Flights      Block  ReusedCount  \
# count     94.000000     88.000000  94.000000  90.000000    94.000000
# mean      54.202128   5919.165341   1.755319   3.500000     3.053191
# std       30.589048   4909.689575   1.197544   1.595288     4.153938
# min        1.000000     20.000000   1.000000   1.000000     0.000000
# 25%       28.250000   2406.250000   1.000000   2.000000     0.000000
# 50%       52.500000   4414.000000   1.000000   4.000000     1.000000
# 75%       81.500000   9543.750000   2.000000   5.000000     4.000000
# max      106.000000  15600.000000   6.000000   5.000000    13.000000

#         Longitude   Latitude
# count   94.000000  94.000000
# mean   -75.553302  28.581782
# std     53.391880   4.639981
# min   -120.610829   9.047721
# 25%    -80.603956  28.561857
# 50%    -80.577366  28.561857
# 75%    -80.577366  28.608058
# max    167.743129  34.632093

df = df[df['BoosterVersion'] != 'Falcon 1']
data_falcon9 = df.copy()
# A value is trying to be set on a copy of a slice from a DataFrame.
# Try using .loc[row_indexer,col_indexer] = value instead
data_falcon9.loc[:,'FlightNumber'] = list(range(1, data_falcon9.shape[0]+1))
# print(data_falcon9[0:5])



# See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
#   isetter(ilocs[0], value)
#    FlightNumber        Date BoosterVersion  PayloadMass Orbit    LaunchSite  \
# 4             1  2010-06-04       Falcon 9          NaN   LEO  CCSFS SLC 40
# 5             2  2012-05-22       Falcon 9        525.0   LEO  CCSFS SLC 40
# 6             3  2013-03-01       Falcon 9        677.0   ISS  CCSFS SLC 40
# 7             4  2013-09-29       Falcon 9        500.0    PO   VAFB SLC 4E
# 8             5  2013-12-03       Falcon 9       3170.0   GTO  CCSFS SLC 40

#        Outcome  Flights  GridFins  Reused   Legs LandingPad  Block  \
# 4    None None        1     False   False  False       None    1.0
# 5    None None        1     False   False  False       None    1.0
# 6    None None        1     False   False  False       None    1.0
# 7  False Ocean        1     False   False  False       None    1.0
# 8    None None        1     False   False  False       None    1.0

#    ReusedCount Serial   Longitude   Latitude
# 4            0  B0003  -80.577366  28.561857
# 5            0  B0005  -80.577366  28.561857
# 6            0  B0007  -80.577366  28.561857
# 7            0  B1003 -120.610829  34.632093
# 8            0  B1004  -80.577366  28.561857
print(data_falcon9.isnull().sum())
# lightNumber       0
# Date               0
# BoosterVersion     0
# PayloadMass        5
# Orbit              0
# LaunchSite         0
# Outcome            0
# Flights            0
# GridFins           0
# Reused             0
# Legs               0
# LandingPad        26
# Block              0
# ReusedCount        0
# Serial             0
# Longitude          0
# Latitude           0
# Calculate below the mean for the <code>PayloadMass</code> using the <code>.mean()</code>. Then use the mean and the <code>.replace()</code> function to replace `np.nan` values in the data with the mean you calculated.

# Calculate the mean value of PayloadMass column
meanValue = data_falcon9['PayloadMass'].mean()
data_falcon9['PayloadMass'] = data_falcon9['PayloadMass'].fillna(meanValue)

# Now we should have no missing values in our dataset except for in <code>LandingPad</code>.
data_falcon9 = data_falcon9.dropna(subset=['LandingPad'])

data_falcon9.to_csv('falcon9_nona_dataset_part_1.csv', index=False)