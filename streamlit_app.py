import streamlit 
import pandas
import requests
import snowflake.connector


from urllib.error import URLError


streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),  ['Avocado','Strawberries'])

fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),  ['Avocado','Strawberries'])
#fliter only selected fruit in dataset
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Display the table on the page
streamlit.dataframe(fruits_to_show)

#new section to display fruitvice api
streamlit.header("Fruityvice Fruit Advice!")

try:
#added text box
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    streamlit.write('The user entered ', fruit_choice)
      
    if fruit_choice :
        streamlit.error('Please select a fruit to get information.')
    else:    
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
        #normalizing json   
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())   
    
        #displayed normalized json  
        streamlit.dataframe(fruityvice_normalized)

except URLError as e:
    streamlit.error()

streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchall()
streamlit.text("The fruit load list contains:")
streamlit.dataframe(my_data_row)

add_my_fruit = streamlit.text_input('What fruit would you like Add?','Jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

my_cur.execute("insert into FRUIT_LOAD_LIST values('Streamlit')")