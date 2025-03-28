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
    # If a seconds parameter is not given, assumes TIME length is equal to 2 and returns a string without seconds
    # If a seconds parameter is given, assumes TIME length is equal to 3 and returns a string including seconds

    date = dt.date(DATE[0], DATE[1], DATE[2]).strftime(r'%Y-%m-%d')

    if len(TIME) == 2:
        time = dt.time(TIME[0], TIME[1]).strftime(r'%H:%M')
        date_time = dt.datetime(DATE[0], DATE[1], DATE[2], TIME[0], TIME[1]).strftime(r'%Y-%m-%d %H:%M')
    else:
        time = dt.time(TIME[0], TIME[1], TIME[2]).strftime(r'%H:%M:%S')
        date_time = dt.datetime(DATE[0], DATE[1], DATE[2], TIME[0], TIME[1], TIME[2]).strftime(r'%Y-%m-%d %H:%M:%S')
 
    return (date_time, date, time)


def filter_by_date(df: pd.DataFrame, after_date: tuple[str], before_date) -> pd.DataFrame:

    # metodo alternativo: usar df['DateTime'].dt.date / dt.time
    # If only after_date is given, just applies after_date filter
    # Filter searches index relative to the date given, and returns every partial match
    # This means it can return several indexes in a list, that's why there is a
    # check on type(index) == list

    df['DateTime'] = pd.to_datetime(df['DateTime']).dt.tz_localize(None)
    df.set_index('DateTime', inplace= True) # Sets datetime as pandas.DatetimeIndex

    # Filters df based on after_date and/or before_date values

    if before_date == None: # Only after_date is given case

        index_list_a = df.index.get_loc(after_date[0]) + 1
    
        if len(index_list_a) == 0:
            filtered_df = pd.DataFrame() # If there were no matches, return empty df
            print('No partial match on some date time')
        else:
            index_a = index_list_a[-1] # Return the oldest match
            filtered_df = df[0:index_a]
            print('Revisar que si toma el ultimo valor correctamenTe: \n',filtered_df.tail(n=2))
            
    elif after_date[1] == before_date[1]: # Same day case

        filtered_df = df.loc[after_date[1]].between_time(after_date[2], before_date[2])

    else: # Different days case

        index_list_b = df.index.get_loc(before_date[0]) 
        index_list_a = df.index.get_loc(after_date[0]) + 1

        if (len(index_list_a) == 0) or (len(index_list_b) == 0):
            filtered_df = pd.DataFrame() # If there were no matches, return empty df
            print('No partial match on some date time')
        else:
            index_b = index_list_b[0] # Return the most recent match
            index_a = index_list_a[-1] # Return the oldest match
            filtered_df = df[index_b : index_a] # Browser history goes in reverse order

    print(df.shape[0] - filtered_df.shape[0], ' rows removed by date filter')

    # Returns this print message on error
    if filtered_df.empty: print('Date filter returned an empty dataframe') 

    return filtered_df


def filter_by_danbooru_posts(df: pd.DataFrame) -> pd.DataFrame:

    # Filters dataframe of MicroEdge browsing history export by url that belongs to Danbooru or Testbooru posts

    if df.empty: return df
    df.rename(columns={'NavigatedToUrl': 'PostID'}, inplace= True)

    # Filters registers with a matching URL, and returns what is after said URL
    
    filtered_df = df[df['PostID'].str[:33] == 'https://danbooru.donmai.us/posts/']
    filtered_df['PostID'] = filtered_df['PostID'].str[33:]

    if filtered_df.empty: 
        print('No posts found in the interval given')
        return filtered_df
    
    # Get just post ID from URL

    filtered_df['PostID'] = filtered_df['PostID'].str.split('?', expand=True)[0]

    print(df.shape[0] - filtered_df.shape[0], ' rows removed by posts filter')
    if filtered_df.empty: print('No posts found in the interval given')

    return filtered_df


def date_verifier(after_date, before_date):
    # Verifica que las fechas dadas sean validas

    if after_date == None:
        raise Exception('- Error: after_date must be given')

    if before_date == None: return

    if (after_date[0] > before_date[0]):
        raise Exception('- Error: before_date must be a date prior after_date')
    
    elif (after_date[0] == before_date[0]) and (after_date[1] > before_date[1]):
        raise Exception('- Error: before_date time must be earlier than after_date')
    
    else: return


def main(FILE: str, after_date, before_date) -> set:

    # Filters a csv file of browser history (Microsoft Edge?) and

    date_verifier(after_date, before_date)

    df: pd.DataFrame = pd.read_csv(FILE, usecols=['DateTime', 'NavigatedToUrl'])
    print('Filtering {0} registers'.format(df.shape[0]))

    df = filter_by_date(df, after_date, before_date)
    
    df = filter_by_danbooru_posts(df)
    
    print(df, '\n', df.shape[0], ' datos')

    if df.empty:
        output = []
    else:
        output_list =  list(df['PostID'])
        output = set(output_list)

    return output


if __name__ == '__main__':

    archivo = r'C:\Users\Usuario\Desktop\Programacion\Python\Online\danbooru_resources\historial\BrowserHistory.csv'

    dia = (2025, 3, 27)
    AFTER_DATE = create_date_string((2025, 3, 26), (19, 11))
    BEFORE_DATE = create_date_string(dia, (23, 0))

    print(main(archivo, after_date=AFTER_DATE, before_date=BEFORE_DATE))