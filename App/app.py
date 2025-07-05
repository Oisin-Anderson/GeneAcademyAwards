from flask import Flask, render_template, request
import csv
import pandas as pd
import numpy as np
import math
from nominations import nomdatcoll, nomcsv, nomcode
from voting import votdatcoll, votcode
from awards import calculate, gettop, getall

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
    df = pd.read_csv("data/"+year+"films.csv")
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
    df = pd.read_csv("data/"+year+"films.csv")
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


#Voting Page Loads
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

    awlink = nomcsv(award, year)
        
    films = []
    candidates = []
    df = pd.read_csv(awlink)
    for idx, row in df.iterrows():
        films.append(row["movie"])
        candidates.append(row["candidate"])

    length = len(films)
    rows = int(math.ceil(length/3))
    
    with open("data/voteCount.csv", 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        header = ['count']
        writer.writerow(header)
        line = [length]
        writer.writerow(line)

    start = 0
    end=3
    error = 0
    msg = ""

    return render_template('voting.html', candidates=candidates, award=award, year=year, films=films, rows=rows, start=start, end=end, error=error, msg=msg, length=length)

#Submit Votes
@app.route('/subvot', methods=['GET', 'POST'])
def subvot():
    voter = request.form['voter']
    amount = 0
    df = pd.read_csv("data/voteCount.csv")
    for idx, row in df.iterrows():
        amount = row["count"]

    strings = []
    num = ""
    votes = []
    id = ""
    check = 0
    real = 0
    error = 0
    for i in range(0, amount):
        num = str(i)
        strings = ["film", num]
        id = "".join(strings)
        check += i + 1
        temp = request.form[id]
        real += int(temp)
        votes.append(request.form[id])
    print(votes)


    
    df = pd.read_csv("data/current.csv")
    for idx, row in df.iterrows():
        year = row["year"]
        award = row["award"]
    if type(year) != str:
        year = int(year)
        year = str(year)
    awlink = nomcsv(award, year)
    
    movies = []
    nominator = []
    candidates = []
    ffion = []
    fiachra = []
    oisin = []
    total = []
    df = pd.read_csv(awlink)
    for idx, row in df.iterrows():
        movies.append(row["movie"])
        nominator.append(row["nominator"])
        candidates.append(row["candidate"])
        ffion.append(row["ffion"])
        fiachra.append(row["fiachra"])
        oisin.append(row["oisin"])
        total.append(row["total"])

    
    rows = int(math.ceil(amount/3))
    start = 0
    end=3
    error = 0
    msg = ""


    if check != real:
        error = 1
        msg = "Incorrect Values Entered Below"
        return render_template('voting.html', award=award, year=year, films=movies, rows=rows, start=start, end=end, error=error, msg=msg, length=amount)

    with open(awlink, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        header = ['movie', 'nominator', 'candidate', 'ffion', 'fiachra', 'oisin', 'total']
        writer.writerow(header)
        for i in range(0, amount):
            if(voter == "Oisin"):
                line = [movies[i], nominator[i], candidates[i], ffion[i], fiachra[i], votes[i], total[i]]
                writer.writerow(line)
            if(voter == "Ffion"):
                line = [movies[i], nominator[i], candidates[i], votes[i], fiachra[i], oisin[i], total[i]]
                writer.writerow(line)
            if(voter == "Fiachra"):
                line = [movies[i], nominator[i], candidates[i], ffion[i], votes[i], oisin[i], total[i]]
                writer.writerow(line)
    


    return render_template('voting.html', candidates=candidates, award=award, year=year, films=movies, rows=rows, start=start, end=end, error=error, msg=msg, length=amount)







#Award Page Loads
@app.route('/awapage', methods=['POST'])
def awapage(): 
    
    list = []
    prog = []
    year = request.form['year']

    df = pd.read_csv("C:/Users/oisin/OneDrive/Documents/GitHub/GeneAcademyAwards/App/data/2018-2022AwardList.csv")
    for idx, row in df.iterrows():
            list.append(row["awards"])
            prog.append(row['completed'])

    award = ""
    num = len(prog)
    for i in range(0, num):
        if(prog[i] == "No"):
            award = list[i]
            break

    if award == "":
        return render_template('home.html')

    calculate(year, award)
    
    with open('data/current.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        header = ['year', 'award']
        writer.writerow(header)
        line = [year, award]
        writer.writerow(line)


    return render_template('award.html', award=award, year=year)


#Award Page Loads
@app.route('/third', methods=['POST', 'GET'])
def third(): 
    df = pd.read_csv("data/current.csv")
    for idx, row in df.iterrows():
            year = row["year"]
            award = row['award']

    if type(year) != str:
        year = int(year)
        year = str(year)

    num = 3
    link = "second"

    awlink = nomcsv(award, year)
    movie, nominator, message, points = gettop(awlink, num)

    return render_template('pos.html', award=award, year=year, movie=movie, nominator=nominator, message=message, points=points, link=link)

#Award Page Loads
@app.route('/second', methods=['POST', 'GET'])
def second(): 
    df = pd.read_csv("data/current.csv")
    for idx, row in df.iterrows():
            year = row["year"]
            award = row['award']

    if type(year) != str:
        year = int(year)
        year = str(year)

    num = 2
    link = "first"

    awlink = nomcsv(award, year)
    movie, nominator, message, points = gettop(awlink, num)

    return render_template('pos.html', award=award, year=year, movie=movie, nominator=nominator, message=message, points=points, link=link)
#Award Page Loads
@app.route('/first', methods=['POST', 'GET'])
def first(): 
    df = pd.read_csv("data/current.csv")
    for idx, row in df.iterrows():
            year = row["year"]
            award = row['award']

    if type(year) != str:
        year = int(year)
        year = str(year)

    num = 1
    link = "all"

    awlink = nomcsv(award, year)
    movie, nominator, message, points = gettop(awlink, num)

    return render_template('pos.html', award=award, year=year, movie=movie, nominator=nominator, message=message, points=points, link=link)


#Award Page Loads
@app.route('/all', methods=['POST', 'GET'])
def all(): 
    df = pd.read_csv("data/current.csv")
    for idx, row in df.iterrows():
            year = row["year"]
            award = row['award']

    if type(year) != str:
        year = int(year)
        year = str(year)

    awlink = nomcsv(award, year)
    movies, nominators, messages, ffion, fiachra, oisin, points = getall(awlink)

    length = len(movies)
    rows = int(math.ceil(length/3))

    start = 0
    end=3

    list = []
    prog = []
    df = pd.read_csv("data/"+year+"Awards.csv")
    for idx, row in df.iterrows():
            list.append(row["awards"])
            prog.append(row['completed'])

    award = ""
    num = len(prog)
    for i in range(0, num):
        if(prog[i] == "No"):
            prog[i] = "Yes"
            break

    with open("data/"+year+"Awards.csv", 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        header = ['awards', 'completed']
        writer.writerow(header)
        for i in range(len(list)): 
            line = [list[i], prog[i]]
            writer.writerow(line)

    return render_template('all.html', award=award, year=year, movies=movies, nominators=nominators, message=messages, ffion=ffion, fiachra=fiachra, oisin=oisin, points=points, nlength=length, rows=rows, start=start, end=end)

#Award Page Loads
@app.route('/restart', methods=['POST', 'GET'])
def restart(): 
    
    list = []
    prog = []
    df = pd.read_csv("data/current.csv")
    for idx, row in df.iterrows():
            year = row["year"]

    if type(year) != str:
        year = int(year)
        year = str(year)

    df = pd.read_csv("data/"+year+"Awards.csv")
    for idx, row in df.iterrows():
            list.append(row["awards"])
            prog.append(row['completed'])

    award = ""
    num = len(prog)
    for i in range(0, num):
        if(prog[i] == "No"):
            award = list[i]
            break

    if award == "":
        return render_template('home.html')

    calculate(year, award)
    
    with open('data/current.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        header = ['year', 'award']
        writer.writerow(header)
        line = [year, award]
        writer.writerow(line)


    return render_template('award.html', award=award, year=year)

if __name__ == '__main__':
    app.run()
