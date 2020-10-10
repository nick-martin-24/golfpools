from golfpools.src import gpftp
from golfpools.src import html_factory

class Contestant:

    def __init__(self, t, name, roster, tiebreaker):
        self.full_html = '{}/{}.html'.format(t.dirs['output'], name)
        self.html = '{}.html'.format(name)
        self.name = name
        self.tiebreaker = tiebreaker
        self.roster = roster
        self.total = 0
        self.days = {'day1': 0, 'day2': 0, 'day3': 0, 'day4': 0}
        self.penalty = 0
        self.t = t
        self.process_roster()


    def process_roster(self):
        for golfer in self.roster:
            self.t.select_golfer(golfer, self.t.data['players'][golfer]['total'], self.t.data['players'][golfer]['real_total'])
            self.penalty += self.t.data['players'][golfer]['penalty']
            self.total += (self.t.data['players'][golfer]['real_total'] or 0)
            self.compute_day_totals(self.t.data['players'][golfer])
        self.total += self.penalty

        html_factory.write_user_html(self)
        gpftp.upload_file_to_ftp(self.t.dirs['output'], self.html, self.t.dirs['ftp'])


    def compute_day_totals(self, golfer_data):
        if self.t.data['current_round'] == 1:
            self.days['day1'] += (golfer_data['today'] or 0)

        elif self.t.data['current_round'] == 2:
            self.days['day1'] += golfer_data['day1']
            self.days['day2'] += (golfer_data['today'] or 0)

        elif self.t.data['current_round'] == 3:
            self.days['day1'] += golfer_data['day1']
            self.days['day2'] += golfer_data['day2']
            self.days['day3'] += golfer_data['today'] or 0

        elif self.t.data['current_round'] == 4:
            self.days['day1'] += golfer_data['day1']
            self.days['day2'] += golfer_data['day2']
            self.days['day3'] += golfer_data['day3']
            self.days['day4'] += (golfer_data['today'] or 0)

