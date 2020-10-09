import os
import collections
from pathlib import Path
from scrapeutils import pgatour
from golfpools.src import gpftp
from golfpools.src import html_factory
from golfpools.src.contestant import Contestant


class Tournament:

    def __init__(self):
        self.url_length = 158
        self.json_url = ''
        self.leaderboard_url = 'http://pgatour.com/leaderboard.html'
        self.tournament_id = ''
        self.setup = {}
        self.leaderboard = {}
        self.selected_golfers = {}
        self.pga_ready_status = False
        self.count_status = False
        self.player_names = []
        self.dirs = {}
        self.files = {}
        self.path = ''
        self.data = {}

    def select_golfer(self, name, total):
        if name not in self.selected_golfers.keys():
            self.add_selected_golfer(name, total)
        else:
            self.increment_selected_golfer(name)

    def add_selected_golfer(self, name, total):
        self.selected_golfers[name] = {}
        self.selected_golfers[name]['count'] = 1
        self.selected_golfers[name]['total'] = total

    def increment_selected_golfer(self, name):
        self.selected_golfers[name]['count'] += 1

    def set_dirs_and_files(self):
        # directories
        self.dirs['ftp'] = 'golfpools.net/{}/{}/'.format(self.data['actual_year'], self.data['name'].replace(' ', '').replace('.', ''))
        self.dirs['golf'] = '{}/golf'.format(os.getenv('HOME'))
        self.dirs['output'] = '{}/{}/{}'.format(self.dirs['golf'],
                                                self.data['actual_year'],
                                                self.data['name'].replace(' ', '').replace('.', ''))
        self.dirs['golfpools'] = '{}/projects/python/golfpools'.format(os.getenv('HOME'))
        self.dirs['ftp-teams'] = '{}teams/'.format(self.dirs['ftp'])

        # files
        self.files['php-file'] = '{}/team_creation.php'.format(self.dirs['output'])
        self.files['field-txt'] = '{}/field'.format(self.dirs['output'])
        self.files['users-file'] = '{}/users.txt'.format(self.dirs['output'])
        self.files['field-html'] = '{}/field.html'.format(self.dirs['output'])
        self.files['chromedriver'] = '{}/ref/chromedriver'.format(self.dirs['golfpools'])
        self.files['leaderboard-html'] = '{}/leaderboard.html'.format(self.dirs['output'])

        if not os.path.exists(self.dirs['output']):
            os.makedirs(self.dirs['output'])
            # create users.txt
            Path('{}/users.txt'.format(self.dirs['output'])).touch()
            gpftp.create_ftp_dirs(self.dirs['ftp'], self.dirs['ftp-teams'])

        if not os.path.exists(self.files['field-html']):
            html_factory.write_field_html(self.files['field-html'], pgatour.scrape_field(self.data['id']))
            gpftp.upload_file_to_ftp(self.dirs['output'] + '/', 'field.html', self.dirs['ftp'])

        if not os.path.exists(self.files['php-file']):
            html_factory.write_php(self.files['php-file'])
            gpftp.upload_file_to_ftp(self.dirs['output'] + '/', 'team_creation.php', self.dirs['ftp'])

    def get_teams(self):
        os.chdir(self.dirs['output'])
        gpftp.get_teams_from_ftp(self.dirs, self.files['users-file'])

    def process_golfpool_leaderboard(self):
        with open(self.files['users-file'], 'r') as f:
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
                self.leaderboard[name] = Contestant(self, name, roster, tiebreaker)
                count += 1
        print('{} teams processed.'.format(count))
        self.count_status = True

    def sort_golfpool_leaderboard(self):
        self.leaderboard = collections.OrderedDict(sorted(self.leaderboard.items(), key=lambda x: x[1].total))

    def sort_selected_golfers(self):
        self.selected_golfers = collections.OrderedDict(sorted(self.selected_golfers.items(), key=lambda x: x[1]['total']))

