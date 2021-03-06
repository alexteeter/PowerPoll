# PowerPoll 2020
PowerPoll 2020 is a simple python script that downloads league data using ESPN's Fantasy League API, in turn by using [cwendt94's ff-espn-api tools](https://github.com/cwendt94/ff-espn-api).
### NOTE: Username/Password Login is currently broken due to change on ESPN's side. Please use SWID/espn_s2 values to login!
##  Installation
### Before You Download
Script requires Python 3 or higher in order to run (available from the [Python site](https://www.python.org/downloads/) or the Microsoft Store).

### Download
The latest release can be found [here](https://github.com/alexteeter/PowerPoll/releases).
After installing Python, extract the PowerPoll files into any directory of your choosing. The script will make seperate directories for each season (so long as you update the properties file!).

Then, run *install.bat*, this installs the python libraries needed for operation. This only needs to run once.
### Important
In *properties.py*, enter the League ID and year into the appropriate lines, and if the league is public, set *private = False*, otherwise, set *private = True*. Without league ID, script will not work!

League ID can be found in the URL of your league:
>*fantasy.espn.com/football/team?*__leagueId=1234567__*&teamId=1&seasonId=2020*

## Usage

To run the Poll, open PowerPoll.pyw.

If the league is private, it will ask for the username/email you use for your ESPN Fantasy league, as well as the password. (If the league is public, this step is skipped).

Enter in the current week of play (the first week starts at 0). Then, for each team in the league, enter in the score gotten from however you choose to take ballots. (I use Survey Monkey's rank surveys for this).

After all scores are entered, the script will then calculate the Poll Score for each team, before generating a ranked list of teams. The Poll Score accounts previous weeks' Poll Scores, as well as Wins vs. Losses for the season and points scored in a match.
Results are also output as a text file for easy copy/pasting.

To run the script with console output, open PowerPoll.bat instead.

