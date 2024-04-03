import streamlit as st
from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()

st.title(":cup_with_straw: Customize")
st.write("""Choose the fruits""")

name_on_order = st.text_input('Smoothie name:')
st.write('The name on Smoothie shall be:', name_on_order)

#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
  'Choose up to 5', my_dataframe, max_selections=5
)

if ingredients_list:
  ingredients_string = ''

  for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen + ' '

  my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
              values ('""" + ingredients_string + """','"""+name_on_order+ """')"""
