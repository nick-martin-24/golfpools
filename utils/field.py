import urllib
import gpftp
import requests
from bs4 import BeautifulSoup


def generate_field_html(field_url, output, filename, ftp):
    f = requests.get(field_url)
    parsed_json = f.json()
    players = parsed_json['Tournament']['Players']
    player_names = []
    for item in players:
        name = item['PlayerName'].split(', ')
        player_names.append(' '.join((name[1], name[0])))

    url = 'http://www.owgr.com/ranking?pageNo=1&pageSize=300$country=All'
    h = urllib.request.urlopen(url)
    html = h.read()
    soup = BeautifulSoup(html, 'html.parser')

    tr = soup.find_all('tr')
    tr = tr[1:]
    owgr = []
    count = 0
    for item in tr:
        name = item.contents[9].contents[0].contents[0]
        if name[0:6] == 'Rafael':
            name = 'Rafa Cabrera Bello'
        if name == 'Peter Uihlein':
            continue
        if name in player_names and count < 60:
            owgr.append(name)
            count += 1

    a = owgr[0:10]
    b = owgr[10:25]
    c = owgr[25:40]
    d = owgr[40:]

    f = open(filename, 'w')
    header = '''<html>
    <head>
    <style>
    table, th, td {
        border: 1px solid black;
    }
    </style>
    </head>
    '''

    body_head = '''
    <body>
    
    <form id="frm1" action = "team_creation.php" method="post">
        <br><br>Your Name: <input type="text" name="user"><br><br><br>
        
        <table style="width:80%">
    '''
    table_header = '''
            <tr>
                <td>Group A (Select 2)</td>
                <td>Group B (Select 3)</td>
                <td>Group C (Select 2)</td>
                <td>Group D (Select 2)</td>
            </tr>
    '''

    one_to_ten = ''
    for i in range(0, 10):
        one_to_ten += '''
            <tr>
                <td>input type="checkbox" name="a[]" value"''' + a[i] + '''">''' + a[i] + '''</td>
                <td>input type="checkbox" name="b[]" value"''' + b[i] + '''">''' + b[i] + '''</td>
                <td>input type="checkbox" name="c[]" value"''' + c[i] + '''">''' + c[i] + '''</td>
                <td>input type="checkbox" name="d[]" value"''' + d[i] + '''">''' + d[i] + '''</td>
            </tr>
    '''

    eleven_to_fifteen = ''
    for i in range(10, 15):
        eleven_to_fifteen += '''
            <tr>
                <td> </td>
                <td>input type="checkbox" name="b[]" value"''' + b[i] + '''">''' + b[i] + '''</td>
                <td>input type="checkbox" name="c[]" value"''' + c[i] + '''">''' + c[i] + '''</td>
                <td>input type="checkbox" name="d[]" value"''' + d[i] + '''">''' + d[i] + '''</td>
            </tr>
    '''

    sixteen_to_twenty = ''
    for i in range(10, 15):
        sixteen_to_twenty += '''
            <tr>
                <td> </td>
                <td> </td>
                <td> </td>
                <td>input type="checkbox" name="d[]" value"''' + d[i] + '''">''' + d[i] + '''</td>
            </tr>
    '''

    footer = '''
        </table><br>
        Tiebreaker: <input type="text" name="tiebreaker"> (Strokes to par of the winning golfer, i.e. -5, -13)<br><br>
    </form>
    '''

    f.write(header)
    f.write(body_head)
    f.write(table_header)
    f.write(one_to_ten)
    f.write(eleven_to_fifteen)
    f.write(sixteen_to_twenty)
    f.write(footer)
    f.close()

    gpftp.upload_file_to_ftp(output, 'field.html', ftp)
