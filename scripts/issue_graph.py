import requests
from datetime import datetime
from matplotlib import dates, pyplot as plt


PROJECT_ID = 2413
ACCESS_TOKEN = ""
URL = f"https://stgit.dcs.gla.ac.uk/api/v4/projects/{PROJECT_ID}/issues"
OPEN_ISSUES_MAP = {}
CLOSED_ISSUES_MAP = {}

plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%d/%m/%Y'))

issues = requests.get(URL, params={"access_token": ACCESS_TOKEN}).json()

for issue in issues:
    opened_date = datetime.fromisoformat(issue["created_at"]).date()
    OPEN_ISSUES_MAP[opened_date] = OPEN_ISSUES_MAP.get(opened_date, 0) + 1

    if issue["state"] == "closed":
        closed_date = datetime.fromisoformat(issue["closed_at"]).date()
        CLOSED_ISSUES_MAP[closed_date] = CLOSED_ISSUES_MAP.get(closed_date, 0) + 1


plt.xlabel("Date (DD/MM/YYYY)")
plt.ylabel("Number of issues")
plt.title("Issue Count for CS20")
plt.yticks(range(10))

for map in [
    {"name": "Issues opened", "data": OPEN_ISSUES_MAP},
    {"name": "Issues closed", "data": CLOSED_ISSUES_MAP}
]:
    x = []
    y = []

    for dt, count in sorted(map["data"].items(), key=lambda t: t[0]):
        x.append(dt)
        y.append(count)

    plt.plot(x, y, label=map["name"])
    plt.gcf().autofmt_xdate()

plt.legend()
plt.show()
