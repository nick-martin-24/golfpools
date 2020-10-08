import os
import json
from golfpools.src import gpftp
from golfpools.src import field
from golfpools.src import html_factory
from scrapeutils import pgatour
import urllib
import datetime
import requests
import collections
from pathlib import Path
from golfpools.src.contestant import Contestant
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
'''
l = golfpools leaderboard
pl = pga_leaderboard
sg = selected_golfers
'''


class Tournament:

    def __init__(self):
        self.url_length = 158
        self.json_url = ''
        self.leaderboard_url = 'http://pgatour.com/leaderboard.html'
        self.tournament_id = ''
        self.setup = {}
        self.l = {}
        self.pl = {}
        self.sg = {}
        self.pga_ready_status = False
        self.count_status = False
        self.player_names = []
        self.dirs = {}
        self.files = {}
        self.path = ''


    def select_golfer(self, name, data):
        if name not in self.__sg.keys():
            self.add_selected_golfer(name, data['total'])
        else:
            self.increment_selected_golfer(name)

    def add_selected_golfer(self, name, total):
        self.sg[name] = {}
        self.sg[name]['count'] = 1
        self.sg[name]['total'] = total

    def increment_selected_golfer(self, name):
        if self.get_count_status() is False:
            self.sg[name]['count'] += 1


    def set_dirs_and_files(self, data):
        # directories
        self.dirs['ftp'] = 'golfpools.net/{}/{}/'.format(data['actual_year'], data['name'].replace(' ', '').replace('.', ''))
        self.dirs['golf'] = '{}/golf'.format(os.getenv('HOME'))
        self.dirs['output'] = '{}/{}/{}'.format(self.dirs['golf'],
                                                data['actual_year'],
                                                data['name'].replace(' ', '').replace('.', ''))
        self.dirs['golfpools'] = '{}/projects/python/golfpools'.format(os.getenv('HOME'))
        self.dirs['ftp-teams'] = '{}teams/'.format(self.dirs['ftp'])

        # files
        self.files['php-file'] = '{}/team_creation.php'.format(self.dirs['output'])
        self.files['field-txt'] = '{}/field'.format(self.dirs['output'])
        self.files['users-file'] = '{}/users.txt'.format(self.dirs['output'])
        self.files['field-html'] = '{}/field.html'.format(self.dirs['output'])
        self.files['chromedriver'] = '{}/data/chromedriver'.format(self.dirs['golfpools'])
        self.files['leaderboard-html'] = '{}/leaderboard.html'.format(self.dirs['output'])

        if not os.path.exists(self.dirs['output']):
            os.makedirs(self.dirs['output'])
            # create users.txt
            Path('{}/users.txt'.format(self.dirs['output'])).touch()
            gpftp.create_ftp_dirs(self.dirs['ftp'], self.dirs['ftp-teams'])

        if not os.path.exists(self.files['field-html']):
            html_factory.write_field_html(self.files['field-html'], pgatour.scrape_field(data['id']))
            gpftp.upload_file_to_ftp(self.dirs['output'] + '/', 'field.html', self.dirs['ftp'])

        if not os.path.exists(self.files['php-file']):
            html_factory.write_php(self.files['php-file'])
            gpftp.upload_file_to_ftp(self.dirs['output'] + '/', 'team_creation.php', self.dirs['ftp'])
#        self.initialize_field()

    def get_teams(self):
        os.chdir(self.dirs['output'])
        gpftp.get_teams_from_ftp(self.dirs, self.files['users-file'])

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
                <td colspan="8" align="center">1st: $80, 2nd: $20, Last: $10</td>
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
        f.write(winnings)
        f.write(home)
#        if self.__pl['round_state'] != 'In Progress':
        f.write(create_a_team)
#        f.write('</table>')

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

        if self.__pl['round_state'] == 'In Progress' or self.__pl['round_state'] != 'In Progress':
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
