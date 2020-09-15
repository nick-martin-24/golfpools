import os
import gpftp
import field
import datetime
import requests
import collections
from pathlib import Path
from contestant import Contestant
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
'''
l = leaderboard
pl = pga_leaderboard
sg = selected_golfers
'''


class Tournament:

    def __init__(self):
        self.__url_length = 158
        self.__json_url = ''
        self.__leaderboard_url = 'http://pgatour.com/leaderboard.html'
        self.__tournament_id = ''
        self.__setup = {}
        self.__l = {}
        self.__pl = {}
        self.__sg = {}
        self.__pga_ready_status = False
        self.__count_status = False
        self.__player_names = []
        self.__dirs = {}
        self.__files = {}
        self.__path = ''
        self.set_tournament_id()

    def get_players(self):
        return self.__pl['players']

    def get_player_names(self):
        return self.__player_names

    def get_cut(self):
        return self.__pl['cut_line']['cut_line_score']

    def get_par(self):
        return int(self.__pl['courses'][0]['par_total'])

    def get_sg(self):
        return self.__sg

    def get_leaderboard(self):
        return self.__l

    def get_current_round(self):
        return self.__pl['current_round']

    def get_output_directory(self):
        return self.__dirs['output']

    def get_ftp_directory(self):
        return self.__dirs['ftp']

    def get_html(self):
        return self.__files['html']

    def get_count_status(self):
        return self.__count_status

    def get_pga_ready_status(self):
        return self.__pga_ready_status

    def set_tournament_id(self):
        schedule = 'https://statdata.pgatour.com/r/current/schedule-v2.json'
        schedule_json = requests.get(schedule).json()
        week = str(int(schedule_json['thisWeek']['weekNumber']) + 1)
        year = schedule_json['years'][1]
        tour = year['tours'][0]
        current_tournament = next(item for item in tour['trns'] if item['date']['weekNumber'] == week
                                  and item['primaryEvent'] == 'Y')
        self.__tournament_id = current_tournament['permNum']
        self.__setup['setup_year'] = year['year']
        self.__pl['tournament_name'] = current_tournament['trnName']['official']
        self.__pl['round_state'] = 'nah'
        self.__pl['current_round'] = 0

    def select_golfer(self, name, data):
        if name not in self.__sg.keys():
            self.add_selected_golfer(name, data['total'])
        else:
            self.increment_selected_golfer(name)

    def add_selected_golfer(self, name, total):
        self.__sg[name] = {}
        self.__sg[name]['count'] = 1
        self.__sg[name]['total'] = total

    def increment_selected_golfer(self, name):
        if self.get_count_status() is False:
            self.__sg[name]['count'] += 1

    def set_json_url(self):
        # init Chrome driver (Selenium)
        options = Options()
        options.headless = True
        cap = DesiredCapabilities.CHROME
        cap['goog:loggingPrefs'] = {'performance': 'ALL'}
        driver = webdriver.Chrome(self.__files['chromedriver'], desired_capabilities=cap, options=options)

        # record and parse performance log
        driver.get(self.__leaderboard_url)
        performance_log = driver.get_log('performance')
        driver.quit()

        log = []
        base = 'https://statdata.pgatour.com/r'
        message = 'message.json'
        for item in performance_log:
            if base in item['message'] and message in item['message']:
                log.append(item['message'])

        idx = log[0].find(base)
        temp_url = log[0][idx:idx + self.__url_length].replace('message', 'leaderboard-v2')
        bad_id_idx = temp_url.find('/r/') + 3
        bad_id = temp_url[bad_id_idx:bad_id_idx+3]
        self.__json_url = temp_url.replace(bad_id, self.__tournament_id)

    def parse_json(self):
        f = requests.get(self.__json_url)
        if f.status_code == '200':
            self.__pga_ready_status = True
            parsed_json = f.json()
            self.__setup = parsed_json['debug']
            self.__pl = parsed_json['leaderboard']

    def initialize_field(self):
        self.__pl['players'] = []
        for golfer in range(0, len(self.__player_names)):
            self.__pl['players'].append({})
            self.__pl['players'][golfer]['current_round'] = None
            self.__pl['players'][golfer]['total'] = 0
            self.__pl['players'][golfer]['status'] = 'active'
            self.__pl['players'][golfer]['today'] = 0
            self.__pl['players'][golfer]['total_strokes'] = None
            self.__pl['players'][golfer]['current_round'] = 1
            self.__pl['players'][golfer]['rounds'] = [{'strokes': 0}, {'strokes': 0}, {'strokes': 0}, {'strokes': 0}]
            self.__pl['players'][golfer]['thru'] = 0
            self.__pl['players'][golfer]['day1'] = None
            self.__pl['players'][golfer]['day2'] = None
            self.__pl['players'][golfer]['day3'] = None
            self.__pl['players'][golfer]['day4'] = None

    def set_dirs_and_files(self, setup_type):
        if setup_type == 'init':
            self.__dirs['golfpools'] = '{}/projects/python/golfpools/'.format(os.getenv('HOME'))
            self.__files['chromedriver'] = '{}/data/chromedriver'.format(self.__dirs['golfpools'])

        else:
            # directories
            self.__dirs['ftp'] = 'golfpools.net/{}/{}/'.format(str(int(self.__setup['setup_year']) - 1),
                                                               self.__pl['tournament_name'].replace(' ', '').replace('.', ''))
            self.__dirs['golf'] = '{}/golf/'.format(os.getenv('HOME'))
            self.__dirs['output'] = '{}/{}/{}/'.format(self.__dirs['golf'],
                                                       str(int(self.__setup['setup_year']) - 1),
                                                       self.__pl['tournament_name'].replace(' ', '').replace('.', ''))
            self.__dirs['ftp-teams'] = '{}teams/'.format(self.__dirs['ftp'])

            # files
            self.__files['html'] = '{}leaderboard.html'.format(self.__dirs['output'])
            self.__files['php-file'] = '{}team_creation.php'.format(self.__dirs['output'])
            self.__files['users-file'] = '{}users.txt'.format(self.__dirs['output'])
            self.__files['field-html'] = '{}field.html'.format(self.__dirs['output'])

            if not os.path.exists(self.__dirs['output']):
                os.makedirs(self.__dirs['output'])
                # create users.txt
                Path('{}/users.txt'.format(self.__dirs['output'])).touch()
                gpftp.create_ftp_dirs(self.__dirs['ftp'], self.__dirs['ftp-teams'])
            self.__player_names = field.generate_field_html(self.__tournament_id, self.__dirs['output'], self.__dirs['ftp'])
            self.initialize_field()
            field.generate_php_file(self.__dirs['output'], self.__dirs['ftp'])

    def get_teams(self):
        os.chdir(self.__dirs['output'])
        gpftp.get_teams_from_ftp(self.__dirs, self.__files['users-file'])

    def initialize_leaderboard(self):
        with open(self.__files['users-file'], 'r') as f:
            count = 0
            for line in f:
                print(line)
                if line == '\n':
                    continue
                line = line[0:-1]
                name = line.split(': ')[0]
                name = name.replace('\\', '')
                roster = line.split(': ')[1].split(', ')
                tiebreaker = line.split(': ')[2]
                self.__l[name] = Contestant(self, name, roster, tiebreaker)
                count += 1
        print('{} teams processed.'.format(count))
        self.__count_status = True

    def update_leaderboard(self):
        for c in self.__l:
            self.__l[c].update_roster()

    def sort_leaderboard(self):
        self.__l = collections.OrderedDict(sorted(self.__l.items(), key=lambda x: x[1].get_total()))

    def sort_selected_golfers(self):
        self.__sg = collections.OrderedDict(sorted(self.__sg.items(), key=lambda x: x[1]['total']))

    def update(self):
        self.set_json_url()
        self.parse_json()
        self.update_leaderboard()
        self.sort_leaderboard()
        self.sort_selected_golfers()
        self.generate_html()
        gpftp.upload_file_to_ftp(self.get_output_directory(),
                                 self.get_html().split('/')[-1],
                                 self.get_ftp_directory())

    def generate_html(self):
        f = open(self.__files['html'], 'w')
        header = '''<!DOCTYPE html>
        <html>


        <head>
        <title>''' + self.__pl['tournament_name'] + '''</title>
        <meta http-equiv="refresh" content="20" />
        </head>

        <body>
        '''
#        <?php echo date('l, F jS, Y'); ?>
#        <?php
#        $handle = fopen("counter.txt", "r");
#        if(!$handle){
#          echo "could not open the file" ;
#        }
#        else {
#              $counter = ( int ) fread ($handle,20) ;
#              fclose ($handle) ;
#              $counter++ ;
#              echo "you are visitor no $counter" ;

#              $handle = fopen("counter.txt", "w" ) ;
#              fwrite($handle,$counter) ;
#              fclose ($handle) ;
#            }
#        ?>
        header += '''
        <h1 align="center">''' + self.__pl['tournament_name'] + '''</h1>
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
        for person in self.__l:
            f.write('<tr>')
            if place == 1:
                f.write('    <td align="center">%d</td>' % place)
            elif self.__l[person].get_total() == last_score:
                f.write('    <td align="center"></td>')
            else:
                f.write('    <td align="center">%d</td>' % place)

            f.write('    <td>')
            f.write(
                '        <a href="%s.html">%s</a>' % (person, person))
            f.write('    </td>')
            last_score = self.__l[person].get_total()
            place += 1

            if self.__l[person].get_total() == 0:
                f.write('    <td align="center">E</td>')
            else:
                f.write('    <td align="center">%+d</td>' % self.__l[person].get_total())

            for i in range(1, 5):
                if i > self.get_current_round():
                    f.write('    <td align="center">---</td>')
                elif self.__l[person].get_day('day' + str(i)) == 0:
                    f.write('    <td align="center">E</td>')
                else:
                    f.write('    <td align="center">%+d</td>' % self.__l[person].get_day('day' + str(i)))

            if self.__l[person].get_penalty() != 0:
                f.write('    <td align="center">%+d</td>' % self.__l[person].get_penalty())
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

        winnings = '''
            <tr>
                <td colspan="8" align="center">1st: $80, 2nd: $30, Last: $10</td>
            </tr>
            '''

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
        # f.write(winnings)
        f.write(home)
        if self.__pl['round_state'] != 'In Progress':
            f.write(create_a_team)
        f.write('</table>')

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

        if self.__pl['round_state'] == 'In Progress':
            for guy in self.__sg:
                f.write('<tr>')
                f.write('    <td>{} ({})</td>'.format(guy, self.__sg[guy]['count']))

                if self.__sg[guy]['total'] == 0:
                    f.write('    <td align="center">E</td>')
                else:
                    f.write('    <td align="center">{:+}</td>'.format(self.__sg[guy]['total']))

                f.write('</tr>')

        footer = '''
            </table>


            </body>
            </html>
            '''

        f.write(footer)

        f.close()
