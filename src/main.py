import time
import gpftp
from tournament import Tournament

if '__main__' in __name__:
    start_time = time.time()
    t = Tournament()
    t.set_dirs_and_files('init')
    t.set_json_url()
    t.parse_json()
#   t.set_player_names()
    t.set_dirs_and_files('full')
    t.get_teams()
    t.initialize_leaderboard()
    t.sort_leaderboard()
    t.sort_selected_golfers()
    t.generate_html()
    gpftp.upload_file_to_ftp(t.get_output_directory(), t.get_html().split('/')[-1], t.get_ftp_directory())
    while True:
        t.update()
        time.sleep(60 - ((time.time() - start_time) % 60.0))
