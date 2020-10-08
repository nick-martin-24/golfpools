from scrapeutils import utils, pgatour
from golfpools.src.tournament2 import Tournament
from golfpools.src import html_factory

def scrape():
    # scrape test
    a = utils.scrape()
    p = a['players']
    n = list(p.keys())[0]
    r = p[n]['rounds'][0]

    print('Tournament:')
    for key in a:
        if key != 'players':
            print('{}: {}'.format(key, a[key]))

    print()
    print('Player')
    print('name: {}'.format(n))
    for key in p[n]:
        if key != 'rounds':
            print('{}: {}'.format(key, p[n][key]))

    print()
    print('Round')
    for key in r:
        print('{}: {}'.format(key, r[key]))


def set_dirs_and_files():
    t = Tournament()
    a = utils.scrape()
    t.set_dirs_and_files(a)
    print()
    print('Directories:')
    for key in t.dirs.keys():
        print('{}: {}'.format(key, t.dirs[key]))

    print()
    print('Files:')
    for key in t.files.keys():
        print('{}: {}'.format(key, t.files[key]))


def pgatour_field():
    x = utils.scrape()
    field = pgatour.scrape_field(x['id'])
    print()
    print('A:')
    for p in field['a']:
        print(p)

    print()
    print('B:')
    for p in field['b']:
        print(p)

    print()
    print('C:')
    for p in field['c']:
        print(p)

    print()
    print('D:')
    for p in field['d']:
        print(p)


def write_html():
    x = utils.scrape()
    html_factory.write_field_html('test_field', pgatour.scrape_field(x['id']))


