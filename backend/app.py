import os
from flask import Flask, make_response, request
from dotenv import load_dotenv
from functools import wraps
from flask_cors import CORS
import db
import uuid
import sessions
import json
import editor
load_dotenv()

db.init()

## jwt init
JWT_SECRET = os.environ.get('JWT_SECRET')
JWT_EXPIRES_HRS = os.environ.get('JWT_EXPIRES_HRS')

app = Flask(__name__)
if(os.environ.get('production')=='false'):
    CORS(app)

VIDEO_EXTNS = ['mp4', 'mkv', 'avi', 'mov', 'wmv']
AUDIO_EXTNS = ['mp3', 'wav', 'ogg']
IMG_EXTNS = ['png', 'jpg', 'jpeg', 'gif', 'webp']
MAX_FILE_SIZE = int(os.environ.get('MAX_FILE_SIZE')) * 1024*1024

preloaded_audio = []
# use preloaded audio
for filename in os.listdir("preloadedaudio"):
    if filename.endswith(".mp3"):
        preloaded_audio.append("preloadedaudio."+filename)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("jwt")
        print(token)
        session = sessions.verify_session(token)
        if(not session):
            return {
                "message": "Invalid session"
            }, 401
        else:
            return f(session, *args, **kwargs)
    return decorated

@app.route('/preloadedaudio', methods=['GET'])
def preloadedaudio():
    return json.dumps(preloaded_audio)

@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    if(not username or not password):
        return {
            "message": "Invalid credentials"
        }, 401
    user = db.getuser(username)
    if not user:
        return {
            "message": "Invalid credentials"
        }, 401
    user.paths = [{"filename": s,"mediatype": filetype(s)} for s in user.paths]
    if user.password == password:
        return {
            "jwt": sessions.create_session(user)
        }
    else:
        return {
            "message": "Invalid credentials"
        }, 401

@app.route('/register', methods=['GET'])
def register():
    email = request.args.get('email')
    username = request.args.get('username')
    password = request.args.get('password') 
    if not username or not password or not email:
        return {
            "message": "Invalid credentials"
        }, 401
    
    if db.adduser(email, username, password):
        return {
            "jwt": sessions.create_session(db.User(username, password, [], False))
        }
    else:
        return {
            "message": "User already exists"
        }, 401


@app.route('/getfile/<filename>', methods=['GET']) 
@token_required
def getfile(session,filename):
    if  (
        ( 
          (filename.startswith("preloadedaudio.")) and filename in preloaded_audio and
          ((filename:= '.'.join(filename.split('.')[1:]))) and 
          (file:= open("preloadedaudio/"+filename, "rb").read()) 
        ) or 
        ( (filename == s["filename"] for s in session.paths) and (file := db.getfile(filename) ) ) 
        ):
        return file, 200, {'Content-Type': 'application/octet-stream', 
                           'Content-Disposition': f'attachment; filename={filename}',
                            'Content-Length': len(file),
                            'Accept-Ranges': 'bytes'
                           }
    
    else:
        return {
            "message": "File not found"
        }, 404

def filetype(filename):
    #TODO secure regex check
    if('.' in filename):
        ext = filename.split('.')[-1]
        if(ext in VIDEO_EXTNS):
            return "video"
        elif(ext in AUDIO_EXTNS):
            return "audio"
        elif(ext in IMG_EXTNS):
            return "image"
    return None

def size_check(file):
    return file.content_length <= MAX_FILE_SIZE

def sanitize(filename):
    return filename.replace('/','').replace('\\','').replace('..','').replace(',','')

@app.route('/user/upload', methods=['POST'])
@token_required
def upload(session):
    if request.method == 'POST': 
        print("upload called")
        files = request.files.getlist("files")       # Get the list of files from webpage 
        if len(files) == 0:
            print("No selected file")
            return { "message":"No selected file" }, 400
        else:
            arr = []
            filenametypes = []
            for file in files:
                media_type = filetype(file.filename)
                if(not media_type or not size_check(file)):
                    return { "message":"Invalid files" }, 400
                fname = uuid.uuid1().hex +'.'+ sanitize(file.filename)
                arr.append(( fname , file.stream.read(), media_type))
                filenametypes.append({"filename": fname,"mediatype": media_type})
            if(db.addfiles(session.username, arr)):
                session.paths.extend(filenametypes)
                return { "message":"Files Uploaded Successfully!", "jwt": sessions.create_session(session)}, 200
            else:
                return { "message":"Error uploading files" }, 500

@app.get('/transitions')
def transitions():
    return json.dumps(editor.TRANSITIONS)

@app.post('/edit')
@token_required
def edit(session):
    data = request.get_json()
    try:
        file, status, headers = editor.edit(session, data)
        return file, status, headers
    except Exception as e:
        print(e)
        return { "message":"Error editing files" }, 500


@app.get('/users')
@token_required
def get_users(session):
    if(session.isadmin):
        return db.getuserlist()
    else:
        return { "message":"Unauthorized" }, 400

if __name__ == '__main__':
    app.run(host="0.0.0.0")
    # app.run(debug=True,host="0.0.0.0")
