#!/usr/bin/env python
# coding: utf-8

# # WeatherPy
# ----
# 
# #### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[2]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
from scipy import stats
from scipy.stats import linregress
from pprint import pprint
import scipy.stats as st

# Import API key
from api_keys import weather_api_key

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

units = "metric"

# Output File (CSV)
output_data_file = "../output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)


# In[2]:


data = pd.read_csv(output_data_file)
data.head()


# ## Generate Cities List

# In[3]:


# List for holding lat_lngs and cities
lat_lngs = []

cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(lat_range[0], lat_range[1], size=1500)
lngs = np.random.uniform(lng_range[0], lng_range[1], size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
len(cities)


# In[5]:


cities


# In[5]:


# check if the url is sufficient: 
url = "http://api.openweathermap.org/data/2.5/weather"
city_url = url + "?q=" + "Irvine" + "&appid=" + weather_api_key + "&units=" + units
cities_collection = requests.get(city_url).json()
pprint(cities_collection)


# ### Perform API Calls
# * Perform a weather check on each city using a series of successive API calls.
# * Include a print log of each city as it'sbeing processed (with the city number and city name).
# 
# > **HINT:** The OpenWeatherMap API only allows 60 calls per minute under their free plan. Try using `time.sleep(60)` after each set of 50 cities to avoid API errors due to large calls.

# In[6]:


# API set up
cities_info = []
#base_url = "https://openweathermap.org/api/&key=" + weather_api_key
url = "http://api.openweathermap.org/data/2.5/weather"
#query = cities

# to help python count every row in the cities (one by one)
records = 1 
sets = 1 

# enumerate is for loop function  when we need to look for many interables here (lats|lngs|temp|humid...)
# set is to plit down the 620 cities into smaller group of 10 or 20
# we use two interables i, city , so we need to do enumerate function
for i, city in enumerate(cities):
    # if here: we want to split out the looking interables into every 20 rows per count-round and i>=20 that mean 
    # the next 20 rows we put to next looking after 15 seconds break
    if (i % 20 == 0 and i >= 20):
        sets += 1
        records = 0
        print("End of set. Sleeping for 15 seconds.")
        time.sleep(15)
    # create url for each city 
    city_url = url + "?q=" + city + "&appid=" + weather_api_key + "&units=" + units
    #print(city_url)
    records += 1
    try:
        cities_collection = requests.get(city_url).json()
        lats = cities_collection["coord"]["lat"]
        longs = cities_collection["coord"]["lon"]
        temperature = cities_collection["main"]["temp"]
        temp_max = cities_collection["main"]["temp_max"]
        humidity = cities_collection["main"]["humidity"]
        cloudiness = cities_collection["clouds"]["all"]
        wind_speed = cities_collection["wind"]["speed"]
        date = cities_collection["dt"]
        country = cities_collection['sys']['country']
        
        cities_info.append({"city": city,
                           "latitutes": lats,
                            "longtitudes": longs,
                            "temperature (F)": temperature,
                            "Temp_max (F)":temp_max,
                            "humidity": humidity,
                            "cloudiness": cloudiness,
                            "wind speed": wind_speed,
                            "date": date,
                            "country": country
                           })
        
    except:
        print('city error: not found, skipping')
        pass
print('----information all collected-----')
#print(cities_collection)


# In[7]:


# check how many cities were found and print out the cities data
len(cities_info)
pprint(cities_info)


# ### Convert Raw Data to DataFrame
# * Export the city data into a .csv.
# * Display the DataFrame

# In[4]:


# convert the cities_info into a dataframe
weather_data = pd.DataFrame(cities_info)
weather_data.head(20)


# In[10]:


#pprint(cities_collection)


# In[3]:


# export city data into csv file: 
weather_data.to_csv("../Output_data/weather_data.csv", index=False, header=True)


# In[5]:


# open csv file to avoid taking long time running above codes
weather_data_path = "../output_data/weather_data.csv"
weather_df = pd.read_csv(weather_data_path)
weather_df.head()


# ## Inspect the data and remove the cities where the humidity > 100%.
# ----
# Skip this step if there are no cities that have humidity > 100%. 

# In[12]:


# check if there is any cities with humidity > 100 
humid_100 = weather_df.loc[weather_df["humidity"]>100]
len(humid_100)

# the len function show that: 0 city has humidity >100, so, we skip to next step


# In[13]:


#  Get the indices of cities that have humidity over 100%.


# In[14]:


# Make a new DataFrame equal to the city data to drop all humidity outliers by index.
# Passing "inplace=False" will make a copy of the city_data DataFrame, which we call "clean_city_data".


# ## Plotting the Data
# * Use proper labeling of the plots using plot titles (including date of analysis) and axes labels.
# * Save the plotted figures as .pngs.

# In[15]:


# please refer to the separate pdf file for my analysis on all those factors


# ## Latitude vs. Temperature Plot

# In[48]:


plt.scatter(weather_df["latitutes"], weather_df["temperature (F)"], marker="o")

# Incorporate the other graph properties
plt.title("Temperature in World 571 Cities")
plt.ylabel("Temperature (C)")
plt.xlabel("Latitude")
plt.grid(True)

# Save the figure
plt.savefig("../output_data/TemperatureInWorld_571_Cities.png")

correlation = st.pearsonr(weather_df["latitutes"],weather_df["temperature (F)"])
print(f" the correlation bt Latitudes and Temperature is : {correlation}")

# Show plot
plt.show()


# ## Latitude vs. Humidity Plot

# In[20]:


plt.scatter(weather_df["latitutes"], weather_df["humidity"], marker="o")

# Incorporate the other graph properties
plt.title("Humidity in World 571 Cities")
plt.ylabel("Humidity")
plt.xlabel("Latitude")
plt.grid(True)

# Save the figure
plt.savefig("HumidityInWorld_571_Cities.png")

# Show plot
plt.show()
correlation = st.pearsonr(weather_df["latitutes"],weather_df["humidity"])
print(f" the correlation bt Latitudes and Humidity is : {correlation}")


# ## Latitude vs. Cloudiness Plot

# In[21]:


plt.scatter(weather_df["latitutes"], weather_df["cloudiness"], marker="o")

# Incorporate the other graph properties
plt.title("Cloudiness in World 571 Cities")
plt.ylabel("Cloudiness")
plt.xlabel("Latitude")
plt.grid(True)

# Save the figure
plt.savefig("CloudinessInWorld_571_Cities.png")

# Show plot
plt.show()
correlation = st.pearsonr(weather_df["latitutes"],weather_df["cloudiness"])
print(f" the correlation bt Latitudes and Cloudiness is : {correlation}")


# ## Latitude vs. Wind Speed Plot

# In[22]:


plt.scatter(weather_df["latitutes"], weather_df["wind speed"], marker="o")

# Incorporate the other graph properties
plt.title("Wind Speed (mph) in World 571 Cities")
plt.ylabel("Win_speed (mph)")
plt.xlabel("Latitude")
plt.grid(True)

# Save the figure
plt.savefig("Win_speed_InWorld_571_Cities.png")

# Show plot
plt.show()
correlation = st.pearsonr(weather_df["latitutes"],weather_df["wind speed"])
print(f" the correlation bt Latitudes and Wind speed is : {correlation}")


# ## Linear Regression

# In[7]:


# Northern Hemisphere | Southern Hemisphere | Max temp | Latitudes | Humid | Cloudiness | wind_speed 
North = weather_df.loc[weather_df["latitutes"]>=0]
North.head()
North.to_csv("../Output_data/North_data.csv", index=False, header=True)


# In[8]:


South = weather_df.loc[weather_df["latitutes"]<=0]
South.head()
South.to_csv("../Output_data/South_data.csv", index=False, header=True)


# ####  Northern Hemisphere - Max Temp vs. Latitude Linear Regression

# In[30]:


lats = North.iloc[:,1]
temp_max = North.iloc[:,4]
plt.scatter(lats,temp_max)
plt.grid()
plt.xlabel('Latitudes')
plt.ylabel('Max Temperature (F)')

(slope, intercept, rvalue, pvalue, stderr) = linregress(lats, temp_max)
regress_values = lats * slope + intercept
plt.plot(lats,regress_values,"r-")

line_eq = "y = " + str(round(slope,2)) + "x +" + str(round(intercept,2))
plt.annotate(line_eq,(0,-38),fontsize=12,color="red")
plt.show()


# ####  Southern Hemisphere - Max Temp vs. Latitude Linear Regression

# In[11]:


slats = South.iloc[:,1]
stemp_max = South.iloc[:,4]
plt.scatter(slats,stemp_max)
plt.grid()
plt.xlabel('Latitudes')
plt.ylabel('Max Temperature (F)')

(slope, intercept, rvalue, pvalue, stderr) = linregress(slats, stemp_max)
regress_values = slats * slope + intercept
plt.plot(slats,regress_values,"r-")
line_eq = "y = " + str(round(slope,2)) + "x +" + str(round(intercept,2))
plt.annotate(line_eq,(-57,32),fontsize=12,color="red")
plt.show()


# In[13]:


correlationS = st.pearsonr(South["latitutes"],stemp_max)
print(correlationS)


# ####  Northern Hemisphere - Humidity (%) vs. Latitude Linear Regression

# In[35]:


lats = North.iloc[:,1]
humid = North.iloc[:,5]
plt.scatter(lats,humid)
plt.grid()
plt.xlabel('Latitudes')
plt.ylabel('Humidity (%')

(slope, intercept, rvalue, pvalue, stderr) = linregress(lats, humid)
regress_values = lats * slope + intercept
plt.plot(lats,regress_values,"r-")

line_eq = "y = " + str(round(slope,2)) + "x +" + str(round(intercept,2))
plt.annotate(line_eq,(50,20),fontsize=12,color="red")
plt.show()


# ####  Southern Hemisphere - Humidity (%) vs. Latitude Linear Regression

# In[36]:


slats = South.iloc[:,1]
shumid = South.iloc[:,5]
plt.scatter(slats,shumid)
plt.grid()
plt.xlabel('Latitudes')
plt.ylabel('Humidity (%)')

(slope, intercept, rvalue, pvalue, stderr) = linregress(slats, shumid)
regress_values = slats * slope + intercept
plt.plot(slats,regress_values,"r-")

line_eq = "y = " + str(round(slope,2)) + "x +" + str(round(intercept,2))
plt.annotate(line_eq,(-20,20),fontsize=12,color="red")
plt.show()


# ####  Northern Hemisphere - Cloudiness (%) vs. Latitude Linear Regression

# In[37]:


lats = North.iloc[:,1]
cloud = North.iloc[:,6]
plt.scatter(lats,cloud)
plt.grid()
plt.xlabel('Latitudes')
plt.ylabel('Cloudiness (%)')

(slope, intercept, rvalue, pvalue, stderr) = linregress(lats, cloud)
regress_values = lats * slope + intercept
plt.plot(lats,regress_values,"r-")

line_eq = "y = " + str(round(slope,2)) + "x +" + str(round(intercept,2))
plt.annotate(line_eq,(30,40),fontsize=12,color="red")
plt.show()


# ####  Southern Hemisphere - Cloudiness (%) vs. Latitude Linear Regression

# In[38]:


slats = South.iloc[:,1]
scloud = South.iloc[:,6]
plt.scatter(slats,scloud)
plt.grid()
plt.xlabel('Latitudes')
plt.ylabel('Cloudiness (%)')

(slope, intercept, rvalue, pvalue, stderr) = linregress(slats, scloud)
regress_values = slats * slope + intercept
plt.plot(slats,regress_values,"r-")

line_eq = "y = " + str(round(slope,2)) + "x +" + str(round(intercept,2))
plt.annotate(line_eq,(-55,50),fontsize=12,color="red")
plt.show()


# ####  Northern Hemisphere - Wind Speed (mph) vs. Latitude Linear Regression

# In[39]:


lats = North.iloc[:,1]
wind = North.iloc[:,7]
plt.scatter(lats,wind)
plt.grid()
plt.xlabel('Latitudes')
plt.ylabel('Wind Speed (mph)')

(slope, intercept, rvalue, pvalue, stderr) = linregress(lats, wind)
regress_values = lats * slope + intercept
plt.plot(lats,regress_values,"r-")

line_eq = "y = " + str(round(slope,2)) + "x +" + str(round(intercept,2))
plt.annotate(line_eq,(0,15),fontsize=12,color="red")
plt.show()


# ####  Southern Hemisphere - Wind Speed (mph) vs. Latitude Linear Regression

# In[40]:


slats = South.iloc[:,1]
swind = South.iloc[:,7]
plt.scatter(slats,swind)
plt.grid()
plt.xlabel('Latitudes')
plt.ylabel('Wind Speed (mph)')

(slope, intercept, rvalue, pvalue, stderr) = linregress(slats, swind)
regress_values = slats * slope + intercept
plt.plot(slats,regress_values,"r-")

line_eq = "y = " + str(round(slope,2)) + "x +" + str(round(intercept,2))
plt.annotate(line_eq,(-50,12),fontsize=12,color="red")
plt.show()


# In[ ]:


# Analysis in pdf presentation file. <weather_vacation_analysis.pdf>

