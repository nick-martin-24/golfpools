import datetime


def write_field_html(filename, field):
    a = field['a']
    b = field['b']
    c = field['c']
    d = field['d']

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
                <td><input type="checkbox" name="a[]" value="''' + a[i] + '''">''' + a[i] + '''</td>
                <td><input type="checkbox" name="b[]" value="''' + b[i] + '''">''' + b[i] + '''</td>
                <td><input type="checkbox" name="c[]" value="''' + c[i] + '''">''' + c[i] + '''</td>
                <td><input type="checkbox" name="d[]" value="''' + d[i] + '''">''' + d[i] + '''</td>
            </tr>
    '''

    eleven_to_fifteen = ''
    for i in range(10, 15):
        eleven_to_fifteen += '''
            <tr>
                <td> </td>
                <td><input type="checkbox" name="b[]" value="''' + b[i] + '''">''' + b[i] + '''</td>
                <td><input type="checkbox" name="c[]" value="''' + c[i] + '''">''' + c[i] + '''</td>
                <td><input type="checkbox" name="d[]" value="''' + d[i] + '''">''' + d[i] + '''</td>
            </tr>
    '''

    sixteen_to_twenty = ''
    for i in range(15, 20):
        sixteen_to_twenty += '''
            <tr>
                <td> </td>
                <td> </td>
                <td> </td>
                <td><input type="checkbox" name="d[]" value="''' + d[i] + '''">''' + d[i] + '''</td>
            </tr>
    '''

    footer = '''
        </table><br>
        Tiebreaker: <input type="text" name="tiebreaker"> (Strokes to par of the winning golfer, i.e. -5, -13)<br><br>
        <input type="submit" value="Submit">
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


def write_php(filename):
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
        echo "Incorrect number of golfers (\\"" . $a . "\\") in Group A. Must select 2 players. <br><a href=\\"#\\" onclick=\\"history.back();\\">Please try again</a>";
    } elseif ($b != 3) {
        echo "Incorrect number of golfers (\\"" . $b . "\\") in Group B. Must select 3 players. <br><a href=\\"#\\" onclick=\\"history.back();\\">Please try again</a>";
    } elseif ($c != 2) {
        echo "Incorrect number of golfers (\\"" . $c . "\\") in Group C. Must select 2 players. <br><a href=\\"#\\" onclick=\\"history.back();\\">Please try again</a>";
    } elseif ($d !=2) {
        echo "Incorrect number of golfers (\\"" . $d . "\\") in Group D. Must select 2 players. <br><a href=\\"#\\" onclick=\\"history.back();\\">Please try again</a>";
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


def write_user_html(user):
        f = open(user.full_html, 'w')
        header = '''<html>
        <head>
            <title>''' + user.name + '''</title>
            <meta http-equiv="refresh" content="20" /></head>
        </head>
        '''

        body_start = '''
        <body>
        <h2>''' + user.name + '''</h2>
        '''

        table_start = '''
        <table border="3" cellspacing="1" cellpadding="1">
        <caption>Roster</caption>

        <tr>
            <td><b>Golfer</b></td>
            <td><b>Total</b></td>
            <td><b>Round 1</b></td>
            <td><b>Round 2</b></td>
            <td><b>Round 3</b></td>
            <td><b>Round 4</b></td>
            <td><b>Penalty</b></td>
        </tr>
        '''

        f.write(header)
        f.write(body_start)
        f.write(table_start)

        for golfer in user.roster:
            golfer_data = user.t.data['players'][golfer]
            f.write('    <tr>')
            if golfer_data['status'] == 'cut':
                f.write('        <td>%s*</td>' % golfer)
            else:
                f.write('        <td>%s</td>' % golfer)

            if golfer_data['total_strokes'] is None:
                f.write('        <td align="center">---</td>')
            elif golfer_data['total'] == 0:
                f.write('        <td align="center">E</td>')
            else:
                f.write('        <td align="center">%+d</td>' % golfer_data['total'])

            for i in range(1, 5):
                if i == user.t.data['current_round']:
                    if golfer_data['status'] == 'cut':
                        if i < 3:
                            score = golfer_data['day{}'.format(i-1)]
                            if score == 0:
                                f.write('        <td align="center">E</td>')
                            else:
                                f.write('        <td align="center">%+d</td>' % score)
                        else:
                            f.write('        <td align="center">---</td>')
                    elif golfer_data['today'] is None:
                        if i == 4:
                            f.write('        <td align="center">{}</td>'.format(golfer_data['rounds'][i-1]['tee_time']))
                        else:
                            f.write('        <td align="center">---</td>')
                    elif golfer_data['today'] == 0:
                        f.write('        <td align="center">E (%s)</td>' % golfer_data['thru'])
                    else:
                        f.write('        <td align="center">%+d (%s)</td>' % (int(golfer_data['today']),
                                                                              golfer_data['thru']))
                elif i >= 3 and golfer_data['status'] == 'cut':
                    f.write('        <td align="center">---</td>')
                elif golfer_data['current_round'] is None and golfer_data['status'] == 'active':
                    f.write('        <td align="center">---</td>')
                elif i > user.t.data['current_round']:
                    f.write('        <td align="center">---</td>')
                elif golfer_data['rounds'][i-1] is None or golfer_data['rounds'][i-1] == '---':
                    f.write('        <td align="center">---</td>')
                else:
                    score = (golfer_data['rounds'][i-1]['strokes'] or user.t.data['par']) - user.t.data['par']
                    if score == 0:
                        f.write('        <td align="center">E</td>')
                    else:
                        f.write('        <td align="center">%+d</td>' % score)

            if golfer_data['penalty'] != 0 and golfer_data['penalty'] is not None:
                f.write('    <td align="center">%+d</td>' % golfer_data['penalty'])
            else:
                f.write('    <td align="center">---</td>')

            f.write('    </tr>')

        tiebreaker = '''
        <tr>
            <td>Tiebreaker</td>
            <td align="center">''' + user.tiebreaker + '''</td>
        '''

        table_end = '''
        </table>
        '''

        asterisk = '''
        * = golfer missed cut; number of strokes over cut has been added to their total score
        '''

        holes_completed = '''
        <br>(#) = holes completed today
        '''

        leaderboard_link = '''
        <br><a href="leaderboard.html">Back to Leaderboard</a>
        '''

        body_end = '''
        </body>
        </html>
        '''

        f.write(tiebreaker)
        f.write(table_end)
        f.write(asterisk)
        f.write(holes_completed)
        f.write(leaderboard_link)
        f.write(body_end)

        f.close()



def write_leaderboard_html(t):
    f = open(t.files['leaderboard-html'], 'w')
    header = '''<!DOCTYPE html>
    <html>


    <head>
    <title>''' + t.data['name'] + '''</title>
    <meta http-equiv="refresh" content="20" />
    </head>
    <body>
    '''
#    <?php echo date('l, F jS, Y'); ?>
#    <?php
#    $handle = fopen("counter.txt", "r");
#    if(!$handle){
#      echo "could not open the file" ;
#    }
#    else {
#          $counter = ( int ) fread ($handle,20) ;
#          fclose ($handle) ;
#          $counter++ ;
#          echo "you are visitor no $counter" ;

#          $handle = fopen("counter.txt", "w" ) ;
#          fwrite($handle,$counter) ;
#          fclose ($handle) ;
#        }
#    ?>
    header += '''
    <h1 align="center">''' + t.data['name'] + '''</h1>
    '''
    f.write(header)

    leaderboard_header = '''
    <table summary="leaderboard" align="left" bgcolor="white" border="3" cellspacing="1" cellpadding="1"
    style="display:inline-block; margin:auto">

    <tr>
    <td colspan="8" align="center">Leaderboard</td>
    </tr>

    <tr>
        <td>Place</td>
        <td>Team</td>
        <td>Total</td>
        <td>Day 1</td>
        <td>Day 2</td>
        <td>Day 3</td>
        <td>Day 4</td>
        <td>Penalty</td>
    </tr>
    '''
    f.write(leaderboard_header)

    place = 1
    last_score = -999
    for person in t.leaderboard:
        f.write('<tr>')
        if place == 1:
            f.write('    <td align="center">%d</td>' % place)
        elif t.leaderboard[person].total == last_score:
            f.write('    <td align="center"></td>')
        else:
            f.write('    <td align="center">%d</td>' % place)

        f.write('    <td>')
        f.write(
            '        <a href="%s.html">%s</a>' % (person, person))
        f.write('    </td>')
        last_score = t.leaderboard[person].total
        place += 1

        if t.leaderboard[person].total == 0:
            f.write('    <td align="center">E</td>')
        else:
            f.write('    <td align="center">%+d</td>' % t.leaderboard[person].total)

        for i in range(1, 5):
            if i > t.data['current_round'] or t.data['is_started'] is False:
                f.write('    <td align="center">---</td>')
            elif t.leaderboard[person].days['day{}'.format(i)] == 0:
                f.write('    <td align="center">E</td>')
            else:
                f.write('    <td align="center">%+d</td>' % t.leaderboard[person].days['day{}'.format(i)])

        if t.leaderboard[person].penalty != 0 and t.leaderboard[person].penalty is not None:
            f.write('    <td align="center">%+d</td>' % t.leaderboard[person].penalty)
        else:
            f.write('    <td align="center">---</td>')

        f.write('</tr>')

    time = datetime.datetime.now().strftime('%I:%M %p')
    date = datetime.datetime.now().strftime('%m-%d-%Y')
    timestamp = '''
        <tr>
            <td colspan="8" align="center">Last updated at ''' + time + ''' on ''' + date + '''</td>
        </tr>
        '''

    winnings_content = ''
    for place in t.payout[str(len(t.leaderboard))].keys():
        if place == 'Last':
            winnings_content += '{}: ${}'.format(place, t.payout[str(len(t.leaderboard))][place])
        else:
            winnings_content += '{}: ${}, '.format(place, t.payout[str(len(t.leaderboard))][place])
 
    winnings = '''
        <tr>
            <td colspan="8" align="center">{}</td>
        </tr>
        '''.format(winnings_content)

    home = '''
        <tr>
            <td colspan="8" align="center"><a href="../../">Home</a></td>
        </tr>
        '''

    create_a_team = '''
        <tr>
            <td colspan="8" align="center"><a href="field.html">Create A Team</a></td>
            </tr>
        '''
    f.write(timestamp)
    f.write(winnings)
    f.write(home)
#    if self.__pl['round_state'] != 'In Progress':
    f.write(create_a_team)
#    f.write('</table>')

    selected_golfer_header = '''
    <table summary="selected_golfer" align="center" bgcolor="white" border="3" cellspacing="1"
    cellpadding="1" style="display:inline-block; margin:auto">

    <tr>
    <td colspan="2" align="center">Selected Golfers</td>
    </tr>

    <tr>
        <td colspan="2">(#)=# of teams w/golfer</td>
    </tr>

    <tr>
        <td align="center">Player</td>
        <td>Total</td>
    </tr>
    '''
    f.write(selected_golfer_header)

    if t.data['is_started']:
        for guy in t.selected_golfers:
            f.write('<tr>')
            f.write('    <td>{} ({})</td>'.format(guy, t.selected_golfers[guy]['count']))

            if t.selected_golfers[guy]['total'] == 0:
                f.write('    <td align="center">E</td>')
            else:
                f.write('    <td align="center">{:+}</td>'.format(t.selected_golfers[guy]['real_total']))

            f.write('</tr>')
        f.write('<tr>')
        f.write('    <td colspan="2" align="center">Scores do not include penalty</td>')
        f.write('</tr>')

    footer = '''
        </table>


        </body>
        </html>
        '''

    f.write(footer)

    f.close()

