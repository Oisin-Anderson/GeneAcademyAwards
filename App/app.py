from flask import Flask, render_template, request
import csv
import pandas as pd

app = Flask(__name__)


#Home Page Loads
@app.route('/')
def home():
    return render_template('home.html')

#About Page Loads
@app.route('/about')
def about():
    return render_template('about.html')

#Nominating Page Loads
@app.route('/nompage', methods=['POST', 'GET'])
def nompage():
    
    list = []
    year = request.form['year']

    if(year == "2018-2022"):
        df = pd.read_csv("App/data/2018-2022AwardList.csv")
        for idx, row in df.iterrows():
            list.append(row["awards"])
        
    elif(year == "2022"):
        df = pd.read_csv("App/data/2022AwardList.csv")
        for idx, row in df.iterrows():
            list.append(row["awards"])

    

    print(list)

    return render_template('nompage.html', year=year)

#View Nominations Page Loads
@app.route('/viepage', methods=['POST', 'GET'])
def viepage():

    return render_template('viepage.html')

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
