# Libraries
import streamlit as sl
import pandas as pd
import requests as req
import snowflake.connector as sc
from urllib.error import URLError

# Functions
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = req.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

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
try:
  fruit_choice = sl.text_input('What fruit would you like information about?')
  if not fruit_choice:
    sl.error('Please select a fruit to get information.')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    sl.dataframe(back_from_function)

except URLError as e:
  sl.error()

#sl.stop()
# Snowflake functions
def get_fruit_load_list():
  with my_cnx.cursor as my_cur:
    my_cur.execute('select * from pc_rivery_db.public.fruit_load_list')
    return my_cur.fetchone()

sl.header('The fruit load list contains:')
# Add a button to load the fruit
my_cnx = sc.connect(**sl.secrets['snowflake'])
my_cur = my_cnx.cursor()
rows = my_cur.execute('select * from fruit_load_list')
sl.dataframe(rows)
  
# Allow the end user to add a fruit to the list
add_my_fruit = sl.text_input('What fruit would you like to add?')
sl.write('The user entered ', add_my_fruit)

