import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import argparse
import pathlib
import random
import NBA_module as nb


parser=argparse.ArgumentParser(description = "Podaj folder ze statystykami, każdy rodzaj statystyk Per Game, Per Possession i Advanced powinien być w oddzielnym folderze, pliki statystyk zaawansowanych powinny zawierać w nazwach 'adv' ")
parser.add_argument("-adv", "--FolderAdv", help="folder ze statystykami zaawansowanymi", default= pathlib.Path(__file__).parent.resolve() )
parser.add_argument("-g", "--FolderPerGame", help="folder ze statystykami per game", default= pathlib.Path(__file__).parent.resolve() )
parser.add_argument("-p", "--FolderPerPoss", help="folder ze statystykami per possesion", default= pathlib.Path(__file__).parent.resolve() )
parser.add_argument("-f", "--Folder2022", help="folder ze statystykami z 2022, upewnij się, że pliki ze statystykami Per Possession i Advanced zawierają w nazwach odpowiednio 'poss' i 'adv' ", default= pathlib.Path(__file__).parent.resolve() )
args = parser.parse_args()

df1=loadfolder(args.FolderAdv)
df2=loadfolder(args.FolderPerPoss)
df3=loadfolder(args.FolderPerGame)


#df1=nb.loadfolder("NBA/Adv")
#df2=nb.loadfolder("NBA/PerGame")
#df3=nb.loadfolder("NBA/PerPoss")

df = nb.makedataframe(df1,df2,df3)
nb.helloworld(df)


