from Auth import *
import requests
import pandas as pd

def main():
    url = root + '2.0/?method=user.gettopartists&user=' + user + '&api_key=' + API_key + '&format=json&'
    response = requests.get(url)
    data = response.json()
    top_artists = data['topartists']['artist']
    artlist = []
    pclist = []
    for i in range(len(top_artists)):
        artist = top_artists[i]['name']
        playcount = top_artists[i]['playcount']
        artlist.append(artist)
        pclist.append(playcount)
    dict = {'artist':artlist,'playcount':pclist}
    df = pd.DataFrame(dict)
    print(df.describe())

if __name__ == '__main__':
    main()