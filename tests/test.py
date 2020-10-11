from scrapeutils import utils, pgatour
from golfpools.src.tournament import Tournament
from golfpools.src import html_factory

def get_current_tournament():
    ct = utils.get_current_tournament()
    for key in ct:
        print('{}: {}'.format(key, ct[key]))

def scrape():
    # scrape test
    a = utils.scrape()
    p = a['players']
    p_active = list(p.keys())[0]
    p_cut = list(p.keys())[100]
    r = p[p_active]['rounds'][0]

    print('Tournament:')
    for key in a:
        if key != 'players':
            print('{}: {}'.format(key, a[key]))

    print()
    print('Active Player:')
    print('name: {}'.format(p_active))
    for key in p[p_active]:
        if key != 'rounds':
            print('{}: {}'.format(key, p[p_active][key]))

    if p[p_cut]['status'] == 'cut':
        print()
        print('Cut Player:')
        print('name: {}'.format(p_cut))
        for key in p[p_cut]:
            if key != 'rounds':
                print('{}: {}'.format(key, p[p_cut][key]))

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


