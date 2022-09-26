from Auth import *
import requests
from UnixToDate import convert_unix

def main():
    for i in range(0,915):
        print(i)
        try:
            unix = get_from_to(i)
            date_from = unix[0]
            date_to = unix[1]
            artist_url = root + '/2.0/?method=user.getweeklyartistchart&user=' + user + '&api_key=' + API_key + '&format=json' + '&from=' + str(date_from) + '&to=' + str(date_to)
            r = requests.get(artist_url)
            rjson = r.json()
            weeklyartistchart = rjson['weeklyartistchart']
            artist = weeklyartistchart['artist']
            f = convert_unix(date_from)
            t = convert_unix(date_to)
            new_dict = {}
            new_dict.update({
                'from':f,
                'to':t
                })
            for i in range(0,3):
                name = artist[i]['name']
                rank1 = artist[i]['@attr']
                rank = rank1['rank']
                playcount = artist[i]['playcount']
                new_dict.update({
                    (f'artist{i+1}'): name,
                    (f'playcount{i+1}'): playcount
                    })
            print(new_dict)
            print(f'Completed {i}')
        except IndexError:
            print(f'Tried {i}, continuing')
            continue


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