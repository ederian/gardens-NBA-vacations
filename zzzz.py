# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 22:49:25 2012

@author: elias
"""

import os, csv
from datetime import datetime
import pandas as pd

file_list = os.listdir('time_series')

teams = {}
for fil in file_list:
    file_name = 'time_series/' + fil
    data = csv.reader(open(file_name,'r'),delimiter='\t')
    fields = data.next()
    name = fil.split('.')[0]
    teams[name] = []
    for row in data:
        item = dict(zip(fields,row))
        teams[name].append(item)

team_names = teams.keys()
# Change dates from strings to datetime objects
for name in team_names:
    dates2 = []
    for team in teams[name]:
        dates2.append(team['dates2'])
    dates = []
    for date in dates2:
        dates.append(datetime.strptime(date, '%Y-%m-%d'))
    i = 0
    for date in dates:
        teams[name][i]['dates2'] = date
        i = i + 1

del file_list, file_name, name, row, item, dates2, date, dates, i, team, fil

def to_int(name):
    ints = ['win','threes','home','pts','tov','fta','pf','blk','ft','ast',
            'threes_a','fg','orb','fga','stl','trb','drb','year']
    for game in teams[name]:
        for var in ints:
            game[var] = int(game[var])

def add_gameNum(team):
    years = [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]
    games = teams[team]
    for year in years:
        balls = []
        for game in games:
            if game['year'] == year:
                balls.append(game)
        i = 0
        for game in balls:
            i += 1
            game['num'] = i

def hist(team):
    games = teams[team]
    if team == 'CHA':
        years = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]
    else:
        years = [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]
    for year in years:
        balls = []
        for game in games:
            if game['year'] == year:
                balls.append(game)
        win_streak = ''
        for game in balls:
            if game['win'] == 0:
                win_streak += 'l'
            else:
                win_streak += 'w'
            game['hist'] = win_streak

def win_streak(team):
    games = teams[team]
    if team == 'CHA':
        years = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]
    else:
        years = [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]
    for year in years:
        balls = []
        for game in games:
            if game['year'] == year:
                balls.append(game)
        for game in balls:
            need = game['hist'][-1]
            streak = 1
            for i in xrange(1,game['num']):
                if game['hist'][-1-i] == need:
                    streak += 1
                else:
                    break
            if need == 'l':
                streak = streak*(-1)
            game['win_streak'] = streak


def season_totals(team):
    print team
    ints2 = ['threes','pts','tov','fta','pf','blk','ft','ast','threes_a',
        'fg','orb','fga','stl','trb','drb']
    season[team] = []
    if team == 'CHA':
        years = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]
    else:
        years = [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]
    games = teams[team]
    for year in years:
        balls = []
        for game in games:
            if game['year'] == year:
                balls.append(game)
        holder = []
        holder.append(balls[0])
        print year
        for i in xrange(1,len(balls)):
            temp = {}
            temp['dates2'] = balls[i]['dates2']
            temp['dates'] = balls[i]['dates']
            temp['win'] = balls[i]['win']
            temp['home'] = balls[i]['home']
            temp['year'] = balls[i]['year']
            temp['num'] = balls[i]['num']
            temp['min'] = balls[i]['min']
            temp['team'] = balls[i]['team']
            temp['opponent'] = balls[i]['opponent']
            temp['hist'] = balls[i]['hist']
            temp['win_streak'] = balls[i]['win_streak']
            for item in ints2:
                marker = holder[i-1][item] + balls[i][item]
                temp[item] = marker
            holder.append(temp)
        for hold in holder:
            season[team].append(hold)


def moving_ten(team):
    print team
    ints2 = ['threes','pts','tov','fta','pf','blk','ft','ast','threes_a',
        'fg','orb','fga','stl','trb','drb']
    ten_day[team] = []
    if team == 'CHA':
        years = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]
    else:
        years = [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]
    games = teams[team]
    for year in years:
        balls = []
        for game in games:
            if game['year'] == year:
                balls.append(game)
        holder = []
        print year
        for i in xrange(9,len(balls)):
            temp = {}
            temp['dates2'] = balls[i]['dates2']
            temp['dates'] = balls[i]['dates']
            temp['win'] = balls[i]['win']
            temp['home'] = balls[i]['home']
            temp['year'] = balls[i]['year']
            temp['num'] = balls[i]['num']
            temp['min'] = balls[i]['min']
            temp['team'] = balls[i]['team']
            temp['opponent'] = balls[i]['opponent']
            temp['hist'] = balls[i]['hist']
            temp['win_streak'] = balls[i]['win_streak']
            for item in ints2:
                marker = 0
                for j in xrange(0,10):
                    marker += balls[i-j][item]
                temp[item] = marker
            holder.append(temp)
        for hold in holder:
            ten_day[team].append(hold)

season = {}
ten_day = {}
for name in team_names:
    to_int(name)
    add_gameNum(name)
    hist(name)
    win_streak(name)
    season_totals(name)
    moving_ten(name)

fields = ['win','threes','num','year','home','pts','tov','fta','pf',
          'blk','opponent','dates2','ft','ast','threes_a','fg','orb','fga',
          'dates','stl','trb','team','drb','hist','win_streak']

for team in team_names:
    games = season[team]
    print 'writing season tots of ' + team
    file_name = 'season_tots/' + team + '.txt'
    output = csv.writer(open(file_name,'w+'),delimiter = '\t')
    for game in games:
        item = [game[fieldname] for fieldname in fields]
        output.writerow(item)
    games2 = ten_day[team]
    file_name2 = 'ten_a_day/' + team + '.txt'
    output2 = csv.writer(open(file_name2, 'w+'),delimiter = '\t')
    print 'writing ten day moving avg of ' + team
    for gam in games2:
        etem = [gam[fieldname] for fieldname in fields]
        output2.writerow(etem)

team = 'IND'
games = season[team]
print 'writing season tots of ' + team
file_name = 'season_tots/' + team + '.txt'
output = csv.writer(open(file_name,'w+'),delimiter = '\t')
for game in games:
    item = [game[fieldname] for fieldname in fields]
    output.writerow(item)
games2 = ten_day[team]
file_name2 = 'ten_a_day/' + team + '.txt'
output2 = csv.writer(open(file_name2, 'w+'),delimiter = '\t')
print 'writing ten day moving avg of ' + team
for gam in games2:
    etem = [gam[fieldname] for fieldname in fields]
    output2.writerow(etem)
