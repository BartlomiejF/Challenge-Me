import os, sqlite3, shutil, datetime

#delete past challenges
def purge_db():
    db = sqlite3.connect(
            '/home/Bartlomiej/instance/challenge-me.sqlite'
            )
    db.execute('''DELETE FROM challenges WHERE gamedate < strftime('%Y-%m-%d');''')
    db.commit()

#create db backup
def backup():
    datee = datetime.datetime.today().strftime('%d-%m-%Y')+'.old'
    shutil.copyfile('/home/Bartlomiej/instance/challenge-me.sqlite', f'/home/Bartlomiej/instance/challenge-me.sqlite.{datee}')

if __name__=='__main__':
    backup()
    purge_db()