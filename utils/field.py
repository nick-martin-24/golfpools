import urllib
import gpftp
import requests
from bs4 import BeautifulSoup


def generate_field_html(output_directory, filename, ftp_directory):
    field_url = get_current_field_url()
    player_names = get_current_field(field_url)
    owgr = get_top_60_in_current_field(player_names)

    # define tiers
    a = owgr[0:10]
    b = owgr[10:25]
    c = owgr[25:40]
    d = owgr[40:]
    write_field_html(filename, a, b, c, d)
    gpftp.upload_file_to_ftp(output_directory, 'field.html', ftp_directory)


def get_current_field_url():
    schedule = 'https://statdata.pgatour.com/r/current/schedule-v2.json'
    schedule_json = requests.get(schedule).json()
    week = str(int(schedule_json['thisWeek']['weekNumber']) + 1)
    year = schedule_json['years'][1]
    tour = year['tours'][0]
    current_tournament = next(item for item in tour['trns'] if item['date']['weekNumber'] == week
                              and item['primaryEvent'] == 'Y')
    tournament_code = current_tournament['permNum']
    return 'https://statdata.pgatour.com/r/{}/field.json'.format(tournament_code)


def get_current_field(field_url):
    # set player names from field of current tournament
    f = requests.get(field_url)
    parsed_json = f.json()
    players = parsed_json['Tournament']['Players']
    player_names = []
    for item in players:
        name = item['PlayerName'].split(', ')
        player_names.append(' '.join((name[1], name[0])))
    return player_names


def get_top_60_in_current_field(player_names):
    # get players from owgr and set the top 60 who are in the field of current tournament
    # url = 'http://www.owgr.com/ranking?pageNo=1&pageSize=300$country=All'
    url = 'http://www.owgr.com/ranking'
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
        if name in player_names and count < 60 and name != 'Scottie Scheffler':
            owgr.append(name)
            count += 1
    return owgr


def write_field_html(filename, a, b, c, d):
    # write html file
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
                <td><input type="checkbox" name="a[]" value"''' + a[i] + '''">''' + a[i] + '''</td>
                <td><input type="checkbox" name="b[]" value"''' + b[i] + '''">''' + b[i] + '''</td>
                <td><input type="checkbox" name="c[]" value"''' + c[i] + '''">''' + c[i] + '''</td>
                <td><input type="checkbox" name="d[]" value"''' + d[i] + '''">''' + d[i] + '''</td>
            </tr>
    '''

    eleven_to_fifteen = ''
    for i in range(10, 15):
        eleven_to_fifteen += '''
            <tr>
                <td> </td>
                <td><input type="checkbox" name="b[]" value"''' + b[i] + '''">''' + b[i] + '''</td>
                <td><input type="checkbox" name="c[]" value"''' + c[i] + '''">''' + c[i] + '''</td>
                <td><input type="checkbox" name="d[]" value"''' + d[i] + '''">''' + d[i] + '''</td>
            </tr>
    '''

    sixteen_to_twenty = ''
    for i in range(10, 15):
        sixteen_to_twenty += '''
            <tr>
                <td> </td>
                <td> </td>
                <td> </td>
                <td><input type="checkbox" name="d[]" value"''' + d[i] + '''">''' + d[i] + '''</td>
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


def generate_php_file(output_directory, ftp_directory):
    filename = '{}/team_creation.php'.format(output_directory)
    f = open(filename, 'w')
    header = '''<html>
    <body>
    '''

    php = '''
    <?php
    $a = count($_POST['a']);
    $b = count($_POST['b']);
    $c = count($_POST['c']);
    $d = count($_POST['d']);
    
    if ($a != 2) {
        echo "Incorrect number of golfers (\\"" . $a . "\\") in Group A. Must select 2 players. <br><a href=\\"#\\" onclick=\\"history.back();\\">Please try again</a>":
    } elseif ($b != 3) {
        echo "Incorrect number of golfers (\\"" . $b . "\\") in Group B. Must select 3 players. <br><a href=\\"#\\" onclick=\\"history.back();\\">Please try again</a>":
    } elseif ($c != 2) {
        echo "Incorrect number of golfers (\\"" . $c . "\\") in Group C. Must select 2 players. <br><a href=\\"#\\" onclick=\\"history.back();\\">Please try again</a>":
    } elseif ($d !2) {
        echo "Incorrect number of golfers (\\"" . $d . "\\") in Group D. Must select 2 players. <br><a href=\\"#\\" onclick=\\"history.back();\\">Please try again</a>":
    } elseif (!isset($_POST['user']) || trim($_POST['user']) == '') {
        echo "Team name was left blank. <br><a href=\\"#\\" onclick=\\"history.back();\\">Please try again</a>";
    } elseif (!isset($_POST['tiebreaker']) || trim($_POST['tiebreaker']) == '') {
        echo "Tiebreaker was left blank. <br><a href=\\"#\\" onclick=\\"history.back();\\">Please try again</a>";
    } else {
        $filename = str_replace(' ', '', $_POST["user"] . '.txt');
        $checked_count = 0;
        $post_length = count($_POST);
        $roster = array();
        echo "Your team has been submitted.\\n";
        echo "<br><a href=\\"" . str_replace(' ', '', $_POST["user"] . '.html') . "\\">Go to your team</a> (Allow up to 2 minutes for update)\\n";
        echo "<br><a href=\\"leaderboard.html\\">Go to Leaderboard</a>\\n";
        echo "<br><a href=\\"../../\\">Go to Homepage</a>\\n";
        foreach($_POST as $input) {
            if (is_array($input)) {
                foreach($input as $item) {
                    $roster[$checked_count] = $item;
                    $checked_count = $checked_count + 1;
                }
            }
        }
        
        $data = $_POST["user"] . ': ' . $roster[0] . ", " . $roster[1] . ", " . $roster[2] . ", " . $roster[3] . ", " . $roster[4] . ", " . $roster[5] . ", " . $roster[6] . ", " . $roster[7] . ", " . $roster[8] . ': ' . $_POST["tiebreaker"];
        file_put_contents("teams/" . $filename, $data);
        $creation_page_text = "<html><head><meta http-equiv=\\"refresh\\" content=\\"20\\" /></head>Creating team page. Please allow up to 2 minutes for roster to appear.</html>";
        file_put_contents(str_replace(' ','',$_POST["user"] . '.html'), $creation_page_text);
    }
    ?>
    '''

    footer = '''
    </body>
    </html>
    '''

    f.write(header)
    f.write(php)
    f.write(footer)
    f.close()

    gpftp.upload_file_to_ftp(output_directory, 'team_creation.php', ftp_directory)
