import csv
import pandas as pd
import math
import os

def nomdatcoll(film, person, awlink, candidate):
    print(candidate)
    error = 0
    msg = ""
    films = []
    df = pd.read_csv("data/allFilms.csv")
    for idx, row in df.iterrows():
        films.append(row["films"])

    flength = len(films)
        
    nominated = []
    nominator = []
    candidates = []
    df = pd.read_csv(awlink)
    for idx, row in df.iterrows():
        if (row['movie'] == film):
            error = 1
            msg = "Movie Already Entered"
        nominated.append(row["movie"])
        nominator.append(row["nominator"])
        candidates.append(row["candidate"])
    print(candidate)

    if error == 0:
        nominated.append(film)
        nominator.append(person)
        candidates.append(candidate)
    print(candidate)
    
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
            candidates.pop(i)
            error = 1
            msg = "User has Entered the Max Amount of Nomiations"

    nlength = len(nominated)
    with open(awlink, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        header = ['movie', 'nominator', 'candidate']
        writer.writerow(header)
        for i in range(0, nlength):
            line = [nominated[i], nominator[i], candidates[i]]
            writer.writerow(line)

    rows = int(math.ceil(nlength/3))

    start = 0
    end=3


    return films, rows, start, end, flength, nlength, error, msg


def nomcsv(award, year):
    awlink = ""
    awards = []
    codes = []

    df = pd.read_csv("data/"+year+"AwardList.csv")
    for idx, row in df.iterrows():
        awards.append(row["awards"])
        codes.append(row["code"])

    for i in range(len(awards)):
        if awards[i] == award:
            awlink = "data/Nominations/"+codes[i]+".csv"

    
    isExist = os.path.exists(awlink)
    if(isExist == False):
        with open(awlink, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            header = ['movie', 'nominator', 'candidate']
            writer.writerow(header)


    return awlink