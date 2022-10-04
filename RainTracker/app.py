### comment for git
import pandas as pd
from calendar import calendar


import calendar  # core python module
from datetime import date, datetime  # core python module

import streamlit as st  # pip install streamlit
# pip install streamlit option menu
from streamlit_option_menu import option_menu
import plotly.express as px  # pip install plotly

import database as db


# ----------------settings-------------
page_title = "Rain Tracker"
page_icon = ":umbrella:"
layout = "centered"
units = "mm"
todays_date = date.today()
# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

# ----Navigation Menu ----
selected = option_menu(
    menu_title=None,
    options=["Data Entry", "History"],
    icons=["pencil-fill", "bar-chart-fill"],
    orientation="horizontal"
)


# ----Dropdown values for selecing the period
years = [datetime.today().year, datetime.today().year - 1]
months = list(calendar.month_name[1:])

# ---- input and save periods ----
if selected == "Data Entry":
    st.header(f"Rain in {units}")
    with st.form("entry_form", clear_on_submit=True):

        #   "---"
        st.date_input("Enter Date", key="selected_date")
        # TODO: ensure local timezone shows correct day.
        st.number_input(f"Enter Rain in mm", min_value=0.0, format="%f", step=0.5, key="rain_fall")
        st.text_area("Observations",
                     placeholder="Enter observation here", key="observation")

        "---"
        submitted = st.form_submit_button("Save Rainfall")
        if submitted:
            entered_date = str(st.session_state["selected_date"])
            dt = datetime.strptime(entered_date, '%Y-%m-%d')
            entered_month = dt.strftime("%B")
            entered_year = dt.year
            rain_amount = float(st.session_state["rain_fall"])
            observation = str(st.session_state["observation"])

# Insert into database
            db.insert_rainfall(entered_date, entered_month,
                               entered_year, rain_amount, observation)


# Show on page and indicate success
            st.write(f"Date: {entered_date}")
            st.write(f"Month: {entered_month}")
            st.write(f"Year: {entered_year}")

            st.write(f"Rainfall: {rain_amount}")
            st.write(f"Observation: {observation}")
            st.success("Data Saved")


# --- Plot Rainfall ---
if selected == "History":
    st.header("Rainfall History")
    with st.form("saved_periods"):
        # TODO: Get periods from database
        select_month = st.selectbox("Select Month:", ('January', 'February', 'March', 'April',
                                                      'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'))  # TODO: default to current month/year
        select_year = st.selectbox("Select Year", (2022, 2023))
        submitted = st.form_submit_button("View Period")

        if submitted:
            rain_falls = db.fetch_all_dates()
            rain_month_total = 0
            ds = []
            rs = []
            os = []
            for rain in rain_falls:
                if rain["month"] == select_month and rain["year"] == select_year:
                    rain_month_total += rain["rainfall"]
                    ds.append(rain["key"])
                    rs.append(rain["rainfall"])
                    os.append(rain["observation"])

            st.metric(label="Total Rain for selected Month",
                      value=rain_month_total)

            data = {"Date": ds, "Rainfall (mm)": rs, "Observation": os}
            
            
            df = pd.DataFrame(data)
            df.round(1)
            st.table(df)

            if ds:
                fig = px.bar(x=ds, y=rs)
                fig.update_xaxes(title="date")
                fig.update_yaxes(title="mm")
                fig.update_layout(margin=dict(
                    l=5,        # left
                    r=5,        # right
                    t=50,        # top
                    b=10         # bottom
                ))
                st.plotly_chart(fig, use_container_width=True,
                                config={'displayModeBar': False})
