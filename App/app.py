from flask import Flask, render_template, request
import csv
import pandas as pd
import numpy as np
import math
from nominations import nomdatcoll, nomcsv

app = Flask(__name__)


#Home Page Loads
@app.route('/')
def home():
    return render_template('home.html')

#About Page Loads
@app.route('/about')
def about():
    return render_template('about.html')

#List of Awards For Nominating Page Loads
@app.route('/nompage', methods=['POST', 'GET'])
def nompage():
    
    list = []
    year = request.form['year']

    if(year == "2018-2022"):
        df = pd.read_csv("data/2018-2022AwardList.csv")
        for idx, row in df.iterrows():
            list.append(row["awards"])
        
    elif(year == "2022"):
        df = pd.read_csv("data/2022AwardList.csv")
        for idx, row in df.iterrows():
            list.append(row["awards"])

    
    with open('data/current.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        header = ['year', 'award']
        writer.writerow(header)
        line = [year, ""]
        writer.writerow(line)

    

    print(list)
    length = len(list)
    rows = int(math.ceil(length/3))

    start = 0
    end=3
    
    return render_template('nompage.html', year=year, list=list, length=length, rows=rows, start=start, end=end)

#Nominating Page Loads
@app.route('/nom/<award>', methods=['POST', 'GET'])
def nom(award):
    df = pd.read_csv("data/current.csv")
    for idx, row in df.iterrows():
        year = row["year"]

    if type(year) != str:
        year = int(year)
        year = str(year)

    films = []
    df = pd.read_csv("data/allFilms.csv")
    for idx, row in df.iterrows():
        films.append(row["films"])

    flength = len(films)

    with open('data/current.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        header = ['year', 'award']
        writer.writerow(header)
        line = [year, award]
        writer.writerow(line)

    print(type(year))
    print(year)
    print(type(award))
    print(award)
    awlink = nomcsv(award, year)
        
    nominated = []
    nominator = []
    candidates = []
    df = pd.read_csv(awlink)
    for idx, row in df.iterrows():
        nominated.append(row["movie"])
        nominator.append(row["nominator"])
        candidates.append(row["candidate"])

    nlength = len(nominated)
    rows = int(math.ceil(nlength/3))

    start = 0
    end=3
    error = 0
    msg = ""


    return render_template('nominations.html', award=award, year=year, films=films, flength=flength, nominated=nominated, candidates=candidates, nominator=nominator, nlength=nlength, rows=rows, start=start, end=end, error=error, msg=msg)

#Submit Nomination Loads
@app.route('/subnom', methods=['GET', 'POST'])
def subnom():
    film = request.form['film']
    candidate = request.form['candidate']
    person = request.form['person']
    print(candidate)

    df = pd.read_csv("data/current.csv")
    for idx, row in df.iterrows():
        year = row["year"]
        award = row["award"]

    if type(year) != str:
        year = int(year)
        year = str(year)
    
    awlink = nomcsv(award, year)
    films, rows, start, end, flength, nlength, error, msg = nomdatcoll(film, person, awlink, candidate)

    nominated = []
    nominator = []
    candidates = []
    df = pd.read_csv(awlink)
    for idx, row in df.iterrows():
        nominated.append(row["movie"])
        nominator.append(row["nominator"])
        candidates.append(row["candidate"])

    return render_template('nominations.html', nominated=nominated, nominator=nominator, candidates=candidates, films=films, rows=rows, start=start, end=end, year=year, award=award, flength=flength, nlength=nlength, error=error, msg=msg)

#View Nominations Page Loads
@app.route('/viepage', methods=['POST', 'GET'])
def viepage():
    
    list = []
    year = request.form['year']

    if(year == "2018-2022"):
        df = pd.read_csv("data/2018-2022AwardList.csv")
        for idx, row in df.iterrows():
            list.append(row["awards"])
        
    elif(year == "2022"):
        df = pd.read_csv("data/2022AwardList.csv")
        for idx, row in df.iterrows():
            list.append(row["awards"])

    
    with open('data/current.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        header = ['year', 'award']
        writer.writerow(header)
        line = [year, ""]
        writer.writerow(line)

    

    print(list)
    length = len(list)
    rows = int(math.ceil(length/3))

    start = 0
    end=3
    
    return render_template('viepage.html', year=year, list=list, length=length, rows=rows, start=start, end=end)



#View Nominations Page Loads
@app.route('/indivnom/<award>', methods=['POST', 'GET'])
def indivnom(award):
    df = pd.read_csv("data/current.csv")
    for idx, row in df.iterrows():
        year = row["year"]

    if type(year) != str:
        year = int(year)
        year = str(year)

    films = []
    df = pd.read_csv("data/allFilms.csv")
    for idx, row in df.iterrows():
        films.append(row["films"])

    flength = len(films)

    with open('data/current.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        header = ['year', 'award']
        writer.writerow(header)
        line = [year, award]
        writer.writerow(line)

    print(type(year))
    print(year)
    print(type(award))
    print(award)
    awlink = nomcsv(award, year)
        
    nominated = []
    nominator = []
    candidates = []
    df = pd.read_csv(awlink)
    for idx, row in df.iterrows():
        nominated.append(row["movie"])
        nominator.append(row["nominator"])
        candidates.append(row["candidate"])

    nlength = len(nominated)
    rows = int(math.ceil(nlength/3))

    start = 0
    end=3
    error = 0
    msg = ""


    return render_template('vienom.html', award=award, year=year, films=films, flength=flength, nominated=nominated, candidates=candidates, nominator=nominator, nlength=nlength, rows=rows, start=start, end=end, error=error, msg=msg)



#Voting Page Loads
@app.route('/votpage', methods=['POST'])
def votpage():    
    df = pd.read_csv("FinalYearProjectCurrent/store/leagueName.csv")
    for idx, row in df.iterrows():
        league = row["CurLeague"]
        sleague = row["StorLeague"]
        date = row["Date"]

    seasons = ["2021"]

    clubs = fleagueTeams(league, seasons)
    length = len(clubs)

    for j in range(len(clubs)):
        temp = clubs[j]
        text = ""
        for i in range(len(temp)):
            if temp[i] == ' ':
                text = text + '_'
            else:
                text = text + temp[i]
        clubs[j] = text
    
    clubs.sort()
    print(clubs)

    return render_template('leaguepage.html', cleague=league, clubs=clubs, length=length, date=date, sleague=sleague)

#Award Page Loads
@app.route('/awapage', methods=['POST'])
def awapage():
    league = request.form['league']
    
    df = pd.read_csv("FinalYearProjectCurrent/store/leagueName.csv")
    for idx, row in df.iterrows():
        date = row["Date"]
        sleague = row["StorLeague"]

    with open('FinalYearProjectCurrent/store/leagueName.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        header = ['CurLeague', 'StorLeague', 'Date']
        writer.writerow(header)
        line = [league, sleague, date]
        writer.writerow(line)
    
    seasons = ["2021"]
    clubs = fleagueTeams(league, seasons)
    length = len(clubs)

    for j in range(len(clubs)):
        temp = clubs[j]
        text = ""
        for i in range(len(temp)):
            if temp[i] == ' ':
                text = text + '_'
            else:
                text = text + temp[i]
        clubs[j] = text
    
    clubs.sort()
    print(clubs)
    return render_template('headpage.html', league=league, clubs=clubs, length=length)


if __name__ == '__main__':
    app.run()
