from scrapeutils import pgatour

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
            golfer_data = user.t.field['players'][golfer]
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
                if i == user.t.current_round():
                    if golfer_data['status'] == 'cut':
                        if i < 3:
                            score = int(self.__team[golfer]['day' + str(i)]) - int(self.__t.get_par())
                            if score == 0:
                                f.write('        <td align="center">E</td>')
                            else:
                                f.write('        <td align="center">%+d</td>' % score)
                        else:
                            f.write('        <td align="center">---</td>')
                    elif golfer_data['today'] is None:
                        if i == 4:
                            f.write('        <td align="center">{}</td>'.format(golfer_data['tee_time']))
                        else:
                            f.write('        <td align="center">---</td>')
                    elif golfer_data['today'] == 0:
                        f.write('        <td align="center">E (%s)</td>' % golfer_data['thru'])
                    else:
                        f.write('        <td align="center">%+d (%s)</td>' % (int(golfer_data['today']),
                                                                              golfer_data['thru']))
                elif golfer_data['current_round'] is None and golfer_data['status'] == 'active':
                    f.write('        <td align="center">---</td>')
                elif i > user.t.current_round():
                    f.write('        <td align="center">---</td>')
                elif golfer_data['rounds'][i-1] is None:
                    f.write('        <td align="center">---</td>')
                else:
                    score = int(golfer_data['rounds'][i-1]) - int(user.t.par())
                    if score == 0:
                        f.write('        <td align="center">E</td>')
                    else:
                        f.write('        <td align="center">%+d</td>' % score)

            if type(golfer_data['penalty']) == int:
                f.write('    <td align="center">%+d</td>' % golfer_data['penalty'])
            else:
                f.write('    <td align="center">%s</td>' % golfer_data['penalty'])

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

