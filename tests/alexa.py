import urllib
import requests
from bs4 import BeautifulSoup

HOME = 'http://www.golfpools.net'

def get_html_element(url, element):
    h = urllib.request.urlopen(url)
    html = h.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all(element)

def get_last_tournament():
    li = get_html_element(url, 'li')
    c = li[1]
    return c.contents[0].contents[0]

def get_last_winner():
    li = get_html_element(HOME, 'li')
    suffix = li[1].contents[0].attrs['href']
    l_url = url + '/' + suffix
    l = urllib.request.urlopen(l_url)
    l_html = l.read()
    l_soup = BeautifulSoup(l_html, 'html.parser')
    tr = l_soup.find_all('tr')
    winner = tr[2].contents[3].contents[1].contents[0]
    if winner == 'DaveT':
        winner = 'Dave T'
    return winner

def get_tournaments_by_year(year):
    ul = get_html_element(HOME, 'ul')
    year_data = [item for item in ul if 'value' in item.attrs and item.attrs['value'] == year]
    tournaments = [item for item in year_data[0] if item != '\n' and 'type' in item.attrs and item.attrs['type'] == 'tournament']
    return tournaments

def get_tournament_data(year, tournament_name):
    year_data = get_tournaments_by_year(year)
    tournament = [t for t in year_data if t.contents[0].text.lower() == tournament_name]
    return tournament

def get_years_in_history():
    ul = get_heml_element(HOME, 'ul')
    years_data = [item for item in ul if 'type' in item.attrs and item.attrs['type'] == 'year']
    
    return years

def get_winner_by_tournament(tournament):
    leaderboard_url = HOME + '/' + tournament[0].next.attrs['href']
    tr = get_html_element(leaderboard_url, 'tr')
    winner = tr[2].contents[3].contents[1].contents[0]
    return winner

