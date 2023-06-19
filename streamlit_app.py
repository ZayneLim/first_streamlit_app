# Libraries
import streamlit as sl
import pandas as pd
import requests as req

# Site content
sl.title('My Parents New Healthy Diner')

sl.header('Breakfast Menu')
sl.text ('🥣 Omega 3 & Blueberry Oatmeal')
sl.text('🥗 Kale, Spinach & Rocket Smoothie')
sl.text('🐔 Hard-Boiled Free-Range Egg')
sl.text('🥑🍞 Avocado Toast')

sl.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Reading fruit list
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Add a pick list here so they can pick the fruit they want to include
fruits_selected = sl.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page
sl.dataframe(fruits_to_show)

# New section to display fruityvice api response
sl.header('Fruityvice Fruit Advice!')

fruityvice_response = req.get("https://fruityvice.com/api/fruit/watermelon")
sl.text(fruityvice_response.json()) # just writes the data tot he screen

# write your own comment -what does the next line do? 
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)




