import pandas as pd
import datetime as dt

pd.options.mode.chained_assignment = None  # default='warn'

'''
Filtra el historial exportado de Microsoft edge para contener solo los resultados
en cierto intervalo de fechas y obtener los IDs de posts de Danbooru que se 
quieren modificar
'''

def create_date_string(year:int, month:int, day:int, hours:int, minutes: int, seconds:int = 0)-> tuple:

    date = (dt.date(year, month, day), dt.time(hours, minutes, seconds))

    return date

def filter_by_date(df: pd.DataFrame, after_date:str, before_date:str) -> pd.DataFrame:

    # Filters dataframe of MicroEdge browsing history export by date interval, doesn't take account for microseconds
    '''
    df['DateTime'] = pd.to_datetime(df['DateTime'].str[:19]) # yyyy-mm--ddThh:mm:ss
    
    df = df[  (df['DateTime'] >= str(after_date[0]))   &    (df['DateTime'] <= str(before_date[0]))   ]
    filtered_df = df[(df['DateTime'].dt.time >= after_date[1]) & (df['DateTime'].dt.time <= before_date[1])]
    
    filtered_df.set_index('DateTime')
    '''
    df['DateTime'] = pd.to_datetime(df['DateTime'].str[:19])

    filter_mask_between_dates = ((df['DateTime'].dt.date > after_date[0]) & (df['DateTime'].dt.date < before_date[0]))
    filter_mask_after_date =  ((df['DateTime'].dt.date == after_date[0])  & (df['DateTime'].dt.time >= after_date[1]))
    filter_mask_before_date = ((df['DateTime'].dt.date == before_date[0]) & (df['DateTime'].dt.time <= before_date[1]))
    filter_mask =  filter_mask_between_dates | (filter_mask_after_date & filter_mask_before_date) 

    filtered_df = df[filter_mask]

    if filtered_df.empty: print('Date filter returned an empty dataframe')

    return filtered_df

def filter_by_danbooru_posts(df: pd.DataFrame, test: bool) -> pd.DataFrame:

    # Filters dataframe of MicroEdge browsing history export by url that belongs to Danbooru or Testbooru posts

    if df.empty: return df

    if test:
        filtered_df = df[df['NavigatedToUrl'].str[:34] == 'https://testbooru.donmai.us/posts/']
        filtered_df['NavigatedToUrl'] = filtered_df['NavigatedToUrl'].str[34:]

    else:
        filtered_df = df[df['NavigatedToUrl'].str[:33] == 'https://danbooru.donmai.us/posts/']
        filtered_df['NavigatedToUrl'] = filtered_df['NavigatedToUrl'].str[33:]

    # Get just post ID from URL
    filtered_df['NavigatedToUrl'] = filtered_df['NavigatedToUrl'].str.split('?', expand=True)[0]
    filtered_df.rename(columns={'NavigatedToUrl': 'PostID'}, inplace= True)

    if filtered_df.empty: print('Danbooru posts filter returned an empty dataframe')

    return filtered_df

def main(FILE: str, after_date, before_date, TEST: bool = True) -> None:

    if (after_date[0] > before_date[0]):
        raise Exception('- Error: before_date must be a date before after_date')
    elif (after_date[0] == before_date[0]) and (after_date[1] > before_date[1]):
        raise Exception('- Error: before_date time must be earlier than after_date')

    df: pd.DataFrame = pd.read_csv(FILE, usecols=['DateTime', 'NavigatedToUrl'])

    df = filter_by_date(df, after_date, before_date)

    df = filter_by_danbooru_posts(df, test= TEST)
    
    print(df, '\n', df.shape[0], ' datos')
    
    return df

if __name__ == '__main__':

    archivo = r'C:\Users\Usuario\Desktop\Programacion\Python\Online\danbooru_resources\historial\BrowserHistory_23_03_25.csv'
    AFTER_DATE = create_date_string(2025, 3, 23, hours=20, minutes=50, seconds=0)
    BEFORE_DATE = create_date_string(2025, 3, 23, hours=19, minutes=30, seconds=0)

    main(archivo, AFTER_DATE, BEFORE_DATE, TEST= False)