from ftplib import FTP

ftp = FTP("hr18.sakura.ne.jp")
ftp.login("hr18", "pzbu97smpe")

with open("latest_calendar.csv", "rb") as f:
    ftp.storlines("STOR /home/hr18/www/latest_calendar.csv", f)

ftp.close()
