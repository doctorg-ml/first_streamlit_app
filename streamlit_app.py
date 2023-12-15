import streamlit as st

# Set title
st.title('My Parents New Healthy Diner')

# Breakfast Menu
st.header('Breakfast Menu')

st.text('🥣 Omega 3 & Blueberrey Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

# Another header for a special menu item
st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include
st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

#display the table on the page
st.dataframe(my_fruit_list)


