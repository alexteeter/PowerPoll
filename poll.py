from ff_espn_api import League
from getpass import getpass
from urllib import request
import os
import json
import properties
import pyfiglet
import PySimpleGUI as sg
import sys, traceback



def main(): 
    global path
    global week
    path = os.getcwd()
    printHeader()
    checkNet()
    league = openLeague()
    week = getWeek()
    pollList = []
    scoreList = {}
    
    layout = []
    col = [[sg.Text('Enter Online Poll Scores:')]]
    col2 = [[sg.Text('')]]
    for team in league.teams:
        col += [[sg.Text(team.team_name + ' (' + str(team.wins) + '-' + str(team.losses) + ') ')]]
        col2 += [[sg.In(key=team.team_id)]]
    layout = [[sg.Column(col), sg.Column(col2, element_justification='r')],
             [sg.Button('Save', bind_return_key=True)]]
    window = sg.Window('PowerPoll2020',layout)
    while True:  
        event, values = window.read()
        if event == 'Save':
            break
        if event is None:
           quit()
        print(event, values)
    window.close() 
    for team in league.teams:
        lastWeek = readScore(team.team_id)
        lastRank = getLastRank(team.team_name)
        matchScore = team.scores[int(week)]
        onlinePoll = values[team.team_id]
        try:
            int(onlinePoll)
        except:
            sg.PopupError(str(values[team.team_id]) + ' is not a Vaild Number!')
            main()
        pollScore = (round((lastWeek*.5)+(int(onlinePoll)*properties.pollMultiplier)+matchScore+((team.wins-team.losses)*10),2))
        pollList.append((pollScore, team.team_id))
        scoreList[team.team_id] = pollScore
    writeScores(scoreList)
    pollList.sort(reverse=True)
    printList(pollList, league)
    displayList(pollList, league)

def writeScores(scoreList):
    filepath = str(path) + '/' + str(properties.year) + '/json/'
    filename = filepath + 'week' + str(week) + '.json'
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
    except OSError:
        sg.Popup('Fatal Error:\nFailed to Make Directory!')
        quit()
    with open(filename, 'w') as json_file:
        json.dump(scoreList, json_file)

def readScore(teamID):
    if int(week) == 0:
        return 0
    else:
        filename = str(path) + '/' + str(properties.year) + '/json/week' + str(int(week)-1) + '.json'
        try:
            with open(filename) as j:
                data = json.load(j)
                score = data[str(teamID)]
            if properties.debug:
                print('\nlast week score: ' + str(score))
            return score
        except:
            sg.PopupError('Failure!\nUnable to open Last Week scores.\nIs week number valid?')
            print('Unable to open Last Week scores. Is week number valid?')
            exit()

def getLastRank(team_name):
    if int(week) == 0:
        return 0
    else:
        filename = str(path) + '/' + str(properties.year) + '/Polls/week' + str(int(week)-1) + '.txt'
        try:
            with open(filename) as f:
                lines = f.readlines()
                for line in lines:
                    if line.find(team_name) != -1:
                        rank = line.split(')')[0]
            if properties.debug:
                print('\nlast week rank: ' + rank)
            return rank
        except:
            sg.PopupError('Failure!\nUnable to open Last Week rankings.\nIs week number valid?')
            print('Unable to open Last Week rankings. Is week number valid?')
            exit()

def checkNet():
    print('Checking network connection...')
    try:
        request.urlopen('http://google.com')
    except:
        sg.PopupError('Failed!\n' +\
                      'Internet connection required for script!\n'+\
                      'Check network connection before trying again.')
        exceptCont('Failed!\n' +\
                   'Internet connection required for script!\n'+\
                   'Check network connection before trying again.')
    print('Success!')
    os.system('cls')
    printHeader()
def openLeague():
    if properties.league == 0:
        sg.PopupError('Please Change League ID in properties.py File!')
        quit()
    if properties.private:
        if properties.useSWID == False:
            display = 'Enter Your Login Information (ESPN Account)'
    
            layout = [[sg.Text(display,key='-DISPLAY-'), sg.Text(size=(15,1), key='-OUTPUT-')],
                    [sg.Input(key='user')],
                    [sg.Text('Password'), sg.Text(size=(15,1))],
                    [sg.Input(key='pass', password_char='*')],
                    [sg.Button('OK', bind_return_key=True)]]
            
            window = sg.Window('PowerPoll 2020', layout)
            
            while True:  # Event Loop
                event, values = window.read()
                if event is  (None):
                    quit()
                    break
                if event == 'OK':
                    sg.PopupAutoClose('Loading League...', non_blocking=True)
                    try:
                        league = League(properties.league, properties.year, username=values['user'], password=values['pass'])
                        test = league.get_team_data(league)
                    except:
                        league = None
                        sg.PopupError('League Failed to Load!')
                        window.close()
                        league = openLeague()
                    sg.PopupAutoClose('League Loaded!')
                    break
            window.close()
        else:
            sg.PopupAutoClose('Loading League...', non_blocking=True)
            try:
                league = League(properties.league, properties.year, espn_s2=properties.espn_s2, swid=properties.swid)
                sg.PopupAutoClose('League Loaded!')
            except:
                league = None
                sg.PopupError('League Failed to Load!\nCheck espn_s2 or SWID values.')
                window.close()
    else:
        sg.PopupAutoClose('Loading League...', non_blocking=True)
        league = League(properties.league, properties.year)
        sg.PopupAutoClose('League Loaded!')
    os.system('cls')
    printHeader()
    print('League loaded!\n-------------------------------\n\n')
    return league
def printList(list, league):
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    rank = 0   
    filepath = str(path) + '/' + str(properties.year) + '/Polls/'
    filename = filepath + 'week' + str(week) + '.txt'
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
    except OSError:
        sg.Popup('Fatal Error:\nFailed to Make Directory!')
        quit()   
    f = open(filename, 'wb')
    for pair in list:
        rank += 1
        i = 0
        line = str(rank) + ") "
        for x in pair:
            if i == 1:
                team = League.get_team_data(league, x)
                if properties.debug:
                    line = line + team.team_name + " " + str(pair[i-1]) + " Prev.: " + str(getLastRank(team.team_name))
                else:
                    line = line + team.team_name + " -  Prev: " + str(getLastRank(team.team_name))
                f.write(line.encode('utf8'))
                f.write('\n'.encode())
                print(line)
            i += 1

def displayList(list, league):
    rank = 0
    layout = [[sg.Text('Week ' + str(week) + ' PowerPoll Rankings:')]]
    for pair in list:
        rank += 1
        i = 0
        line = str(rank) + ') '
        for x in pair:
            if i == 1:
                team = League.get_team_data(league, x)
                line = line + team.team_name + " " + str(pair[i-1])
                layout += [[sg.Text(line)]]
            i += 1
    layout += [[sg.Button('OK', bind_return_key=True)]]
    window = sg.Window('PowerPoll 2020', layout)
    while True:
        event, values = window.Read()
        if event is None or event =='OK':
            break
    window.close()

def getWeek():
    display = ''
    week = 0
    layout = [[sg.Text('Enter Week (Starts at 0)',key='-DISPLAY-'), sg.Text(size=(15,1), key='-OUTPUT-')],
              [sg.Input(key='-IN-')],
              [sg.Button('OK', bind_return_key=True)]]
    
    window = sg.Window('PowerPoll 2020', layout)
    
    while True:
        event, values = window.read()
        if event is None:
            break
        if event == 'OK':
            display = 'Week:'
            week = values['-IN-']
            break
    
    window.close()
    try:
        int(week)
    except:
        sg.PopupError('\'' + week + '\' is not a valid Week Number!')
        week = getWeek()
    if os.path.exists(str(path) + '/' + str(properties.year) + '/json/week' + str(week) + '.json'):
            layout = [[sg.Text('A Poll for Week ' + str(week) + ' already exisits! \nOverwrite?')],
                      [sg.Button('Overwrite', bind_return_key=True), sg.Button('Cancel')]]
            window = sg.Window('Overwrite Poll?', layout)
            while True:
                event, values = window.read()
                if event is None:
                    quit()
                    break
                if event == 'Overwrite':
                    return week
                    break
                if event == 'Cancel':
                    quit()
                    break
            window.close()  
    else:
        return week
    
def getOnlinePoll():
    onlinePoll = input("\nOnline Poll Score: ")
    try:
        int(onlinePoll)
    except:
        print('Invalid Poll Score: \"' + str(onlinePoll) + '\" is not a number!')
        cont = input('Try again? (y/n):')
        if cont == 'y':
            getOnlinePoll()
        else:
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

#main()