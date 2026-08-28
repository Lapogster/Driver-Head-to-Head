import fastf1
import streamlit as st
#from fastf1 import plotting
#import pandas as pd
import os
import loadData
import stTools

currentSeason = 2026

# Session state first time setup
if not os.path.exists(".temp"):
    os.makedirs(".temp", exist_ok=True)
fastf1.Cache.enable_cache(".temp")
if "page" not in st.session_state:
    st.session_state.page = "home"
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



# Page display
if st.session_state.page == "home":
    st.title("Teammate Head-to-Head")
    st.subheader("Select a season to view:")

    season = st.selectbox("Select a season", range(1950, currentSeason+1), (currentSeason-1950 - 1), accept_new_options=False)
    st.session_state.year = season

    st.subheader("Select a team to compare:")
    col1, col2 = st.columns(2)

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

    with col1:
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

    with col2:
        if numTeamsCol2 > 0:
            i = 1
            j = 1
            while i <= numTeamsCol2:
                if st.button(st.session_state.teamNames[j]):
                    st.session_state.selectedTeam = st.session_state.teamNames[j]
                    st.session_state.page = "teamView"
                    st.rerun()
                i += 1
                j += 2

elif st.session_state.page == "teamView":
    columns = st.session_state.drivenFor[st.session_state.selectedTeam]
    columns = st.columns(len(st.session_state.drivenFor[st.session_state.selectedTeam]))

    driverI = 0
    while driverI < len(columns):
        with columns[driverI]:
            st.session_state.drivenFor[st.session_state.selectedTeam][driverI]

            driverI += 1

            print(st.session_state.yearSessions[0].results)
        