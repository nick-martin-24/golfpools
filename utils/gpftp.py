from ftplib import FTP

user = '2096943'
password = 'Bonner10!'
site = 'golfpools.net'


def upload_file_to_ftp(path, filename, destination):
    ftp = FTP(site, user, password)
    ftp.cwd(destination)
    file = open(path + filename, 'rb')
    ftp.storbinary('STOR ' + filename, file)
    file.close()
    ftp.quit()


def create_ftp_dirs(ftp_dir, ftp_teams):
    ftp = FTP(site, user, password)
    ftp.mkd(ftp_dir)
    ftp.mkd(ftp_teams)
    ftp.quit()


def get_teams_from_ftp(dirs):
    ftp = FTP(site, user, password)
    ftp.cwd(dirs['ftp-teams'])
    files = ftp.nlst()
    for filename in files:
        local_filename = dirs['output'] + filename
        file = open(local_filename, 'wb')
        ftp.retrbinary('RETR ' + filename, file.write)
        file.close()

    ftp.quit()
