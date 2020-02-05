from ff_espn_api import League
from getpass import getpass
from urllib import request
import os
import json
import properties
import pyfiglet

def main():
    printHeader()
    checkNet()
    league = openLeague()
    week = getWeek()
    
    lastWeek = 0 ##last weeks poll points, will be gotten from file
    pollScore = 0 ## current week pollscore, written to file
    pollList = []
    scoreList = {}
    
    for team in league.teams:
        lastWeek = readScore(team.team_id, week)
        matchScore = team.scores[int(week)]
        if properties.debug:
            print('TeamID: ' + str(team.team_id))
        print("\n" + str(team.team_name) + "\n" +\
              str(team.wins) + " Wins\n" +\
              str(team.losses) + " Losses\n" +\
              str(matchScore) + " Match Score\n")
        onlinePoll = getOnlinePoll()
        print('-')
        pollScore = (round((lastWeek*.5)+int(onlinePoll)*2+matchScore+((team.wins-team.losses)*10),2))
        if properties.debug:
            print('pollScore = ' + str(pollScore) + '\n-----\n')
        pollList.append((pollScore, team.team_id))
        scoreList[team.team_id] = pollScore
    writeScores(scoreList, week)
    pollList.sort(reverse=True)
    printList(pollList, league)


def writeScores(scoreList, week):
    with open('week' + str(week) + '.txt', 'w') as json_file:
        json.dump(scoreList, json_file)

def readScore(teamID, week):
    if int(week) == 0:
        return 0
    else:
        try:
            with open('week' + str(int(week)-1) + '.txt') as j:
                data = json.load(j)
                score = data[str(teamID)]
            if properties.debug:
                print('\nlast week score: ' + str(score))
            return score
        except:
            print('Unable to open Last Week scores. Is week number valid?')
            exit()

def checkNet():
    print('Checking network connection...')
    try:
        request.urlopen('http://google.com')
    except:
        exceptCont('Failed!\n' +\
                   'Internet connection required for script!\n'+\
                   'Check network connection before trying again.')
    print('Success!')
    os.system('cls')
    printHeader()
def openLeague():
    try: 
        if properties.private:
            user = input('Enter username: ')
            password = getpass('Enter password: ')
            print('Loading league...')
            league = League(properties.league, properties.year, username=user, password=password)
        else:
            print('Loading league...')
            league = League(properties.league, properties.year)
        os.system('cls')
        printHeader()
        print('League loaded!\n-------------------------------\n\n')
        return league
    except:
        exceptCont('')

def printList(list, league):
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    rank = 0
    for pair in list:
        rank += 1
        i = 0
        line = str(rank) + ") "
        for x in pair:
            if i == 1:
                team = League.get_team_data(league, x)
                print(line + team.team_name + " " + str(pair[i-1]))
            i += 1

def getWeek():
    week = input("Enter Week (starts at 0): ")
    try:
        int(week)
    except:
        print('Invalid Week value: \"' + str(week) + '\" is not an integer')
        exit()
    return week
    
def getOnlinePoll():
    onlinePoll = input("\nOnline Poll Score: ")
    try:
        int(onlinePoll)
    except:
        print('Invalid Poll Score: \"' + str(onlinePoll) + '\" is not a number!' +\
            '\nExiting Program...')
        exit()
    return onlinePoll

def exceptCont(message):
    print(message)
    cont = input('Try again? (y/n): ')
    if cont == 'y':
        os.system('cls')
        main()
    else:
        exit()

def printHeader():
    print(pyfiglet.figlet_format("PowerPoll 2020"))

main()