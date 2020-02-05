# PowerPoll 2020
PowerPoll 2020 is a simple pyhton script that downloads league data using ESPN's Fantasy League API, in turn by using [cwendt94's ff-espn-api tools](https://github.com/cwendt94/ff-espn-api).
##  Installation

Script requires Python 3 or higher in order to run (available from the [Python site](https://www.python.org/downloads/) or the Microsoft Store).

After installing Pyhton, place the PowerPoll files into any directory (making a seperate directory for each year will make the output files much simpler to sift through).

Then, run *install.bat*, this installs the python libraries needed for operation.

In *properties.py*, enter the League ID and year into the appropriate lines, and if the league is public, set *private = False*, otherwise, set *private = True*.
## Usage

To run the Poll, open PowerPoll.bat.

If the league is private, it will ask for the username/email you use for your ESPN Fantasy league, as well as the password. (If the league is public, this step is skipped).

Enter in the current week of play (the first week starts at 0). Then, for each team in the league, enter in the score gotten from however you choose to take ballots. (I use Survey Monkey's rank surveys for this).

After all scores are entered, the script will then calculate the Poll Score for each team, before generating a ranked list of teams. The Poll Score accounts previous weeks' Poll Scores, as well as Wins vs. Losses for the season and points scored in a match.
Results are also output as a python dict in *weekx.txt*.
