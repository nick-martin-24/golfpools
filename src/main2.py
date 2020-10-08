import time
import gpftp
import datetime
from scrapeutils import utils
from tournament2 import Tournament


start_time = time.time()
t = Tournament()
data = utils.scrape()
t.set_dirs_and_files(data)
t.get_teams()
