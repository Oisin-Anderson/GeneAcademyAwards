import csv
import pandas as pd
import math
import os


def calculate(year, award):
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


    movies = []
    nominator = []
    candidate = []
    ffion = []
    fiachra = []
    oisin = []
    total = []

    df = pd.read_csv(awlink)
    for idx, row in df.iterrows():
        movies.append(row["movie"])
        nominator.append(row["nominator"])
        candidate.append(row["candidate"])
        ffion.append(row["ffion"])
        fiachra.append(row["fiachra"])
        oisin.append(row["oisin"])
        total.append(row["total"])

    for i in range(len(total)):
        total[i] = ffion[i] + fiachra[i] + oisin[i]
    
    with open(awlink, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        header = ['movie', 'nominator', 'candidate', 'ffion', 'fiachra', 'oisin', 'total']
        writer.writerow(header)
        for i in range(len(movies)): 
            line = [movies[i], nominator[i], candidate[i], ffion[i], fiachra[i], oisin[i], total[i]]
            writer.writerow(line)

def gettop(awlink, num):
    movies = []
    nominators = []
    candidate = []
    total = []

    df = pd.read_csv(awlink)

    df.sort_values(["total"], 
                    axis=0,
                    ascending=[False], 
                    inplace=True)

    for idx, row in df.iterrows():
        movies.append(row["movie"])
        nominators.append(row["nominator"])
        candidate.append(row["candidate"])
        total.append(row["total"])

    movie = ""
    nominator = ""
    message = ""
    points = 0

    num = num - 1
    movie = movies[num]
    nominator = nominators[num]
    message = candidate[num]
    points = total[num]
    




    return movie, nominator, message, points

def getall(awlink):
    movies = []
    nominators = []
    candidate = []
    ffion = []
    fiachra = []
    oisin = []
    total = []

    df = pd.read_csv(awlink)

    df.sort_values(["total"], 
                    axis=0,
                    ascending=[False], 
                    inplace=True)

    for idx, row in df.iterrows():
        movies.append(row["movie"])
        nominators.append(row["nominator"])
        candidate.append(row["candidate"])
        ffion.append(row["ffion"])
        fiachra.append(row["fiachra"])
        oisin.append(row["oisin"])
        total.append(row["total"]) 


    return movies, nominators, candidate, ffion, fiachra, oisin, total
