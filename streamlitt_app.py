import requests
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!"""
)

title = st.text_input("Name of Smoothie")
st.write(f"The name of your Smoothie will be: {title}")

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose up to 6 ingredients:",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    st.write(ingredients_list)
    ingredients_string = ", ".join(ingredients_list)
    for fruit in ingredients_list:
      st.subheader(f"{fruit} Nutrition Information")
      smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit}")
      sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders(ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{title}');"""
  
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {title}!', icon="✅")
