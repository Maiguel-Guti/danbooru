import pandas 
import datetime

df: pandas.DataFrame = pandas.read_csv('Historial\BrowserHistory_23_03_25.csv')

df['NavigatedToUrl']
print(datetime.date(df['DateTime'][0][:10]))
print(df['DateTime'][0][11:19])