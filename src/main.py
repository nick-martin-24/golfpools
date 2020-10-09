import gpftp
import html_factory
from scrapeutils import utils
from tournament import Tournament


t = Tournament()
t.data = utils.scrape()
t.set_dirs_and_files()
t.get_teams()
t.process_golfpool_leaderboard()
t.sort_golfpool_leaderboard()
t.sort_selected_golfers()
html_factory.write_leaderboard_html(t)
gpftp.upload_file_to_ftp(t.dirs['output'], t.files['leaderboard-html'].split('/')[-1], t.dirs['ftp'])

