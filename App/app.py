from flask import Flask, render_template, request
import csv
import pandas as pd
import numpy as np
import math
from nominations import nomdatcoll, nomcsv, nomcode
from voting import votcsv, votdatcoll, votcode

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
    prog = []
    year = request.form['year']

    df = pd.read_csv("data/"+year+"AwardList.csv")
    for idx, row in df.iterrows():
            list.append(row["awards"])
            prog.append(row['nominating'])
    
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
    
    return render_template('nompage.html', year=year, list=list, prog=prog, length=length, rows=rows, start=start, end=end)

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
    films, rows, start, end, flength, nlength, error, msg, prog = nomdatcoll(film, person, awlink, candidate, year)
    nomcode(prog, award, year)

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
    
    list = []
    prog = []
    year = request.form['year']

    df = pd.read_csv("data/"+year+"AwardList.csv")
    for idx, row in df.iterrows():
            list.append(row["awards"])
            prog.append(row['voting'])
    
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
    
    return render_template('votpage.html', year=year, list=list, prog=prog, length=length, rows=rows, start=start, end=end)


#Nominating Page Loads
@app.route('/vot/<award>', methods=['POST', 'GET'])
def vot(award):
    df = pd.read_csv("data/current.csv")
    for idx, row in df.iterrows():
        year = row["year"]

    if type(year) != str:
        year = int(year)
        year = str(year)

    with open('data/current.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        header = ['year', 'award']
        writer.writerow(header)
        line = [year, award]
        writer.writerow(line)

    awlink = votcsv(award, year)
        
    films = []
    df = pd.read_csv(awlink)
    for idx, row in df.iterrows():
        films.append(row["movie"])

    length = len(films)
    rows = int(math.ceil(length/3))

    start = 0
    end=3
    error = 0
    msg = ""

    return render_template('voting.html', award=award, year=year, films=films, rows=rows, start=start, end=end, error=error, msg=msg, length=length)

#Submit Votes
@app.route('/subvot', methods=['GET', 'POST'])
def subvot():
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
    films, rows, start, end, flength, nlength, error, msg, prog = nomdatcoll(film, person, awlink, candidate)
    nomcode(prog, award, year)

    nominated = []
    nominator = []
    candidates = []
    df = pd.read_csv(awlink)
    for idx, row in df.iterrows():
        nominated.append(row["movie"])
        nominator.append(row["nominator"])
        candidates.append(row["candidate"])

    return render_template('nominations.html', nominated=nominated, nominator=nominator, candidates=candidates, films=films, rows=rows, start=start, end=end, year=year, award=award, flength=flength, nlength=nlength, error=error, msg=msg)







#Award Page Loads
@app.route('/awapage', methods=['POST'])
def awapage():


    return render_template('headpage.html')


if __name__ == '__main__':
    app.run()
