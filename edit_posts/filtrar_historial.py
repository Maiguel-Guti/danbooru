import pandas as pd
import datetime as dt

pd.options.mode.chained_assignment = None  # default='warn'

'''
Filtra el historial exportado de Microsoft edge para contener solo los resultados
en cierto intervalo de fechas y obtener los IDs de posts de Danbooru que se 
quieren modificar.
'''

def create_date_string(year:int, month:int, day:int, hours:int, minutes: int, seconds:int = 0)-> tuple[str]:
    # Returns as string, not datetime object
    date = dt.date(year, month, day).strftime(r'%Y-%m-%d')
    time = dt.time(hours, minutes, seconds).strftime(r'%H:%M:%S')

    return (date, time)

def filter_by_date_old(df: pd.DataFrame, after_date:str, before_date:str) -> pd.DataFrame:

    # Filters dataframe of MicroEdge browsing history export by date interval, doesn't take account for microseconds

    df['DateTime'] = pd.to_datetime(df['DateTime'].str[:19]) # yyyy-mm-ddThh:mm:ss

    filter_mask_after_date =  ((df['DateTime'].dt.date == after_date[0])  & (df['DateTime'].dt.time >= after_date[1]))

    if before_date != None:
        filter_mask_between_dates = ((df['DateTime'].dt.date > after_date[0]) & (df['DateTime'].dt.date < before_date[0]))
        filter_mask_before_date = ((df['DateTime'].dt.date == before_date[0]) & (df['DateTime'].dt.time <= before_date[1]))
        filter_mask = filter_mask_between_dates | (filter_mask_after_date & filter_mask_before_date) 
    else:
        filter_mask = filter_mask_after_date

    filtered_df = df[filter_mask]

    if filtered_df.empty: print('Date filter returned an empty dataframe')

    return filtered_df

def filter_by_date(df: pd.DataFrame, after_date, before_date) -> pd.DataFrame:

    #df['DateTime'] = pd.to_datetime(df['DateTime'].str[:19])
    df['DateTime'] = pd.to_datetime(df['DateTime']).dt.tz_localize(None)
    df.set_index('DateTime', inplace= True) # Sets datetime as index (pandas.DateTimeIndex), allows very fasts filters
    
    if after_date[0] == before_date[0]:
        # Este es el caso de que el filtro sea de dos fechas en el mismo dia 
        filtered_df = df.loc[after_date[0]].between_time(after_date[1], before_date[1])
    else:
        print(df.index < '2025-03-24') # Se permite esta clase de comparaciones con el indice
        raise Exception('TODAVIA NO IMPLEMENTO ESTA PVTA MIERDA')
         #filtered_df = df.loc[filter1 & filter2] ###### get_loc()??

    print(df.shape[0] - filtered_df.shape[0], ' rows removed by date filter')
    if filtered_df.empty: print('Date filter returned an empty dataframe')

    return filtered_df

def filter_by_danbooru_posts(df: pd.DataFrame, test: bool) -> pd.DataFrame:

    # Filters dataframe of MicroEdge browsing history export by url that belongs to Danbooru or Testbooru posts

    df.rename(columns={'NavigatedToUrl': 'PostID'}, inplace= True)
    if df.empty: return df

    if test:
        filtered_df = df[df['PostID'].str[:34] == 'https://testbooru.donmai.us/posts/']
        filtered_df['PostID'] = filtered_df['PostID'].str[34:]

    else:
        filtered_df = df[df['PostID'].str[:33] == 'https://danbooru.donmai.us/posts/']
        filtered_df['PostID'] = filtered_df['PostID'].str[33:]

    # Get just post ID from URL

    if filtered_df.empty: 
        print('No posts found in the interval given')
        return filtered_df

    filtered_df['PostID'] = filtered_df['PostID'].str.split('?', expand=True)[0]

    print(df.shape[0] - filtered_df.shape[0], ' rows removed by posts filter')
    if filtered_df.empty: print('No posts found in the interval given')

    return filtered_df

def main(FILE: str, after_date, before_date, TEST: bool = True) -> list:

    if (after_date[0] > before_date[0]):
        raise Exception('- Error: before_date must be a date before after_date')
    elif (after_date[0] == before_date[0]) and (after_date[1] > before_date[1]):
        raise Exception('- Error: before_date time must be earlier than after_date')

    df: pd.DataFrame = pd.read_csv(FILE, usecols=['DateTime', 'NavigatedToUrl'])
    print('Filtering {0} registers'.format(df.shape[0]), after_date, before_date)

    df = filter_by_date(df, after_date, before_date)

    df = filter_by_danbooru_posts(df, test= TEST)
    
    print(df, '\n', df.shape[0], ' datos')

    output =  list(df['PostID'])

    return set(output)

if __name__ == '__main__':

    archivo = r'C:\Users\Usuario\Desktop\Programacion\Python\Online\danbooru_resources\historial\BrowserHistory.csv'
    AFTER_DATE = create_date_string(2025, 3, 24, hours=20, minutes=16, seconds=0)
    BEFORE_DATE = create_date_string(2025, 3, 24, hours=20, minutes=18, seconds=0)

    main(archivo, AFTER_DATE, BEFORE_DATE, TEST= False)