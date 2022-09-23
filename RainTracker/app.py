# streamlit run app.py

# from operator import index
# from tkinter.ttk import Style
import pandas as pd
from calendar import calendar


import calendar #core python module
from datetime import date, datetime #core python module

import streamlit as st #pip install streamlit
from streamlit_option_menu import option_menu #pip install streamlit option menu
import plotly.express as px # pip install plotly

import database as db


#----------------settings-------------
page_title = "Rain Tracker"
page_icon = ":umbrella:"
layout = "centered"
units = "mm"
todays_date = date.today()
#--------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

#----Navigation Menu ----
selected = option_menu(
    menu_title=None,
    options=["Data Entry", "History"],
    icons= ["pencil-fill", "bar-chart-fill"],
    orientation="horizontal"
)


#----Dropdown values for selecing the period
years = [datetime.today().year, datetime.today().year - 1]
months = list(calendar.month_name[1:])

#---- input and save periods ----
if selected == "Data Entry":
    st.header(f"Rain in {units}")
    with st.form("entry_form",clear_on_submit=True):

    #   "---"
        st.date_input("Enter Date", key="selected_date")
        st.number_input(f"Enter Rain in mm", min_value=0, format="%i", step=1, key="rain_fall")
        st.text_area("Observations", placeholder="Enter observation here", key="observation")

        "---"
        submitted = st.form_submit_button("Save Rainfall")
        if submitted:
            entered_date = str(st.session_state["selected_date"])
            dt=datetime.strptime(entered_date, '%Y-%m-%d')
            entered_month = dt.strftime("%B")
            entered_year = dt.year
            rain_amount = int(st.session_state["rain_fall"])
            observation = str(st.session_state["observation"])
            # TODO: Insert Values into Spreadsheet or Database
            db.insert_rainfall(entered_date, entered_month, entered_year, rain_amount, observation)

            st.write(f"Date: {entered_date}")
            st.write(f"Month: {entered_month}")
            st.write(f"Year: {entered_year}")

            st.write(f"Rainfall: {rain_amount}")
            st.write(f"Observation: {observation}")
            st.success("Data Saved")


#--- Plot Rainfall ---
if selected == "History":
    st.header("Rainfall History")
    with st.form("saved_periods"):
        #TODO: Get periods from database
        select_month = st.selectbox("Select Month:", ('January', 'February', 'March', 'April',
        'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')) #TODO: default to current month/year
        select_year = st.selectbox("Select Year", (2022, 2023))
        submitted = st.form_submit_button("View Period")
        rain_falls = db.fetch_all_dates()
        if submitted:
            rain_month_total = 0
            ds = []
            rs = []
            os =[]
            for rain in rain_falls:
                if rain["month"] == select_month and rain["year"] == select_year:
                    rain_month_total += rain["rainfall"]      
                    ds.append(rain["key"])   
                    rs.append(rain["rainfall"])
                    os.append(rain["observation"]) 
            st.write(f"Total Rain for selected Month: ", rain_month_total, "mm")
            
            data = {"Date":ds, "Rainfall (mm)": rs, "Observation": os}

            df = pd.DataFrame(data)
            
            st.table(df)

            if ds:
                fig = px.bar(x=ds, y=rs)
                st.plotly_chart(fig, use_container_width=True)

        # Create Metrics
        # total_rainfall = sum(rain_falls.values())
        # selected_month = calendar.month_name[datetime.now().month] #calendar.month_name(datetime.now().today)
        # col1, col2 = st.columns(2)
        # col1.metric("Total Rainfall", f"{total_rainfall}")
        # col2.metric("Month: ", selected_month)
        
        

        #fig = px.line(pd.DataFrame(rain_falls, index=["key"]).T, y="key")
        # fig = px.bar(x=['2022-09-21', '2022-09-18', '2022-09-12', '2022-09-10', 
        #                 '2022-09-5', '2022-09-4', 
        #                 '2022-09-3', '2022-09-1'], y=[5, 0, 3, 10, 
        #                 5, 0, 5, 1])
        # st.plotly_chart(fig, use_container_width=True)


        



        




