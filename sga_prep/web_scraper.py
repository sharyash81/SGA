import pandas as pd 
import requests
from bs4 import BeautifulSoup as bs
import re
import os
from utils import df2json

'''
    extract league table standing from wikipedia using beautifilsoup
'''
def create_leauge_attr_table(league_id , year , link):
    # extract standing table data from wikipedia     
    response = requests.get(link)
    soup = bs(response.text, 'html.parser')
    ht = soup.find_all(['h2','h3','table'])
    h2t = [[ r for r in x.children][0].get_text() if ( x.name == 'h2' or x.name =='h3') else str(x) for x in ht ]
    regex = ["League*.",".*Standings"]
    r = re.compile('|'.join(regex))
    ind = h2t.index(list(filter(r.match,h2t))[0])
    while (not bool(bs(h2t[ind], "html.parser").find())):
        ind+=1
    standing_table = h2t[ind]
    # convert extracted data to data frame 
    df_std = pd.read_html(str(standing_table))
    df_std = pd.DataFrame(df_std[0])
    # data summarizing and cleaning
    df_std = df_std.loc[:,df_std.columns!='Qualification or relegation']
    df_std = df_std[df_std['Team'].notna()]
    df_std = df_std.set_axis([x.split('.')[0].rstrip() for x in df_std.columns] , axis = 1 , copy = False)
    df_std['Pts'] = df_std['Pts'].astype(str).str.extract('(\d+)').astype(int,errors ='ignore')
    df_std['Team'] = df_std['Team'].apply(lambda x : x.split('(')[0].rstrip())
    df.append({'league_id':league_id,'Season':year,'table':df_std})

if __name__ == '__main__':
    print("***** web scraping process starts *****")
    global df
    df = []
    league_id = [1729,4769,7809,10257,13274,15722,17642,19694,21518,24558]
    league_name = [ 'Premier_League',
                    'Ligue_1',
                    'Bundesliga',
                    'Serie_A',
                    'Eredivisie',
                    'Ekstraklasa',
                    'Primeira_Liga',
                    'Scottish_Premier_League',
                    'La_Liga',
                    'Swiss_Super_League']
    

    for ind,league in enumerate(league_name):  
        for start_date in range(8,17):
            season = f'20{start_date:02}%E2%80%93{start_date+1:02}'
            link = f'https://en.wikipedia.org/wiki/{season}_{league}'
            try:
                create_leauge_attr_table(league_id[ind],f'20{start_date:02}/{start_date+1:02}', link)
            except:
                continue


    df = pd.DataFrame(df)
    os.system("touch jsonCols/League.json")
    df2json(df, "jsonCols/League.json")
    print("***** web scraping ends successfully *****")
