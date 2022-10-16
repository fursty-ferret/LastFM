from Auth import *
import requests, math, csv, os
from UnixToDate import convert_unix
from openpyxl import load_workbook
from openpyxl.styles import Font, Border, Side, Alignment
from openpyxl.utils import get_column_letter, column_index_from_string

def main():
    filename = 'TopArtists.xlsx'
    wb = load_workbook(filename)
    ws = wb['Weekly Charts']
    for j in range(355,922):
        # j = int(input("What week to input? 919 = 02/10/22 "))
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
            wcl = [t, total, unique]
            for i in range(0,3):
                    name = artist[i]['name']
                    playcount = int(artist[i]['playcount'])
                    percentage = int(playcount)/total
                    results = [name, playcount, percentage]
                    wcl.extend(results)
            row = str(ws.max_row + 1)
            fontObj = Font(bold=True)
            aborder = Border(left=Side(border_style='dashed'), right=Side(border_style='medium'), bottom=Side(border_style='dashed'), top=Side(border_style='dashed'))
            cellborder = Border(left=Side(border_style='dashed'), right=Side(border_style='dashed'), bottom=Side(border_style='dashed'), top=Side(border_style='dashed'))
            ws.row_dimensions[int(row)].height = 25
            column_widths = [15, 8, 8, 30, 5, 5, 30, 5, 5, 30, 5, 5]
            for cells in range(0,12):
                column = str(get_column_letter(cells+1))
                ws.column_dimensions[column].width = column_widths[cells]
                cell = column + row
                ws[cell].alignment = Alignment(horizontal='center', vertical='center')
                ws[cell].border = cellborder
                ws[cell] =  wcl[cells]
            ws['A'+row].font, ws['A'+row].border = fontObj, aborder
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