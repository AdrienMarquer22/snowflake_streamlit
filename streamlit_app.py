import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Parents New Healthy diner")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg ')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
select = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

fruitsshow = my_fruit_list.loc[select]
streamlit.dataframe(fruitsshow)


def getfruit(frui):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + frui)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try: 
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
        back_fun=getfruit(fruit_choice)
        # write your own comment - what does this do?
        streamlit.dataframe(back_fun)
except URLError as e:
    streamlit.error()



streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()
# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) 
    my_data_rows = get_fruit_load_list() 
    my_cnx.close()
    streamlit.dataframe (my_data_rows)





# Allow the end user to add a fruit to the list 
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('"+ new_fruit +"')") 
        return "Thanks for adding " + new_fruit
add_my_fruit = streamlit.text_input('What fruit would you like to add?') 
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) 
    back_from_function = insert_row_snowflake(add_my_fruit) 
    my_cnx.close()
    streamlit.text(back_from_function)