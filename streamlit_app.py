import streamlit as st
import pandas as pd
import requests as req

# Set title
st.title('My Parents\' New Healthy Diner')

# Header for Breakfast Menu
st.header('Breakfast Menu')

# List of breakfast items
breakfast_items = [
    '🥣 Omega 3 & Blueberry Oatmeal',
    '🥗 Kale, Spinach & Rocket Smoothie',
    '🐔 Hard-Boiled Free-Range Egg',
    '🥑🍞 Avocado Toast'
]

# Display breakfast items
for item in breakfast_items:
    st.text(item)

# Header for Build Your Own Fruit Smoothie
st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Load the fruit macros data
fruit_macros_url = "https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt"
my_fruit_list = pd.read_csv(fruit_macros_url)

# Set the index of the DataFrame to 'Fruit'
my_fruit_list.set_index('Fruit', inplace=True)

# Select fruits using multiselect
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

# Filter the DataFrame based on selected fruits
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display selected fruit macros in a table
st.dataframe(fruits_to_show)

# Header for Fruityvice Fruit Advice
st.header("Fruityvice Fruit Advice!")

# Fetch data from Fruityvice API for a specific fruit (e.g., kiwi)
fruit_name = "kiwi"
fruityvice_response = req.get(f"https://fruityvice.com/api/fruit/{fruit_name}")

# Convert API response to a Pandas DataFrame for better display
if fruityvice_response.status_code == 200:
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    st.dataframe(fruityvice_normalized)
else:
    st.error(f"Failed to fetch data for {fruit_name}. Please try again later.")
