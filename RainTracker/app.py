import pandas as pd
from calendar import calendar


import calendar #core python module
from datetime import date, datetime #core python module

import streamlit as st #pip install streamlit
import plotly.express as px # pip install plotly

#----------------settings-------------
page_title = "Rain Tracker"
page_icon = ":umbrella:"
layout = "centered"
units = "mm"
todays_date = date.today()
#--------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

#----Dropdown values for selecing the period
years = [datetime.today().year, datetime.today().year - 1]
months = list(calendar.month_name[1:])

#---- input and save periods ----
st.header(f"Data Entry in {units}")
with st.form("entry_form",clear_on_submit=True):
    col1, col2 = st.columns(2)
    col1.selectbox("Select Month:", months, key="month")
    col2.selectbox("Select Year:", years, key="year")

    "---"
    st.date_input("Enter Date", key="selected_date")
    st.number_input(f"Enter Rain in mm", min_value=0, format="%i", step=1, key="rain_fall")
    st.text_area("Observations", placeholder="Enter observation here", key="observation")

    "---"
    submitted = st.form_submit_button("Save Rainfall")
    if submitted:
        entered_date = str(st.session_state["selected_date"])
        rain_amount = int(st.session_state["rain_fall"])
        observation = str(st.session_state["observation"])
        # TODO: Insert Values into Spreadsheet or Database
        st.write(f"Date: {entered_date}")
        st.write(f"Rainfall: {rain_amount}")
        st.write(f"Observation: {observation}")
        st.success("Data Saved")


#--- Plot Rainfall ---
st.header("Rainfall History")
with st.form("saved_periods"):
    #TODO: Get periods from database
    period = st.selectbox("Select Period:", ["2022_September"])
    submitted = st.form_submit_button("Change Period")
    #if submitted:
    #TODO: Get Data from Database
    comment = "some Comment"
    rain_falls = {'2022-09-21': 5, '2022-09-18': 0, '2022-09-12': 3, '2022-09-10': 10, 
                    '2022-09-5': 5, '2022-09-4': 0, 
                    '2022-09-3': 5, '2022-09-1': 1 }
    
    # Create Metrics
    total_rainfall = sum(rain_falls.values())
    selected_month = calendar.month_name[datetime.now().month] #calendar.month_name(datetime.now().today)
    col1, col2 = st.columns(2)
    col1.metric("Total Rainfall", f"{total_rainfall}")
    col2.metric("Month: ", selected_month)
    st.text(f"Comment: {comment}")

    #fig = px.line(pd.DataFrame(rain_falls, index=["key"]).T, y="key")
    fig = px.bar(x=['2022-09-21', '2022-09-18', '2022-09-12', '2022-09-10', 
                    '2022-09-5', '2022-09-4', 
                    '2022-09-3', '2022-09-1'], y=[5, 0, 3, 10, 
                    5, 0, 5, 1])
    st.plotly_chart(fig, use_container_width=True)


        



        




