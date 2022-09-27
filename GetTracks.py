from Auth import *
import requests, math, csv, os
from UnixToDate import convert_unix
from openpyxl import load_workbook

def main():
    filename = 'TopArtists.xlsx'
    wb = load_workbook(filename)
    ws = wb['Weekly Charts']
    j = int(input("What week to input? 919 = 02/10/22 "))
    unix = get_from_to(j)
    date_from = unix[0]
    date_to = unix[1]
    artist_url = root + '/2.0/?method=user.getweeklyartistchart&user=' + user + '&api_key=' + API_key + '&format=json' + '&from=' + str(date_from) + '&to=' + str(date_to)
    r = requests.get(artist_url)
    rjson = r.json()
    weeklyartistchart = rjson['weeklyartistchart']
    artist = weeklyartistchart['artist']
    f = convert_unix(date_from)
    t = convert_unix(date_to)
    print(f'Starting {j}, week ending {t}')
    if len(artist) < 3:
        print("Not enough artists recorded this week")
    else:
        total = 0
        for l in range(len(artist)):
            playcount = artist[l]['playcount']
            total += int(playcount)
        unique = len(artist)
        new_dict = {}
        new_dict.update({
            'week':t,
            'total_plays':total,
            'unique_artists':unique
            })
        for i in range(0,3):
                name = artist[i]['name']
                playcount = int(artist[i]['playcount'])
                percentage1 = int(playcount)/total
                percentage2 = percentage1 * 100
                percentage = math.ceil(percentage2)
                new_dict.update({
                    (f'artist{i+1}'): name,
                    (f'playcount{i+1}'): playcount,
                    (f'percentage{i+1}'): percentage
                    })
        weeklychartlist = [new_dict['week'],
        new_dict['total_plays'],
        new_dict['unique_artists'],
        new_dict['artist1'],
        new_dict['playcount1'],
        new_dict['percentage1'],
        new_dict['artist2'],
        new_dict['playcount2'],
        new_dict['percentage2'],
        new_dict['artist3'],
        new_dict['playcount3'],
        new_dict['percentage3']
        ]
        ws.append(weeklychartlist)
        print(f'Written {j}')
        print(f'Complete {t}')
    wb.save(filename)

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