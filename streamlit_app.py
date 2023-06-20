# Libraries
import streamlit as sl
import pandas as pd
import requests as req
import snowflake.connector 

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
fruit_choice = sl.text_input('What fruit would you like information about?','Kiwi')
sl.write('The user entered ', fruit_choice)

fruityvice_response = req.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# write your own comment -what does the next line do? 
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

# converts into a tabular display using dataframes
sl.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
sl.text("The fruit load list contains:")
sl.text(my_data_rows)



