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

