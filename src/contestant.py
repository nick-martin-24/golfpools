import gpftp
from datetime import datetime


class Contestant:

    def __init__(self, t, name, roster, tiebreaker):
        self.__full_html = '{}{}.html'.format(t.get_output_directory(), name)
        self.__html = '{}.html'.format(name)
        self.__name = name
        self.__tiebreaker = tiebreaker
        self.__roster = roster
        self.__missed_cuts = 0
        self.__total = 0
        self.__day1 = 0
        self.__day2 = 0
        self.__day3 = 0
        self.__day4 = 0
        self.__days = {'day1': 0, 'day2': 0, 'day3': 0, 'day4': 0}
        self.__rounds = []
        self.__started = False
        self.__penalty = 0
        self.__t = t
        self.__team = {}
        self.initialize_roster()

    def get_t(self):
        return self.__t

    def get_html(self):
        return self.__html

    def get_name(self):
        return self.__name

    def get_roster(self):
        return self.__roster

    def get_golfer_status(self, golfer_name):
        return self.__team[golfer_name]['status']

    def get_golfer_total_strokes(self, golfer_name):
        return self.__team[golfer_name]['total_strokes']

    def get_golfer_total(self, golfer_name):
        return self.__team[golfer_name]['total']

    def get_total(self):
        return self.__total

    def get_day(self, day):
        return self.__days[day]

    def get_penalty(self):
        return self.__penalty

    def get_team(self):
        return self.__team

    def initialize_roster(self):
        players = self.__t.get_players()
        for golfer in self.__roster:
            golfer_data = players[self.__t.get_player_names().index(golfer)]
            self.__t.select_golfer(golfer, golfer_data)
            self.initialize_golfer(golfer, golfer_data)
            self.assess_cut(golfer)
            self.set_thru(golfer_data['thru'], golfer)
            self.process_golfer_rounds(golfer, self.__t.get_current_round())

        self.generate_html()
        gpftp.upload_file_to_ftp(self.__t.get_output_directory(), self.__html, self.__t.get_ftp_directory())

    def update_roster(self):
        for g in self.__roster:
            if self.__t.get_players()[self.__t.get_player_names().index(g)]['thru'] == self.__team[g]:
                self.assess_cut(g)
                self.set_thru(self.__t.get_player_names().index(g)['thru'], g)
                self.process_golfer_rounds(g, self.__t.get_current_round())

    def initialize_golfer(self, name, data):
        self.__team[name] = {}
        self.__team[name]['status'] = data['status']
        self.__team[name]['penalty'] = '---'
        self.__team[name]['today'] = data['today']
        self.__team[name]['total'] = data['total']
        self.__team[name]['total_strokes'] = data['total_strokes']
        self.__team[name]['current_round'] = data['current_round']
        self.__team[name]['day1'] = data['rounds'][0]['strokes']
        self.__team[name]['day2'] = data['rounds'][1]['strokes']
        self.__team[name]['day3'] = data['rounds'][2]['strokes']
        self.__team[name]['day4'] = data['rounds'][3]['strokes']
        if data['rounds'][3]['tee_time'] is not None:
            date_str = data['rounds'][3]['tee_time']
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
            self.__team[name]['tee_time'] = date_obj.time().isoformat()[0:5]
        else:
            self.__team[name]['tee_time'] = data['rounds'][3]['tee_time']
        if self.__team[name]['total'] is not None:
            self.update_total(self.__team[name]['total'])

    def process_golfer_rounds(self, name, current_round):
        if current_round == 1:
            if self.__team[name]['today'] is not None:
                self.update_current_day_score('day1', name)
                self.start_team()
            else:
                self.start_team()
        elif current_round == 2:
            self.update_previous_day_score('day1', name)
            if self.__team[name]['today'] is not None or self.__team[name]['status'] == 'cut':
                self.update_current_day_score('day2', name)
                self.start_team()
            else:
                self.start_team()
        elif current_round == 3:
            self.update_previous_day_score('day1', name)
            self.update_previous_day_score('day2', name)
            if self.__team[name]['today'] is not None:
                self.update_current_day_score('day3', name)
                self.start_team()
        elif current_round == 4:
            self.update_previous_day_score('day1', name)
            self.update_previous_day_score('day2', name)
            if self.__team[name]['status'] == 'active':
                self.update_previous_day_score('day3', name)
            if self.__team[name]['today'] is not None:
                self.update_current_day_score('day4', name)
                self.start_team()

    def set_thru(self, thru, g):
        if thru == '18':
            self.__team[g]['thru'] = 'F'
        else:
            self.__team[g]['thru'] = thru

    def assess_cut(self, g):
        if self.__team[g]['status'] == 'cut':
            self.assess_penalty(g, self.__t.get_cut())

    def assess_penalty(self, name, cut):
        penalty = (self.__team[name]['total'] - cut)
        self.__team[name]['total'] += penalty
        self.__team[name]['penalty'] = penalty
        self.__penalty += penalty
        self.__missed_cuts += 1
        self.__total += penalty

    def update_total(self, total):
        self.__total += total

    def update_current_day_score(self, day, name):
        if self.__team[name]['status'] == 'cut' and day == 'day2':
            self.__days[day] += self.__team[name]['day2'] - self.__t.get_par()
        else:
            self.__days[day] += self.__team[name]['today']

    def update_previous_day_score(self, day, name):
        self.__days[day] += int(self.__team[name][day]) - self.__t.get_par()

    def get_change(self, name):
        initial_score = self.__team[name]['today']
        new_score = self.__t.get_players()[self.__t.get_player_names().index(name)]['today']
        return new_score - initial_score

    def start_team(self):
        self.__started = True

    def generate_html(self):
        f = open(self.__full_html, 'w')
        header = '''<html>
        <head>
            <title>''' + self.__name + '''</title>
            <meta http-equiv="refresh" content="20" /></head>
        </head>
        '''

        body_start = '''
        <body>
        <h2>''' + self.__name + '''</h2>
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

        for golfer in self.__roster:
            f.write('    <tr>')
            if self.__team[golfer]['status'] == 'cut':
                f.write('        <td>%s*</td>' % golfer)
            else:
                f.write('        <td>%s</td>' % golfer)

            if self.__team[golfer]['total_strokes'] is None:
                f.write('        <td align="center">---</td>')
            elif self.__team[golfer]['total'] == 0:
                f.write('        <td align="center">E</td>')
            else:
                f.write('        <td align="center">%+d</td>' % self.__team[golfer]['total'])

            for i in range(1, 5):
                if i == self.__t.get_current_round():
                    if self.__team[golfer]['status'] == 'cut':
                        if i < 3:
                            score = int(self.__team[golfer]['day' + str(i)]) - int(self.__t.get_par())
                            if score == 0:
                                f.write('        <td align="center">E</td>')
                            else:
                                f.write('        <td align="center">%+d</td>' % score)
                        else:
                            f.write('        <td align="center">---</td>')
                    elif self.__team[golfer]['today'] is None:
                        if i == 4:
                            f.write('        <td align="center">{}</td>'.format(self.__team[golfer]['tee_time']))
                        else:
                            f.write('        <td align="center">---</td>')
                    elif self.__team[golfer]['today'] == 0:
                        f.write('        <td align="center">E (%s)</td>' % self.__team[golfer]['thru'])
                    else:
                        f.write('        <td align="center">%+d (%s)</td>' % (int(self.__team[golfer]['today']),
                                                                              self.__team[golfer]['thru']))
                elif self.__team[golfer]['current_round'] is None and self.__team[golfer]['status'] == 'active':
                    f.write('        <td align="center">---</td>')
                elif i > self.__t.get_current_round():
                    f.write('        <td align="center">---</td>')
                elif self.__team[golfer]['day' + str(i)] is None:
                    f.write('        <td align="center">---</td>')
                else:
                    score = int(self.__team[golfer]['day' + str(i)]) - int(self.__t.get_par())
                    if score == 0:
                        f.write('        <td align="center">E</td>')
                    else:
                        f.write('        <td align="center">%+d</td>' % score)

            if type(self.__team[golfer]['penalty']) == int:
                f.write('    <td align="center">%+d</td>' % self.__team[golfer]['penalty'])
            else:
                f.write('    <td align="center">%s</td>' % self.__team[golfer]['penalty'])

            f.write('    </tr>')

        tiebreaker = '''
        <tr>
            <td>Tiebreaker</td>
            <td align="center">''' + self.__tiebreaker + '''</td>
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
