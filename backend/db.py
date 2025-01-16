## initialise
import uuid
import mysql.connector
import os


filecachemap = {}
maxfilecached = 1000
def putcachefile(path, file):
    filecachemap[path] = file
    if(len(filecachemap)>maxfilecached):
        filecachemap.pop(list(filecachemap.keys())[0])


class User:
    def __init__(self, username, password, paths, isadmin=False):
        self.username = username
        self.password = password
        self.paths = paths
        self.isadmin = isadmin
    


def init():
    global db
    db = mysql.connector.connect(
        user=os.environ.get('MYSQL_USER'), 
        password=os.environ.get('MYSQL_PASSWORD'), 
        host = os.environ.get('MYSQL_HOST'),
        port=os.environ.get("MYSQL_PORT") , 
        database=os.environ.get('MYSQL_DATABASE'),
        pool_size=10,
        pool_name="quickpool"
#        autocommit=True
        )
## query
# generate tables if not exist
# userdata username,password
# media username, path  
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS userdata (email VARCHAR(300) NOT NULL, username VARCHAR(300) NOT NULL, password VARCHAR(300) NOT NULL,isadmin BOOL NOT NULL DEFAULT 0, PRIMARY KEY (username))")
    c.execute("CREATE TABLE IF NOT EXISTS media (username VARCHAR(300) NOT NULL, path VARCHAR(300) NOT NULL, mediatype ENUM('image','audio','video') NOT NULL, PRIMARY KEY (path), FOREIGN KEY (username) REFERENCES userdata(username) ON UPDATE CASCADE ON DELETE CASCADE)")
    # separate table, which is basically a key value store
    # can flexibly change file storage implementations if it is done like this
    c.execute("CREATE TABLE IF NOT EXISTS files (path VARCHAR(300), file LONGBLOB, FOREIGN KEY (path) REFERENCES media(path) ON UPDATE CASCADE ON DELETE CASCADE)")
    c.close()
# this is made assuming that there is only one instance of the server running at any given time.

# username password
def getuser(username):
    c = db.cursor()
    c.execute("SELECT userdata.username,userdata.password,media.path,userdata.isadmin FROM userdata  LEFT JOIN media ON media.username = userdata.username WHERE userdata.username = %s", (username,))
    res = c.fetchall()
    c.close()
    if(len(res)==0):
        return None
    paths = []
    password = ""
    isadmin = False
    for r in res:
        password = r[1]
        isadmin = r[3]
        if(r[2]):
            paths.append(r[2])
    
    return User(username, password, paths,isadmin)


def adduser(email, username, password):
    c = db.cursor()
    # create user if not exists, if exists use try catch instead of checking using another query 
    try:
        c.execute("INSERT INTO userdata (email, username, password) VALUES (%s, %s, %s)", (email, username, password))
        db.commit()
    except(mysql.connector.errors.IntegrityError):
        c.close()
        return False
    c.close()
    return True

def getfile(path):
    if(path in filecachemap):
        return filecachemap[path]
    c = db.cursor()
    try:
        c.execute("SELECT file FROM files WHERE path = %s", (path,))
        res = c.fetchall()
    except Exception as e:
        print(e)
        return None
    c.close()
    if(len(res)==0):
        return None
    putcachefile(path, res[0][0])
    return res[0][0]


def addfile(username, path):
    c = db.cursor()
    c.execute("INSERT INTO media (username, path) VALUES (%s, %s)", (username, path))
    db.commit()
    c.close()


def addfiles(username, arr):
    # arr = list of file and filenames and mediatypes(filename, file,mediatype)[]
    valpaths = []
    valfiles = []
    for filename,file,mediatype in arr:
        valpaths.append((username, filename, mediatype))
        valfiles.append((filename, file))
    
    c = db.cursor()    
    try: 
        c.executemany("INSERT INTO media (username, path, mediatype) VALUES (%s, %s, %s)", valpaths)
        c.executemany("INSERT INTO files (path, file) VALUES (%s, %s)", valfiles)
        db.commit()
        c.close()
        return True
    except:
        db.rollback()
        c.close()
        return False


def getuserlist():
    c = db.cursor()
    res = []
    try:
        c.execute("SELECT email, username, isadmin FROM userdata")
        res = c.fetchall()
    except Exception as e:
        print(e)
    c.close()
    return [{"email":r[0], "username":r[1], "isadmin":r[2]} for r in res]
