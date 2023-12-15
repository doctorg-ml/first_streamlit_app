import streamlit as st

# Set title
st.title('My Parents New Healthy Diner')

# Breakfast Menu
st.header('Breakfast Menu')

menu_items = {
    'Avocado Toast': '$8.99',
    'Greek Yogurt Parfait': '$6.99',
    'Veggie Omelette': '$9.99',
    'Fruit Bowl': '$5.99'
}

for item, price in menu_items.items():
    st.write(f'{item}: {price}')

