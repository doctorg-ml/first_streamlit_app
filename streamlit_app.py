import streamlit as st
import pandas as pd
import requests as req
import snowflake.connector

# Set title
st.title("My Parents' New Healthy Diner")

# Display breakfast menu
st.header('Breakfast Menu')
breakfast_items = [
    '🥣 Omega 3 & Blueberry Oatmeal',
    '🥗 Kale, Spinach & Rocket Smoothie',
    '🐔 Hard-Boiled Free-Range Egg',
    '🥑🍞 Avocado Toast'
]
for item in breakfast_items:
    st.text(item)

# Display section for building a fruit smoothie
st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Load and display available fruits
fruit_macros_url = "https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt"
my_fruit_list = pd.read_csv(fruit_macros_url)
my_fruit_list.set_index('Fruit', inplace=True)
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
st.dataframe(fruits_to_show)

# Input field to add a new fruit
new_fruit = st.text_input("Add a new fruit to the list:")
if new_fruit:
    my_fruit_list.loc[new_fruit] = 0  # Add the new fruit to the DataFrame

    # Display updated fruit list
    st.header('Updated Fruit List')
    st.dataframe(my_fruit_list)

# Display advice from Fruityvice API for a specific fruit
st.header("Fruityvice Fruit Advice!")
fruit_name = "kiwi"  # You can change this to fetch advice for the added fruit
fruityvice_response = req.get(f"https://fruityvice.com/api/fruit/{fruit_name}")
if fruityvice_response.status_code == 200:
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    st.dataframe(fruityvice_normalized)
else:
    st.error(f"Failed to fetch data for {fruit_name}. Please try again later.")

# Snowflake Connection and displaying fruit load list
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
    my_cur.execute("SELECT * from fruit_load_list")
    my_data_rows = my_cur.fetchall()

    st.header("Snowflake: Fruit Load List")
    st.text("The fruit load list contains:")
    st.write(my_data_rows)

except snowflake.connector.errors.ProgrammingError as e:
    st.error(f"Snowflake Error: {e}")
