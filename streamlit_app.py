import streamlit as st
from snowflake.snowpark.functions import col
import requests

cnx = st.connection("snowflake")
session = cnx.session()

st.title(":cup_with_straw: Customize")
st.write("""Choose the fruits""")

name_on_order = st.text_input('Smoothie name:')
st.write('The name on Smoothie shall be:', name_on_order)

#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON))
st.dataframe(data=my_dataframe,use_container_width=True)
st.stop()                                                                                       
                                                                                            

ingredients_list = st.multiselect(
  'Choose up to 5', my_dataframe, max_selections=5
)

if ingredients_list:
  ingredients_string = ''

  for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen + ' '
    st.subheader(fruit_chosen + ' Nutrition Information')
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
    fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

  my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
              values ('""" + ingredients_string + """','"""+name_on_order+ """')"""
