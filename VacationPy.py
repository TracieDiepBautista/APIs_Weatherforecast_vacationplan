#!/usr/bin/env python
# coding: utf-8

# # VacationPy
# ----
# 
# #### Note
# * Keep an eye on your API usage. Use https://developers.google.com/maps/reporting/gmp-reporting as reference for how to monitor your usage and billing.
# 
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[33]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import gmaps
import os
from pprint import pprint

# Import API key
from api_keys import g_key

# Access maps with unique API key
gkey = ""
gmaps.configure(api_key=gkey)


# ### Store Part I results into DataFrame
# * Load the csv exported in Part I to a DataFrame

# In[3]:



# open csv file from Part I
weather_data_path = "../output_data/weather_data.csv"
weather_data = pd.read_csv(weather_data_path)
weather_data = weather_data.rename(columns = {"temperature (F)" : "Temperature (C)",
                                            "Temp_max (F)" : "Max Temperature (C)"})
weather_data.head()


# ### Humidity Heatmap
# * Configure gmaps.
# * Use the Lat and Lng as locations and Humidity as the weight.
# * Add Heatmap layer to map.

# In[17]:


# Create a list containing coordinates
humidity = weather_data["humidity"]


# In[27]:


# Customize the size of the figure
figure_layout = {
    'width': '600px',
    'height': '400px',
    'border': '1px solid black',
    'padding': '1px',
    'margin': '0 auto 0 auto'
}
fig = gmaps.figure(layout=figure_layout)
fig


# In[5]:


# Store latitude and longitude in locations
locations = weather_data[["latitutes", "longtitudes"]]

# Fill NaN values and convert to float
humidity = weather_data["humidity"].astype(float)


# In[28]:


# Plot Heatmap
fig = gmaps.figure(map_type="TERRAIN")

# Create heat layer
heat_layer = gmaps.heatmap_layer(locations, weights=humidity, 
                                 dissipating=False, max_intensity=20,
                                 point_radius=1)


# Add layer
fig.add_layer(heat_layer)

# Display figure
fig


# ### Create new DataFrame fitting weather criteria
# * Narrow down the cities to fit weather conditions.
# * Drop any rows will null values.

# In[7]:


# condition to travel (based on my family's interests): temp <=25 and >=18 | zero cloudiness | humidity <=40
temp = weather_data["Max Temperature (C)"].astype(float)
new_df = weather_data.loc[(weather_data["Max Temperature (C)"]< 25) & (weather_data["Max Temperature (C)"]>=18) &
 (weather_data["humidity"]<40) & (weather_data["cloudiness"] == 0)]
clean_df = new_df.dropna()
us_cities = clean_df.loc[(clean_df["country"] == "US")]
us_cities.head()
#len(new_df) # the result show there are 13 cities that my family may plan to visit, but we just wanna travel within the US this year so,
# I choose to filter out cities in the US only; 


# ### Hotel Map
# * Store into variable named `hotel_df`.
# * Add a "Hotel Name" column to the DataFrame.
# * Set parameters to search for hotels with 5000 meters.
# * Hit the Google Places API for each city's coordinates.
# * Store the first Hotel result into the DataFrame.
# * Plot markers on top of the heatmap.

# In[8]:


hotel_df = us_cities[["city","latitutes","longtitudes"]]
hotel_df.insert(1, "Hotel Name", " ", True)
hotel_df.insert(2, "Hotel Address", " ", True)
hotel_df.head()


# In[10]:


# params dictionary to update each iteration
params = {
    "radius": 5000,
    "types": "hotel",
    "keyword": "hotel",
    "key": g_key
}

# Use the lat/lng we recovered to identify the hotels
for index, row in hotel_df.iterrows():
    # get lat, lng from df
    lat = row["latitutes"]
    lng = row["longtitudes"]

    # change location each iteration while leaving original params in place
    params["location"] = f"{lat},{lng}"

    # Use the search term: "International Airport" and our lat/lng
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    # make request and print url
    hotel_address = requests.get(base_url, params=params)
    
#     print the name_address url, avoid doing for public github repos in order to avoid exposing key
#     print(name_address.url)

    # convert to json
    hotel_address = hotel_address.json()
    pprint(hotel_address)

    # Since some data may be missing we incorporate a try-except to skip any that are missing a data point.
    try:
        hotel_df.loc[index, "Hotel Name"] = hotel_address["results"][0]["name"]
        hotel_df.loc[index, "Hotel Address"] = hotel_address["results"][0]["vicinity"]

    except (KeyError, IndexError):
        print("Missing field/result... skipping.")
        pass
print('----job done-----')


# In[18]:


hotel_df.head()


# In[22]:


to_mark = hotel_df[['latitutes', 'longtitudes']]
to_mark


# In[29]:


# Create a map and set markers
marker_hotel = to_mark
hotel_name = hotel_df["Hotel Name"]

# Create a marker_layer using the hotel name and address to fill the info box
fig = gmaps.figure()
markers = gmaps.marker_layer(marker_hotel,
    info_box_content=[f"Hotel: {hotel_name}" for name in hotel_name])
fig.add_layer(markers)
fig


# In[3]:


# NOTE: Do not change any of the code in this cell

# Using the template add the hotel marks to the heatmap
info_box_template = """
<dl>
<dt>Name</dt><dd>{Hotel Name}</dd>
<dt>City</dt><dd>{City}</dd>
<dt>Country</dt><dd>{Country}</dd>
</dl>
"""
# Store the DataFrame Row
# NOTE: be sure to update with your DataFrame name
hotel_info = [info_box_template.format(**row) for index, row in hotel_df.iterrows()]
locations = hotel_df[["Lat", "Lng"]]


# In[ ]:


# Add marker layer ontop of heat map


# Display figure


# In[ ]:




