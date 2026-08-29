import fastf1
import streamlit as st
#from fastf1 import plotting
#import pandas as pd
import os
import loadData
import stTools

currentSeason = 2026
driverPortraits = False

# Session state first time setup
# Cache
if not os.path.exists(".temp"):
    os.makedirs(".temp", exist_ok=True)
fastf1.Cache.enable_cache(".temp")
# Session Variables
if "page" not in st.session_state:
    st.session_state.page = "home"
if "pageHistory" not in st.session_state:
    st.session_state.pageHistory = []
if "year" not in st.session_state:
    st.session_state.year = None
if "loadedYear" not in st.session_state:
    st.session_state.loadedYear = None
if "yearSessions" not in st.session_state:
    st.session_state.yearSessions = []
if "driverCounts" not in st.session_state:
    st.session_state.driverCounts = {}
if "teamNames" not in st.session_state:
    st.session_state.teamNames = []
if "drivenFor" not in st.session_state:
    st.session_state.drivenFor = {}
if "selectedTeam" not in st.session_state:
    st.session_state.selectedTeam = None
# Page Config
st.set_page_config(page_title="Teammate Head-to-Head", page_icon="🏁", layout="wide")

# Page display
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center;'>Teammate Head-to-Head</h1>", unsafe_allow_html=True)

    c1, col2, c3 = st.columns(3)
    with col2:
        season = st.selectbox("Select a season", range(1950, currentSeason+1), (currentSeason-1950 - 1), accept_new_options=False)
    st.session_state.year = season

    st.markdown("<h2 style='text-align: center;'>Select a team to compare:</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    if st.session_state.year != st.session_state.loadedYear:
        loadText = st.empty()
        yearData = loadData.loadYear(st.session_state.year, loadText)
        st.session_state.loadedYear = st.session_state.year
        st.session_state.yearSessions = yearData[0]
        st.session_state.loadedYear = yearData[1][0]
        st.session_state.driverCounts = yearData[1][1]
        st.session_state.teamNames = yearData[1][2]
        st.session_state.drivenFor = yearData[1][3]
        st.rerun()

    numTeams = len(st.session_state.teamNames)
    numTeamsCol1 = numTeams - int((len(st.session_state.teamNames)/2))
    numTeamsCol2 = int(len(st.session_state.teamNames)/2)

    with col3:
        if numTeams < 1:
            st.text(f"Failed to load any races for the {st.session_state.loadedYear} season")
        else:
            i = 1
            j = 0
            while i <= numTeamsCol1:
                if st.button(st.session_state.teamNames[j]):
                    st.session_state.selectedTeam = st.session_state.teamNames[j]
                    st.session_state.page = "teamView"
                    st.rerun()
                i += 1
                j += 2

    with col4:
        if numTeamsCol2 > 0:
            i = 1
            j = 1
            while i <= numTeamsCol2:
                if st.button(st.session_state.teamNames[j]):
                    st.session_state.selectedTeam = st.session_state.teamNames[j]
                    stTools.setPage("teamView")
                    st.rerun()
                i += 1
                j += 2
# View drivers for the selected team
elif st.session_state.page == "teamView":
    columns = st.session_state.drivenFor[st.session_state.selectedTeam]
    columns = st.columns(len(st.session_state.drivenFor[st.session_state.selectedTeam]))

    print(st.session_state.drivenFor[st.session_state.selectedTeam])

    driverI = 0
    while driverI < len(columns):
        with columns[driverI]:
            driver = st.session_state.drivenFor[st.session_state.selectedTeam][driverI][2].get_driver(st.session_state.drivenFor[st.session_state.selectedTeam][driverI][1])
            print(driver)

            if driverPortraits:
                stTools.renderNamePFP(loadData.loadDriverHeadshot(st.session_state.drivenFor[st.session_state.selectedTeam][driverI][2], st.session_state.drivenFor[st.session_state.selectedTeam][driverI][1]), st.session_state.drivenFor[st.session_state.selectedTeam][driverI][0])
            else:
                st.header(driver["FullName"])

            driverI += 1

    
    stTools.backButton()
        