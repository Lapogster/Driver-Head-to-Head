import fastf1
import os
from stTools import loadingText

if not os.path.exists(".temp"):
    os.makedirs(".temp", exist_ok=True)
fastf1.Cache.enable_cache(".temp")

# Load Session data
def loadSession(year, race, session):
    session = fastf1.get_session(year, race, session)
    session.load(laps=False, telemetry=False, weather=False, messages=False, livedata=True)

    return session

def loadDriverHeadshot(session, driverNum):

    session.load()
    sessionResult = session.results

    headshot = sessionResult.loc[driverNum, "HeadshotUrl"]

    print(headshot)

    if headshot == "":
        return False
    return headshot

def loadTeams(year, yearSessions):
    driverCounts = {}
    drivenFor = {}
    teamNames = []

    for race in yearSessions:
        driverI = 0
        while driverI < len(race.results["TeamName"]):
            team = race.results["TeamName"].iloc[driverI]
            driver = race.results["FullName"].iloc[driverI]
            driver = race.results["DriverId"].iloc[driverI]
            driverNum = race.results["DriverNumber"].iloc[driverI]

            if team not in teamNames:
                teamNames.append(team)
        
            if team in driverCounts.keys():
                if not any(listedDriver[0] == driver for listedDriver in drivenFor[team]):
                    driverCounts[team] += 1
                    drivenFor[team].append((driver, driverNum, race))
            else:
                driverCounts[team] = 1
                drivenFor[team] = []
                drivenFor[team].append((driver, driverNum, race))

            driverI += 1

    return (year, driverCounts, teamNames, drivenFor)

#@st.cache_data(show_spinner="Downloading and caching season data | First load may take a few minutes...")
def loadYear(year, loadText):
    yearSessions = []
    schedule = loadSchedule(year)

    for race in schedule:
        loadingText(f"Loading {race} data...", loadText)
        yearSessions.append(loadSession(year, race, "R"))


    teamData = loadTeams(year, yearSessions)

    return (yearSessions, teamData)

def loadSchedule(year):
    seasonRaces = []
    schedule = fastf1.get_event_schedule(year)
    for i, row in schedule.iterrows():
        if (row["EventFormat"] != "testing"):
            seasonRaces.append(row["EventName"])

    return seasonRaces