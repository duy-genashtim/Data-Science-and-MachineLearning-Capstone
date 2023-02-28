import pandas as pd
import sqlite3

# Read the CSV data from the link
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv"
df = pd.read_csv(url)

# Connect to the database
conn = sqlite3.connect("mydatabase_spacex.db")

# Write the DataFrame to the database
df.to_sql("SPACEX", conn, if_exists="replace", index=False)

# ### Task 1

##### Display the names of the unique launch sites  in the space missionRead all the data from the database
query = "SELECT DISTINCT(Launch_Site) FROM SPACEX;"
# Execute query by the end of the file
#     Launch_Site
# 0   CCAFS LC-40
# 1   VAFB SLC-4E
# 2    KSC LC-39A
# 3  CCAFS SLC-40
### Task 2

##### Display 5 records where launch sites begin with the string 'KSC'
query = 'SELECT * FROM SPACEX WHERE "Launch_Site" LIKE "KSC%" LIMIT 5;'
# Execute query by the end of the file

#          Date Time (UTC) Booster_Version Launch_Site  ...      Orbit    Customer Mission_Outcome      Landing _Outcome
# 0  19-02-2017   14:39:00   F9 FT B1031.1  KSC LC-39A  ...  LEO (ISS)  NASA (CRS)         Success  Success (ground pad)
# 1  16-03-2017   06:00:00     F9 FT B1030  KSC LC-39A  ...        GTO    EchoStar         Success            No attempt
# 2  30-03-2017   22:27:00  F9 FT  B1021.2  KSC LC-39A  ...        GTO         SES         Success  Success (drone ship)
# 3  01-05-2017   11:15:00   F9 FT B1032.1  KSC LC-39A  ...        LEO         NRO         Success  Success (ground pad)
# 4  15-05-2017   23:21:00     F9 FT B1034  KSC LC-39A  ...        GTO    Inmarsat         Success            No attempt

### Task 3

##### Display the total payload mass carried by boosters launched by NASA (CRS)

query = 'SELECT SUM(PAYLOAD_MASS__KG_) FROM SPACEX WHERE "Customer" = "NASA (CRS)";'
# Execute query by the end of the file

#    SUM(PAYLOAD_MASS__KG_)
# 0                   45596

### Task 4

##### Display average payload mass carried by booster version F9 v1.1

query = 'SELECT AVG(PAYLOAD_MASS__KG_) FROM SPACEX WHERE "Booster_Version" = "F9 v1.1";'
# Execute query by the end of the file

#    AVG(PAYLOAD_MASS__KG_)
# 0                  2928.4


### Task 5

##### List the date where the succesful landing outcome in drone ship was acheived.

# *Hint:Use min function*

query = 'SELECT MIN(DATE) FROM SPACEX WHERE "Landing _Outcome" = "Success (drone ship)";'
#     MIN(DATE)
# 0  06-05-2016


### Task 6

##### List the names of the boosters which have success in ground pad  and have payload mass greater than 4000 but less than 6000

query = 'SELECT "Booster_Version" FROM SPACEX WHERE "Landing _Outcome" = "Success (ground pad)" AND "PAYLOAD_MASS__KG_" BETWEEN 4000 AND 6000;'
# Execute query by the end of the file

#   Booster_Version
# 0   F9 FT B1032.1
# 1   F9 B4 B1040.1
# 2   F9 B4 B1043.1

query = 'SELECT "Booster_Version" FROM SPACEX WHERE "Landing _Outcome" = "Success (drone ship)" AND "PAYLOAD_MASS__KG_" BETWEEN 4000 AND 6000;'
# Execute query by the end of the file

#   Booster_Version
# 0     F9 FT B1022
# 1     F9 FT B1026
# 2  F9 FT  B1021.2
# 3  F9 FT  B1031.2

### Task 7

##### List the total number of successful and failure mission outcomes

query = 'SELECT "Mission_Outcome", COUNT(*) FROM SPACEX GROUP BY "Mission_Outcome"'
# Execute query by the end of the file

#                     Mission_Outcome  COUNT(*)
# 0               Failure (in flight)         1
# 1                           Success        98
# 2                          Success          1
# 3  Success (payload status unclear)         1

### Task 8

##### List the   names of the booster_versions which have carried the maximum payload mass. Use a subquery

query = 'SELECT "Booster_Version","PAYLOAD_MASS__KG_"  FROM SPACEX WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEX )'
# Execute query by the end of the file

#   Booster_Version  PAYLOAD_MASS__KG_
# 0    F9 B5 B1048.4              15600
# 1    F9 B5 B1049.4              15600
# 2    F9 B5 B1051.3              15600
# 3    F9 B5 B1056.4              15600
# 4    F9 B5 B1048.5              15600
# 5    F9 B5 B1051.4              15600
# 6    F9 B5 B1049.5              15600
# 7   F9 B5 B1060.2               15600
# 8   F9 B5 B1058.3               15600
# 9    F9 B5 B1051.6              15600
# 10   F9 B5 B1060.3              15600
# 11  F9 B5 B1049.7               15600

### Task 9

##### List the records which will display the month names, succesful landing_outcomes in ground pad ,booster versions, launch_site for the months in year 2017

# **Note: SQLLite does not support monthnames. So you need to use  substr(Date, 4, 2) as month to get the months and substr(Date,7,4)='2017' for year.**

query = 'SELECT substr(Date, 4, 2) as month,"Landing _Outcome", "Booster_Version","Launch_Site"  FROM SPACEX WHERE "Landing _Outcome" = "Success (ground pad)" AND substr(Date,7,4)="2017"'
# Execute query by the end of the file

#   month      Landing _Outcome Booster_Version   Launch_Site
# 0    02  Success (ground pad)   F9 FT B1031.1    KSC LC-39A
# 1    05  Success (ground pad)   F9 FT B1032.1    KSC LC-39A
# 2    06  Success (ground pad)   F9 FT B1035.1    KSC LC-39A
# 3    08  Success (ground pad)   F9 B4 B1039.1    KSC LC-39A
# 4    09  Success (ground pad)   F9 B4 B1040.1    KSC LC-39A
# 5    12  Success (ground pad)  F9 FT  B1035.2  CCAFS SLC-40

### Task 10

##### Rank the  count of  successful landing_outcomes between the date  04-06-2010 and 20-03-2017 in descending order.

query = 'SELECT "Landing _Outcome",COUNT(*) AS qty FROM SPACEX WHERE "Landing _Outcome" LIKE "Success%" AND DATE BETWEEN "04-06-2010" AND "20-03-2017" GROUP BY "Landing _Outcome" ORDER BY qty DESC'
# Execute query by the end of the file

#        Landing _Outcome  qty
# 0               Success   20
# 1  Success (drone ship)    8
# 2  Success (ground pad)    6


# Change query here to check the result
df = pd.read_sql_query(query, conn)


# # Read all the data from the database
# query = "SELECT * FROM SPACEX"

# df = pd.read_sql_query(query, conn)


# Print the data
print(df)

# Close the connection
conn.close()
