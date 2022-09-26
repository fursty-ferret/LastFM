from Auth import *
import requests, math, csv
from UnixToDate import convert_unix

def main():
    with open('TopArtists.csv','a') as csvfile:
        fieldnames = ['week','total_plays','unique_artists','artist1','playcount1','percentage1','artist2','playcount2','percentage2','artist3','playcount3','percentage3']
        csv_writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        # csv_writer.writeheader()
        for j in range(915,920): # start at 355
            print(j)
            unix = get_from_to(j)
            date_from = unix[0]
            date_to = unix[1]
            artist_url = root + '/2.0/?method=user.getweeklyartistchart&user=' + user + '&api_key=' + API_key + '&format=json' + '&from=' + str(date_from) + '&to=' + str(date_to)
            r = requests.get(artist_url)
            rjson = r.json()
            weeklyartistchart = rjson['weeklyartistchart']
            artist = weeklyartistchart['artist']
            if len(artist) < 3:
                continue
            else:
                total = 0
                for l in range(len(artist)):
                    playcount = artist[l]['playcount']
                    total += int(playcount)
                f = convert_unix(date_from)
                t = convert_unix(date_to)
                unique = len(artist)
                new_dict = {}
                new_dict.update({
                    'week':t,
                    'total_plays':total,
                    'unique_artists':unique
                    })
                for i in range(0,3):
                        name = artist[i]['name']
                        playcount = artist[i]['playcount']
                        percentage1 = int(playcount)/total
                        percentage2 = percentage1 * 100
                        percentage = math.ceil(percentage2)
                        new_dict.update({
                            (f'artist{i+1}'): name,
                            (f'playcount{i+1}'): playcount,
                            (f'percentage{i+1}'): percentage
                            })
                csv_writer.writerow(new_dict)
                print(f'Written {j}')
                print('Complete')

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