import streamlit as st
import pandas as pd

uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
if st.checkbox("Upload"):
    files=uploaded_files
    list_n=[]
    df_list=[]
    df_dict={}
    count=0

    col1,col2=st.columns(2)
    for uploaded_file in uploaded_files:
        count+=1
        list_n.append(uploaded_file.name)
        df = pd.read_csv(uploaded_file)
        df_list.append(df)
        if count%2 == 0:
            with col2:
                st.write("{})filename : ".format(count), uploaded_file.name)
                st.write(df, height=100)
        else:
            with col1:
                st.write("{})filename : ".format(count), uploaded_file.name)
                st.write(df, height=100)
    if 'first_table' not in st.session_state:
        st.session_state.first_table = pd.DataFrame({'Name':[],'BSE Code':[],'NSE Code':[],'Industry':[]})
    if st.checkbox("Create Master sheet"):
        #st.write(list_n)
        #st.write(df_list)
        res = {}
        for key in list_n:
            for value in df_list:
                res[key] = value
                df_list.remove(value)
                break
        #st.write(res)
        select=st.selectbox("Select:",options=res.keys())
        st._legacy_dataframe(res.get(select))
        #process=st.radio("Select Process",options=('Show','First Table','New Columns','New Companies'))
        col1,col2,col3=st.columns(3)


        if col1.button("First Table"):
            st.session_state.first_table=pd.DataFrame(res.get(select))
            st.write("First Table")
            st._legacy_dataframe(st.session_state.first_table)
        #else:
            #st._legacy_dataframe(st.session_state.first_table)

        if col2.button('New Columns'):
            df_new=pd.DataFrame(res.get(select))
            st.session_state.first_table=pd.merge(st.session_state.first_table,df_new,on=['Name','BSE Code','NSE Code','Industry'])
            st.write("combined Table")
            #st._legacy_dataframe(st.session_state.first_table)
        #else:
            #st._legacy_dataframe(st.session_state.first_table)


        if col3.button("Clear"):
            st.session_state.first_table.drop(st.session_state.first_table.index,inplace=True)
            st.experimental_rerun()
            st._legacy_dataframe(st.session_state.first_table)
        else:
            st.write("Current Master Table:")
            st._legacy_dataframe(st.session_state.first_table)

        df=st.session_state.first_table
        csv=df.to_csv()
        st.download_button("download your file",csv,"mega_sheet.csv")
    else:
        st.write("Current Master Table:")
        st.session_state.first_table.drop(st.session_state.first_table.index, inplace=True)
        st._legacy_dataframe(st.session_state.first_table)
