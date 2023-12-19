import streamlit as st
import pandas as pd
import requests as req

# Set title
st.title('My Parents New Healthy Diner')

# Breakfast Menu
st.header('Breakfast Menu')

st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

# Another header for a special menu item
st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Load the fruit macros data
fruit_macros_url = "https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt"
my_fruit_list = pd.read_csv(fruit_macros_url)

# Set the index of the DataFrame to 'Fruit'
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

# Filter the DataFrame based on selected fruits
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the selected fruit macros in a table on the page
st.dataframe(fruits_to_show)

# New Section to display fruityvice api response
st.header("Fruityvice Fruit Advice!")

fruityvice_response = req.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())
