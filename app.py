import fastf1
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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
plt.style.use('dark_background')

# Page display
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center;'>Teammate Head-to-Head</h1>", unsafe_allow_html=True)

    # Make season select box in center
    c1, col2, c3 = st.columns(3)
    with col2:
        season = st.selectbox("Select a season", range(1950, currentSeason+1), (currentSeason-1950 - 1), accept_new_options=False)
    st.session_state.year = season

    st.markdown("<h2 style='text-align: center;'>Select a team to compare:</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    # Load newly selected year
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

    # Setup for teams display
    numTeams = len(st.session_state.teamNames)
    numTeamsCol1 = numTeams - int((len(st.session_state.teamNames)/2))
    numTeamsCol2 = int(len(st.session_state.teamNames)/2)
    # Display all teams from year
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

    # Tally team points from races
    teamPoints = 0
    racePoints = 0
    sprintPoints = 0
    for session in st.session_state.yearSessions:
        teamResults = session.results[session.results["TeamName"] == st.session_state.selectedTeam]
        teamPoints += teamResults["Points"].sum()
        racePoints += teamResults["Points"].sum()

    # Tally team points from sprints when they exist
    season = loadData.loadSchedule(st.session_state.loadedYear)
    loadingMessage = st.empty()
    sprintCount = 0
    for session in season:
        try:
            # Load each sprint
            stTools.loadingText("Loading Team Data...", loadingMessage)
            sprint = loadData.loadSession(st.session_state.loadedYear, session, "S")
            sprintPoints += sprint.results.loc[sprint.results["TeamName"] == st.session_state.selectedTeam, "Points"].sum()
            teamPoints += sprint.results.loc[sprint.results["TeamName"] == st.session_state.selectedTeam, "Points"].sum()
            sprintCount += 1
        except ValueError:
            # Race has no sprint
            pass

    # Clearing loading text
    with loadingMessage:
        st.empty()

    # Load all driver names for the team
    driverI = 0
    while driverI < len(columns):
        with columns[driverI]:
            driver = st.session_state.drivenFor[st.session_state.selectedTeam][driverI][2].get_driver(st.session_state.drivenFor[st.session_state.selectedTeam][driverI][1])

            # Load driver portraits if enabled
            if driverPortraits:
                stTools.renderNamePFP(loadData.loadDriverHeadshot(st.session_state.drivenFor[st.session_state.selectedTeam][driverI][2], st.session_state.drivenFor[st.session_state.selectedTeam][driverI][1]), st.session_state.drivenFor[st.session_state.selectedTeam][driverI][0])
            else:
                st.markdown(f"<h1 style='text-align: center;'>{driver['FullName']}</h1>", unsafe_allow_html=True)

            driverI += 1

    st.markdown("<h3 style='text-align: center;'>Championship Points:</h3>", unsafe_allow_html=True)


    columns = st.session_state.drivenFor[st.session_state.selectedTeam]
    columns = st.columns(len(st.session_state.drivenFor[st.session_state.selectedTeam]), border=True)
    driverI = 0
    while driverI < len(columns):
        with columns[driverI]:
            driver = st.session_state.drivenFor[st.session_state.selectedTeam][driverI][2].get_driver(st.session_state.drivenFor[st.session_state.selectedTeam][driverI][1])
            col1, col2 = st.columns(2)

            # Display point counts
            with col1:
                driverPoints = 0
                driverRacePoints = 0
                driverSprintPoints = 0
                for session in st.session_state.yearSessions:
                    driverResults = session.results[session.results["DriverId"] == driver["DriverId"]]
                    driverPoints += driverResults["Points"].sum()
                    driverRacePoints += driverResults["Points"].sum()
                if sprintCount != 0:
                    for session in season:
                        try:
                            sprint = loadData.loadSession(st.session_state.loadedYear, session, "S")
                            driverSprintPoints += sprint.results.loc[sprint.results["DriverId"] == driver["DriverId"], "Points"].sum()
                            driverPoints += sprint.results.loc[sprint.results["DriverId"] == driver["DriverId"], "Points"].sum()
                        except ValueError:
                            # Race has no sprint
                            pass

                stTools.betterText("Total Points:<br>" + str(driverPoints))
                if sprintCount != 0:
                    stTools.betterText("Race Points:<br>" + str(driverRacePoints))
                    stTools.betterText("Sprint Points:<br>" + str(driverSprintPoints))
            # Display percantage of the teams points
            with col2:
                stTools.betterText("Percentage of Team Points:<br>" + str(round((driverPoints/teamPoints)*100, 2)) + "%")
                if sprintCount != 0:
                    stTools.betterText("Percentage of Points in Races:<br>" + str(round((driverRacePoints/racePoints)*100, 2)) + "%")
                    stTools.betterText("Percentage of Points in Sprints:<br>" + str(round((driverSprintPoints/sprintPoints)*100, 2)) + "%")

            driverI += 1

    drivers = st.session_state.drivenFor[st.session_state.selectedTeam]
    points = {driverId: 0 for driverId, _, _ in drivers}
    pointsHistory = {driverId: [] for driverId, _, _ in drivers}
    sessionNames = []
    for race in st.session_state.yearSessions:
        sessionNames.append(race.event["EventName"])

        for driverId, _, _ in drivers:
            result = race.results[race.results["DriverId"] == driverId]

            if not result.empty:
                points[driverId] += float(result.iloc[0]["Points"])

            pointsHistory[driverId].append(points[driverId])

    # Championship points graph
    fig, ax = plt.subplots(figsize=(10, 5))

    cleanedSessionNames = []
    for session in sessionNames:
        cleaned = session.replace(" Grand Prix", "")
        cleanedSessionNames.append(cleaned)

    for driverId, _, _ in drivers:
        ax.plot(cleanedSessionNames, pointsHistory[driverId], marker="o", label=driverId.replace("_", " ").title())

    ax.set_xlabel("Race")
    ax.set_ylabel("Points")
    ax.set_title("Driver Points Comparison")

    ax.legend()
    ax.grid(alpha=0.3)
    ax.tick_params(axis="x", rotation=90)

    c1, col2, c3 = st.columns([1,4,1])
    with col2:
        st.pyplot(fig, width=2400)

    stTools.backButton()
