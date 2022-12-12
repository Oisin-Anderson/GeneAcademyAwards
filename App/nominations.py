import csv
import pandas as pd
import math

def nomdatcoll(film, person):
    df = pd.read_csv("App/data/current.csv")
    for idx, row in df.iterrows():
        year = row["year"]
        award = row["award"]

    if type(year) != str:
        year = int(year)

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
    df = pd.read_csv("App/data/2022NomBestPic.csv")
    for idx, row in df.iterrows():
        nominated.append(row["movie"])
        nominator.append(row["nominator"])

    nominated.append(film)
    nominator.append(person)
    nlength = len(nominated)
    with open('App/data/2022NomBestPic.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        header = ['movie', 'nominator']
        writer.writerow(header)
        for i in range(0, nlength):
            line = [nominated[i], nominator[i]]
            writer.writerow(line)

    rows = int(math.ceil(nlength/3))

    start = 0
    end=3


    return films, rows, start, end, year, award, flength, nlength
