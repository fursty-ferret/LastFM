from Auth import *
import requests
from UnixToDate import convert_unix

def main():
    for j in range(355,356):
        print(j)
        unix = get_from_to(j)
        date_from = unix[0]
        date_to = unix[1]
        artist_url = root + '/2.0/?method=user.getweeklyartistchart&user=' + user + '&api_key=' + API_key + '&format=json' + '&from=' + str(date_from) + '&to=' + str(date_to)
        r = requests.get(artist_url)
        rjson = r.json()
        weeklyartistchart = rjson['weeklyartistchart']
        artist = weeklyartistchart['artist']
        if not artist:
            continue
        else:
            f = convert_unix(date_from)
            t = convert_unix(date_to)
            new_dict = {}
            new_dict.update({
                'week':t
                })
            for i in range(0,3):
                    name = artist[i]['name']
                    rank1 = artist[i]['@attr']
                    playcount = artist[i]['playcount']
                    new_dict.update({
                        (f'artist{i+1}'): name,
                        (f'playcount{i+1}'): playcount
                        })
            print(new_dict)

def get_from_to(count):
    chart_url = root + '/2.0/?method=user.getweeklychartlist&user=' + user + '&api_key=' + API_key + '&format=json'
    r = requests.get(chart_url)
    rjson = r.json()
    weeklychartlist = rjson['weeklychartlist']
    chart = weeklychartlist['chart']
    date = chart[count]
    funix = int(date['from'])
    tunix = int(date['to']) 
    return funix, tunix

if __name__ == '__main__':
    main()