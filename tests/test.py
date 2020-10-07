from scrapeutils import utils


# scrape test
a = utils.scrape()
p = a['players']
n = list(p.keys())[0]
r = p[n]['rounds'][0]

print('Tournament:')
print('name: {}'.format(a['name']))
print('par: {}'.format(a['par']))
print('current_round: {}'.format(a['current_round']))
print('is_started: {}'.format(a['is_started']))
print('is_finished: {}'.format(a['is_finished']))
print('round_state: {}'.format(a['round_state']))
print('cut_line: {}'.format(a['cut_line']))

print()

print('Player')
print('name: {}'.format(n))
print('status: {}'.format(p[n]['status']))
print('current_round: {}'.format(p[n]['current_round']))
print('thru: {}'.format(p[n]['thru']))
print('today: {}'.format(p[n]['today']))
print('total: {}'.format(p[n]['total']))
print('total_strokes: {}'.format(p[n]['total_strokes']))

print()

print('Round')
print('strokes: {}'.format(r['strokes']))
print('tee_time: {}'.format(r['tee_time']))
