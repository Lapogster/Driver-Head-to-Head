import fastf1
import streamlit as st
from fastf1 import plotting
import pandas as pd

currentSeason = 2026

# Session state first time setup
fastf1.Cache.enable_cache('.temp')
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

# Load Session data
@st.cache_data
def loadSession(year, race, session):
    session = fastf1.get_session(year, race, session)
    session.load(laps=False, telemetry=False, weather=False, messages=False, livedata=True)

    return session

def loadDriverHeadshot(session, driverNum):
    sessionResult = session.results

    headshot = sessionResult.loc[driverNum, "HeadshotUrl"]

    if headshot == "":
        return False

    st.image(headshot)
    return True

@st.cache_data
def loadTeams(year):
    pass

@st.cache_data(show_spinner="Downloading and caching season data | First load may take a few minutes...")
def loadYear(year):
    st.session_state.yearSessions = []
    schedule = loadSchedule(year)
    for race in schedule:
        st.text(f"Loading {race} data...")
        st.session_state.yearSessions.append(loadSession(year, race, "R"))
        st.text(f"{race} loading complete!")

    driverCounts = {}
    drivenFor = {}
    teamNames = []
    for race in st.session_state.yearSessions:
        driverI = 0
        while driverI < len(race.results["TeamName"]):
            team = race.results["TeamName"].iloc[driverI]
            driver = race.results["FullName"].iloc[driverI]

            if team not in teamNames:
                teamNames.append(team)
        
            if team in driverCounts.keys():
                if driver not in drivenFor[team]:
                    driverCounts[team] += 1
                    drivenFor[team].append(driver)
            else:
                driverCounts[team] = 1
                drivenFor[team] = []
                drivenFor[team].append(driver)

            driverI += 1

    print(driverCounts)
    print(drivenFor)
    st.session_state.loadedYear = year
    st.session_state.driverCounts = driverCounts
    st.rerun()

@st.cache_data
def loadSchedule(year):
    seasonRaces = []
    schedule = fastf1.get_event_schedule(year)
    for i, row in schedule.iterrows():
        if (row["EventFormat"] != "testing"):
            seasonRaces.append(row["EventName"])

    print(seasonRaces)
    return seasonRaces

# Page display
if st.session_state.page == "home":
    st.title("Teammate Head-to-Head")
    st.subheader("Select a season to view:")

    season = st.selectbox("Select a season", range(1950, currentSeason+1), (currentSeason-1950 - 1), accept_new_options=False)
    st.session_state.year = season

    st.subheader("Select a team to compare:")
    col1, col2 = st.columns(2)

    #loadSchedule(st.session_state.year)
    #session = loadSession(st.session_state.year, 1, "R")
    #print(len(session.results["TeamName"]))
    #teamNames = []
    #driverCounts = {}
    #driverI = 0
    #while driverI < len(session.results["TeamName"]):
    #    team = session.results["TeamName"].iloc[driverI]
    #    teamNames.append(team)
    #    driverI += 1
    #
    #    if team in driverCounts.keys():
    #        driverCounts[team] += 1
    #    else:
    #        driverCounts[team] = 1

    #print(teamNames)
    #print(driverCounts)

    if st.session_state.year != st.session_state.loadedYear:
        loadYear(st.session_state.year)

    print(st.session_state.driverCounts)
    with col1:
        #if loadDriverHeadshot(session, "18") == False:
        #    st.image("Assets/missingIcon.png")
        pass

        
