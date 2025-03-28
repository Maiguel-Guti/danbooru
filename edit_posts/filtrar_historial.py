import pandas as pd
import datetime as dt

pd.options.mode.chained_assignment = None  # default='warn'

'''
Filtra el historial exportado de Microsoft edge para contener solo los resultados
en cierto intervalo de fechas y obtener los IDs de posts de Danbooru que se 
quieren modificar.
'''

def create_date_string(DATE: list[int], TIME: list[int])-> tuple[str]:
    # Returns as string, not datetime object
    date = dt.date(DATE[0], DATE[1], DATE[2]).strftime(r'%Y-%m-%d')
    time = dt.time(TIME[0], TIME[1], TIME[2]).strftime(r'%H:%M:%S')
    date_time = dt.datetime(DATE[0], DATE[1], DATE[2], TIME[0], TIME[1], TIME[2]).strftime(r'%Y-%m-%d %H:%M:%S')

    return (date, time, date_time)

def filter_by_date(df: pd.DataFrame, after_date, before_date) -> pd.DataFrame:

    # metodo alternativo: usar df['DateTime'].dt.date / dt.time
    #

    df['DateTime'] = pd.to_datetime(df['DateTime']).dt.tz_localize(None) #.str[:19] to get datetime without miliseconds
    df.set_index('DateTime', inplace= True) # Sets datetime as pandas.DateTimeIndex

    if after_date[0] == before_date[0]: # same day case
        filtered_df = df.loc[after_date[0]].between_time(after_date[1], before_date[1])
    else:
        df.index.get_loc('yyyy-mm-dd hh:mm:ss') # tambien se puede recortar a hh:mm

         #filtered_df = df.loc[filter1 & filter2] ###### get_loc()??

    print(df.shape[0] - filtered_df.shape[0], ' rows removed by date filter')
    if filtered_df.empty: print('Date filter returned an empty dataframe')
    '''
    NOTAS: CAMBIAR CREATE DATE PARA DEVOLVER OBJETO DE DATETIME Y SOLO CONVERTIR A TEXTO DENTRO DE ESTA FUNCION?
    '''
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

def date_verifier(after_date, before_date):

    if (after_date[0] > before_date[0]):
        raise Exception('- Error: before_date must be a date before after_date')
    
    elif (after_date[0] == before_date[0]) and (after_date[1] > before_date[1]):
        raise Exception('- Error: before_date time must be earlier than after_date')
    
    else: return

def main(FILE: str, after_date, before_date, TEST: bool = True) -> set:

    date_verifier(after_date, before_date)

    df: pd.DataFrame = pd.read_csv(FILE, usecols=['DateTime', 'NavigatedToUrl'])
    print('Filtering {0} registers'.format(df.shape[0]), after_date, before_date)

    df = filter_by_date(df, after_date, before_date)
    pass
    df = filter_by_danbooru_posts(df, test= TEST)
    
    print(df, '\n', df.shape[0], ' datos')

    output =  list(df['PostID'])

    return set(output)

if __name__ == '__main__':

    archivo = r'C:\Users\Usuario\Desktop\Programacion\Python\Online\danbooru_resources\historial\BrowserHistory.csv'

    dia = (2025, 3, 25)
    AFTER_DATE = create_date_string(dia, (16, 34, 0))
    BEFORE_DATE = create_date_string(dia, (16, 40, 0))

    print(main(archivo, AFTER_DATE, BEFORE_DATE, TEST= False))