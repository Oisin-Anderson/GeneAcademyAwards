import csv
import pandas as pd
import math

def nomdatcoll(film, person):
    error = 0
    msg = ""

    df = pd.read_csv("App/data/current.csv")
    for idx, row in df.iterrows():
        year = row["year"]
        award = row["award"]

    if type(year) != str:
        year = int(year)
        year = str(year)

    films = []
    df = pd.read_csv("App/data/allFilms.csv")
    for idx, row in df.iterrows():
        films.append(row["films"])

    flength = len(films)

    with open('App/data/current.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        header = ['year', 'award']
        writer.writerow(header)
        line = [year, award]
        writer.writerow(line)
        
    nominated = []
    nominator = []
    df = pd.read_csv("App/data/Nominations/picture22.csv")
    for idx, row in df.iterrows():
        if (row['movie'] == film):
            error = 1
            msg = "Movie Already Entered"
        nominated.append(row["movie"])
        nominator.append(row["nominator"])

    if error == 0:
        nominated.append(film)
        nominator.append(person)
    
    oisin = 0
    ffion = 0
    fiachra = 0
    for i in range(len(nominator)):
        if nominator[i] == "Oisin":
            oisin += 1
        if nominator[i] == "Ffion":
            ffion += 1
        if nominator[i] == "Fiachra":
            fiachra += 1

        if oisin > 3 or ffion > 3 or fiachra > 3:
            nominated.pop(i)
            nominator.pop(i)
            error = 1
            msg = "User has Entered the Max Amount of Nomiations"

    nlength = len(nominated)
    with open('App/data/Nominations/picture22.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        header = ['movie', 'nominator']
        writer.writerow(header)
        for i in range(0, nlength):
            line = [nominated[i], nominator[i]]
            writer.writerow(line)

    rows = int(math.ceil(nlength/3))

    start = 0
    end=3


    return films, rows, start, end, year, award, flength, nlength, error, msg


def nomcsv(award, year):
    awlink = ""
    awards = []
    codes = []

    df = pd.read_csv("App/data/"+year+"AwardList.csv")
    for idx, row in df.iterrows():
        awards.append(row["awards"])
        codes.append(row["code"])

    for i in range(len(awards)):
        if awards[i] == award:
            awlink = "App/data/Nominations/"+codes[i]+".csv"
        print(awards[i])
        print(codes[i])


    return awlink