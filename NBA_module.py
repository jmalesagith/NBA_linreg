import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import argparse
import pathlib
import random

def loadfolder(folder):
    frames = []
    for filename in os.listdir(folder):
        if filename.endswith('.csv'):
            if "adv" in filename:
                data = pd.read_csv(str(folder) + "/" + filename, delimiter=',', header = 0, skiprows = 1)
                frames.append(data)
            else:
                data = pd.read_csv(str(folder) + "/" + filename, delimiter=',', header = 0)
                frames.append(data)

    dataframe = pd.concat(frames,axis=0, ignore_index = True) 
    return dataframe

def makedataframe(df1,df2,df3):
    for col in df1.columns:
        if "Unnamed" in col:
            df1=df1.drop(col, axis=1)
 
    df2 = df2.sort_values(["FG%","Team"])
    df3 = df3.sort_values(["FG%","Team"])
    df3.index=df2.index

    df3=df3.drop(["Rk","Team","G","MP"],axis=1)
    for col in df3.columns.values:
        if '%' in col:
            df3=df3.drop(col,axis=1)
        else:
            df3=df3.rename(columns={col : (col + "/100")})

    df = pd.concat((df2,df3), axis=1)
    df1 = df1.sort_values(["ORtg","Team"])
    df = df.sort_values(["PTS/100","Team"])
    df1.index=df.index

    df = pd.concat((df,df1), axis=1)
    df = df.sort_index()
    df=df.loc[:,~df.columns.duplicated()]

    df=df.drop(["Rk","Arena","Attend.","Attend./G"],axis=1)
    return df

def load2022(folder):
    for filename in os.listdir(folder):
        if filename.endswith('.csv'):
            if "adv" in filename:
                data1 = pd.read_csv(str(folder) + "/" + filename, delimiter=',', header = 0, skiprows = 1)
            elif "poss" in filename:
                data3 = pd.read_csv(str(folder) + "/" + filename, delimiter=',', header = 0)
            else:
                data2=pd.read_csv(str(folder) + "/" + filename, delimiter=',', header = 0)
    df2022=makedataframe(data1,data2,data3)
    return df2022

def makeratio(df):
    ratio = []
    r=len(df)
    W=df['W']
    L=df['L']
    for i in range(0,r):
        ratio.append(W[i]/(L[i]+W[i]))
    return ratio

def makeparams(df):
    parameters = []
    par = '2'
    print(df.columns.values)
    print("Wybierz parametry względem, których chcesz wykonać regresję, jeżeli chcesz zakończyć podaj 'q' ")
    while par!= 'q':
        par = input()
        if par !='q':
            while par not in list(df.columns.values):
                print("Nie istnieje taki parametr, podaj poprawny parametr")
                par = input()
            parameters.append(par)

    return parameters

def regressionall(df):
    Y = makeratio(df)
    list=df.columns.values.tolist()
    if("Team" in list):
        list.remove("Team")
    for col in list:
        X = df[col].values.reshape(-1,1)
        model = LinearRegression().fit(X, Y)
        r_sq = model.score(X, Y)
        print(str(col) + " " + str(r_sq))

def regressionparams(df):
    parameters = makeparams(df)

    Y=makeratio(df)
    X=df.loc[:, parameters]
    model = LinearRegression().fit(X, Y)
    r_sq = model.score(X, Y)
    print(" R^2: ", r_sq, " ", "współczynniki kierunkowe: ", model.coef_ )
 
    print("Czy chcesz dokonać predykcji na sezon 2022? Wpisz 'T' lub 'N' ")
    par = input()
    if par == 'T':
        predict2022(model,parameters)
    elif par != 'N':
                print("Miałeś/aś wpisać 'N' >:( ")

def predict2022(model,parameters):
    df2022 = load2022("2022")
    X2 = df2022.loc[:, parameters]
    Y2 = makeratio(df2022)
    pred=model.predict(X2)
    print("Przewidziane wyniki/faktyczne wyniki:")
    for i in range(0, len(df2022.index)):
        print(str(pred[i]) , " ", str(Y2[i]), str(df2022["Team"][i]))
    Sum=0
    for i in range(0, len(Y2)):
        Sum+= abs(pred[i]-Y2[i])
    avg=Sum/len(Y2)
    print("Średni błąd =", str(avg))

def launchtest():
    conv = list(map(str, list(range(0,48))))
    test=pd.DataFrame(np.random.randn(50,50), index = range(0,50), columns=(['W','L']+ conv ))
    print(test)

    regressionall(test)

    print("Teraz regresja będzie dokonywana względem kolumny 'W'")
    parameters = makeparams(test)

    Y=test['W']
    X=test.loc[:, parameters]
    model = LinearRegression().fit(X, Y)
    r_sq = model.score(X, Y)
    print(" R^2: ", r_sq, " ", "współczynniki kierunkowe: ", model.coef_ )

def helloworld(df):
    print("Program regresji liniowej dla % zwycięstw drużyn NBA")
    par = '36'

    print(df)
    
    while par!= '0':
        print("Jeżeli chcesz dokonać regresji pojedynczej względem każdej statystyki wpisz '1' \n" 
        "jeżeli chcesz dokonać regresji względem wybranych przez siebie statystyk wpisz '2' \n"
        "jeżeli chcesz zakończyć program wpisz '0'")

        par = input()

        if par == '1':
            regressionall(df)

        elif par == '2':
            regressionparams(df)

        elif par == 'T':
            launchtest()
