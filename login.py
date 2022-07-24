# Homepage
import streamlit as st
from PIL import Image
import mysql.connector
import subprocess

# to setup mysql connection
# Creating connection
conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password333",
        database="stock_filtering_dashboard_database",
    )
cur = conn.cursor()




Menu = ["Home","Login","Sign Up"]
process=st.selectbox("Menu",Menu)
if process=="Home":
    #st.subheader("Home")
    st.title("Dashboard")
    image = Image.open('DASHBOARD_trial_sheet_testdb\stock2.png')
    st.image(image, caption='Stocks Analyser',use_column_width='auto')
elif process=="Login":
    st.subheader("Login")
    username=st.text_input("Username")
    password=st.text_input("Password",type='password')
    if st.button("Login"):
        acc_query="SELECT username,password FROM user_login where username='"+username+"'"
        cur.execute(acc_query)
        value=cur.fetchall()
        if value:
            db_username=str(value[0][0])
            db_password=str(value[0][1])
            if username == db_username and password == db_password:
                if 'authentication' not in st.session_state:
                    st.session_state.authentication = True

                st.success("Successfully logged in as {}".format(username))
                st.balloons()
                subprocess.Popen(["streamlit", "run", "F:\Project\Stock_filtering_dashboard\DASHBOARD_trial_sheet_testdb\master_sheet\pages\master_sheet_maker.py"])

            else:
                if 'authentication' not in st.session_state:
                    st.session_state.authentication = False
                st.warning("incorrect username and password!")
        else:
            st.warning("incorrect username and password!")


elif process==("Sign Up"):
    st.subheader("Create New Account")
    user_id = st.text_input("User ID (mail_id)")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    acc_query = "SELECT * FROM user_login where id='" + str(user_id) + "' AND username='" + username + "' AND password='" + password + "'"
    cur.execute(acc_query)
    values = cur.fetchall()
    if st.button("Sign Up"):
        if values:
            st.warning("User already exist!")
        else:
            add_query='insert into `user_login`(`id`,`username`,`password`)VALUES(%s,%s,%s)'
            cur.execute(add_query, (str(user_id), username, password))
            conn.commit()
            st.success("Successfully created.")
            st.balloons()
