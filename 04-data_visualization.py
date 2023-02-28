# andas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns

df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")

# If you were unable to complete the previous lab correctly you can uncomment and load this csv

# df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/dataset_part_2.csv')

# print(df.head(5))
#   FlightNumber        Date BoosterVersion  PayloadMass Orbit  ... ReusedCount Serial   Longitude   Latitude  Class
# 0             1  2010-06-04       Falcon 9  6104.959412   LEO  ...           0  B0003  -80.577366  28.561857      0
# 1             2  2012-05-22       Falcon 9   525.000000   LEO  ...           0  B0005  -80.577366  28.561857      0
# 2             3  2013-03-01       Falcon 9   677.000000   ISS  ...           0  B0007  -80.577366  28.561857      0
# 3             4  2013-09-29       Falcon 9   500.000000    PO  ...           0  B1003 -120.610829  34.632093      0
# 4             5  2013-12-03       Falcon 9  3170.000000   GTO  ...           0  B1004  -80.577366  28.561857      0
# First, let's try to see how the `FlightNumber` (indicating the continuous launch attempts.) and `Payload` variables would affect the launch outcome.

# We can plot out the <code>FlightNumber</code> vs. <code>PayloadMass</code>and overlay the outcome of the launch. We see that as the flight number increases, the first stage is more likely to land successfully. The payload mass is also important; it seems the more massive the payload, the less likely the first stage will return.
sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect = 5)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Pay load Mass (kg)",fontsize=20)
plt.show()

# We see that different launch sites have different success rates.  <code>CCAFS LC-40</code>, has a success rate of 60 %, while  <code>KSC LC-39A</code> and <code>VAFB SLC 4E</code> has a success rate of 77%.


# Next, let's drill down to each site visualize its detailed launch records.
### TASK 1: Visualize the relationship between Flight Number and Launch Site
# Use the function <code>catplot</code> to plot <code>FlightNumber</code> vs <code>LaunchSite</code>, set the  parameter <code>x</code>  parameter to <code>FlightNumber</code>,set the  <code>y</code> to <code>Launch Site</code> and set the parameter <code>hue</code> to <code>'class'</code>

sns.catplot(y="LaunchSite", x="FlightNumber", hue="Class", data=df, aspect = 5)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Launch Site",fontsize=20)
plt.show()


# Now try to explain the patterns you found in the Flight Number vs. Launch Site scatter point plots.

### TASK 2: Visualize the relationship between Payload and Launch Site
# We also want to observe if there is any relationship between launch sites and their payload mass.

sns.catplot(y="LaunchSite", x="PayloadMass", hue="Class", data=df, aspect = 5)
plt.xlabel("Pay Load Mass (kg)",fontsize=20)
plt.ylabel("Launch Site",fontsize=20)
plt.show()

# Now if you observe Payload Vs. Launch Site scatter point chart you will find for the VAFB-SLC  launchsite there are no  rockets  launched for  heavypayload mass(greater than 10000).


### TASK  3: Visualize the relationship between success rate of each orbit type
# Next, we want to visually check if there are any relationship between success rate and orbit type.

# Let's create a `bar chart` for the sucess rate of each orbit
# HINT use groupby method on Orbit column and get the mean of Class column

bar_data = df.groupby(['Orbit'])['Class'].mean().reset_index()

sns.barplot(y="Class", x="Orbit", data=bar_data)
plt.xlabel("Orbit",fontsize=20)
plt.ylabel("Class",fontsize=20)
plt.show()

# Analyze the ploted bar chart try to find which orbits have high sucess rate.


### TASK  4: Visualize the relationship between FlightNumber and Orbit type

# For each orbit, we want to see if there is any relationship between FlightNumber and Orbit type.

sns.catplot(y="Orbit", x="FlightNumber", hue="Class", data=df)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Orbit",fontsize=20)
plt.show()

# # Create the scatter plot
sns.scatterplot(x='FlightNumber', y='Orbit', hue='Class', data=df)

# Show the plot
plt.show()

# Trong seaborn, scatterplot và catplot là hai kiểu đồ thị khác nhau dùng để trực quan hóa dữ liệu.

# Scatterplot là một biểu đồ tần suất dùng để trực quan hóa mối quan hệ giữa hai biến. Trong một scatterplot, mỗi điểm dữ liệu sẽ được biểu thị bằng một điểm trên biểu đồ. Trong scatterplot, ta có thể sử dụng màu sắc, kích thước hoặc dấu hiệu để biểu thị thêm thông tin về dữ liệu.

# Catplot là một loại biểu đồ tần suất dùng để trực quan hóa dữ liệu liên quan đến nhiều biến. Trong catplot, ta có thể sử dụng các biến phụ để biểu thị thêm thông tin về dữ liệu. Catplot có thể sử dụng các kiểu biểu đồ khác nhau như biểu đồ tròn, biểu đồ cột, biểu đồ đường vv.

# Trong tổng quan, scatterplot thích hợp nếu bạn muốn trực quan hóa mối quan hệ giữa hai biến, trong khi catplot thích hợp nếu bạn muốn trực quan hóa dữ liệu liên quan đến nhiều biến.


# You should see that in the LEO orbit the Success appears related to the number of flights; on the other hand, there seems to be no relationship between flight number when in GTO orbit.


### TASK  5: Visualize the relationship between Payload and Orbit type
# Similarly, we can plot the Payload vs. Orbit scatter point charts to reveal the relationship between Payload and Orbit type
# Plot a scatter point chart with x axis to be Payload and y axis to be the Orbit, and hue to be the class value

sns.catplot(y="Orbit", x="PayloadMass", hue="Class", data=df)
plt.xlabel("PayloadMass",fontsize=20)
plt.ylabel("Orbit",fontsize=20)
plt.show()

# With heavy payloads the successful landing or positive landing rate are more for Polar,LEO and ISS.

# However for GTO we cannot distinguish this well as both positive landing rate and negative landing(unsuccessful mission) are both there here.


### TASK  6: Visualize the launch success yearly trend
# You can plot a line chart with x axis to be <code>Year</code> and y axis to be average success rate, to get the average launch success trend.

# The function will help you get the year from the date:
year=[]
def Extract_year(date):
    for i in df["Date"]:
        year.append(i.split("-")[0])
    return year
    
Extract_year(0)
df["Year"] = year

average_df = df.groupby(by="Year").mean()
average_df.reset_index(inplace=True)
# print(average_df)


# Plot a line chart with x axis to be the extracted year and y axis to be the success rate
# Option 1:
# sns.lineplot(data=df, x="Year", y="Class")
# plt.xlabel("Year",fontsize=20)
# plt.ylabel("Success Rate",fontsize=20)
# plt.show()

# Option 3


# Plot a line chart with x axis to be the extracted year and y axis to be the success rate
# plt.plot(average_df["Year"],average_df["Class"])
# plt.xlabel("Year")
# plt.ylabel("Success/Failure")
# plt.show()



# Option 2
sns.lineplot(data=average_df, x="Year", y="Class")
plt.xlabel("Year",fontsize=20)
plt.ylabel("Success Rate",fontsize=20)
plt.show()



# you can observe that the sucess rate since 2013 kept increasing till 2020
## Features Engineering
# By now, you should obtain some preliminary insights about how each important variable would affect the success rate, we will select the features that will be used in success prediction in the future module.

features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
# print(features.head())
#    FlightNumber  PayloadMass Orbit    LaunchSite  Flights  GridFins  Reused   Legs LandingPad  Block  ReusedCount Serial
# 0             1  6104.959412   LEO  CCAFS SLC 40        1     False   False  False        NaN    1.0            0  B0003
# 1             2   525.000000   LEO  CCAFS SLC 40        1     False   False  False        NaN    1.0            0  B0005
# 2             3   677.000000   ISS  CCAFS SLC 40        1     False   False  False        NaN    1.0            0  B0007
# 3             4   500.000000    PO   VAFB SLC 4E        1     False   False  False        NaN    1.0            0  B1003
# 4             5  3170.000000   GTO  CCAFS SLC 40        1     False   False  False        NaN    1.0            0  B1004

### TASK  7: Create dummy variables to categorical columns
# Use the function <code>get_dummies</code> and <code>features</code> dataframe to apply OneHotEncoder to the column <code>Orbits</code>, <code>LaunchSite</code>, <code>LandingPad</code>, and <code>Serial</code>. Assign the value to the variable <code>features_one_hot</code>, display the results using the method head. Your result dataframe must include all features including the encoded ones.
# HINT: Use get_dummies() function on the categorical columns
categorical_columns = ['Orbit','LaunchSite','LandingPad','Serial']
features_one_hot = pd.get_dummies(features,columns=categorical_columns,prefix=categorical_columns)
print(features_one_hot.head())
#    FlightNumber  PayloadMass  Flights  GridFins  Reused  ...  Serial_B1056  Serial_B1058  Serial_B1059  Serial_B1060  Serial_B1062
# 0             1  6104.959412        1     False   False  ...             0             0             0             0             0
# 1             2   525.000000        1     False   False  ...             0             0             0             0             0
# 2             3   677.000000        1     False   False  ...             0             0             0             0             0
# 3             4   500.000000        1     False   False  ...             0             0             0             0             0
# 4             5  3170.000000        1     False   False  ...             0             0             0             0             0

# [5 rows x 80 columns]

### TASK  8: Cast all numeric columns to `float64`

# Now that our <code>features_one_hot</code> dataframe only contains numbers cast the entire dataframe to variable type <code>float64</code>


# HINT: use astype function
# features_one_hot = features_one_hot.astype('float64')

features_one_hot.astype('float64')
# We can now export it to a <b>CSV</b> for the next section,but to make the answers consistent, in the next lab we will provide data in a pre-selected date range.
features_one_hot.to_csv('dataset_part_3.csv', index=False)


