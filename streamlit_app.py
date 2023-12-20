import streamlit as st
import pandas as pd
import requests as req
import snowflake.connector

# Set title
st.title("My Parents' New Healthy Diner")

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

# Snowflake Connection
try:
    snowflake_config = {
        "user": st.secrets["snowflake"]["user"],
        "password": st.secrets["snowflake"]["password"],
        "account": st.secrets["snowflake"]["account"],
        "warehouse": st.secrets["snowflake"]["warehouse"],
        "database": st.secrets["snowflake"]["database"],
        "schema": st.secrets["snowflake"]["schema"]
    }

    my_cnx = snowflake.connector.connect(**snowflake_config)
    my_cur = my_cnx.cursor()
    my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
    my_data_row = my_cur.fetchone()
    st.text("Hello from Snowflake:")
    st.text(my_data_row)

except snowflake.connector.errors.ProgrammingError as e:
    st.error(f"Snowflake Error: {e}")
