import pandas as pd

first = pd.read_excel('stationData.xlsx')
first.to_csv('stationData.csv', sep=';')
