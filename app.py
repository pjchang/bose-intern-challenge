from flask import Flask
from flask import session
from flask import request
from flask import render_template
from flask import redirect, url_for, abort, jsonify
from werkzeug.utils import secure_filename
import json
import os
from pymongo import MongoClient
import time
import base64
from bson.objectid import ObjectId

# -------------- class ----------------
class Login:

    def __init__(self):
        # self.client = MongoClient(host='localhost', port=27017)
        # self.db = self.client['Bose']
        self.connection = MongoClient('ds023455.mlab.com', 23455)
        self.db = self.connection['bose']
        self.db.authenticate('admin', 'pass')

    def sign_in(self,username,password):
        user=self.db.users.find_one({'user':username,'pass':password})
        return True if user else False

    def register(self, username,password, email):
        # check if the username has been claimed
        user_pre = self.db.users.find_one({'user':username})
        if user_pre:
            return {'status':False,'error':error_list[9]}
        self.db.users.insert({'user':username,'pass':password,'email':email})
        return {'status':True,'error':''}



class Albums:

    def __init__(self):
        # self.client = MongoClient(host='localhost', port=27017)
        # self.db = self.client['Bose']
        self.connection = MongoClient('ds023455.mlab.com', 23455)
        self.db = self.connection['bose']
        self.db.authenticate('admin', 'pass')

    def get_albums(self,username):
        album=self.db.albums.find({'user':username}, {'album':1,'_id': 0})
        albums_list=[ k['album'] for k in album ]
        return albums_list

    def add_album(self,album_name,username):
        album_exit = self.db.albums.find_one({'user':username,'album':album_name})
        if album_exit:
            return {'status':False,'error':error_list[5]}
        self.db.albums.insert({'user':username,'album':album_name,'create_time':time.time(),'photos':[]})
        return {'status':True,'error':''}


    def delete_album(self, album_name,username):
        album_exit = self.db.albums.find_one({'user':username,'album':album_name})
        if album_exit:
            self.db.albums.delete_one({'user':username,'album':album_name})
            return {'status':True,'error':''}
        else:
            return {'status':False,'error':error_list[8]}


    def edit_album_name(self,oldName,newName,username):
        pass


class Photos:

    def __init__(self):
        # self.client = MongoClient(host='localhost', port=27017)
        # self.db = self.client['Bose']
        self.connection = MongoClient('ds023455.mlab.com', 23455)
        self.db = self.connection['bose']
        self.db.authenticate('admin', 'pass')

    def get_photos(self, album_name,username):
        album=self.db.albums.find_one({'user':username,'album':album_name}, {'photos':1,'_id': 0})
        photos_list=[]
        if album:
            for photo in album['photos']:
                photos_list.append(self.db.photos.find_one({'_id': photo}, {'img':1,'_id': 1}))
        return photos_list

    def add_photo(self, file, filename, album, username):
        _id=self.db.photos.insert({"img":file,'filename':filename,'album':album,'user':username,'create_time':time.time()})
        self.db.albums.update({'user':username,'album':album}, {'$push': {'photos': _id}})


    def delete_photo(self, album_name, photo_name,username):
        self.db.photos.delete_one({'_id': ObjectId(photo_name)})
        self.db.albums.update_one({ "user": username, "album": album_name},{ "$pull": { "photos": ObjectId(photo_name) } })
        return True

# -------------- initiate app ----------------

app = Flask(__name__)
app.config.update(dict(SECRET_KEY='mylongsecretkeys'))
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg','png','gif' ])
# app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 
# something wrong with this code
error_list=['','No selected file', 'Upload cant complete', 'Only album owner could add photos', 'Only jpg, jpeg, png and gif files are allowed',
'The album already exists.', 'Album name is too long','User hasnt login yet.','Cant delete this albums','username has been claimed'
,'Username or password is incorrect.']

# -------------- Sign-in Sign-our ----------------

@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def index():
    error_msg=''
    # visited by url
    if request.method == "GET":
        if 'user_login' in session:
            if session['user_login'] == True:
                return redirect(url_for('albums'))
        return render_template("index-login.html", error_msg=error_msg,session=session)

    # visited by form
    if request.method == "POST":
        login_inst=Login()
        login_status=login_inst.sign_in(request.form['username'],request.form['password'])
        if login_status:
            session['user_login'] = True
            session['user_curr'] = request.form['username']
            return redirect(url_for('albums'))
        else:
            error_msg=error_list[10]
            return render_template("index-login.html", error_msg=error_msg,session=session)
        

@app.route('/register', methods=['GET','POST'])
def register():
    # visited by url
    if request.method == "GET":
        if 'user_login' in session:
            if session['user_login'] == True:
                return redirect(url_for('index'))
        return render_template("index-register.html", error_msg='',session=session)
    # visited by form
    if request.method == "POST":
        login_inst=Login()
        register=login_inst.register(request.form['username_reg'],request.form['password_reg'],request.form['email_reg'])
        if register['status']:
            session['user_login'] = True
            session['user_curr'] = request.form['username_reg']
            return redirect(url_for('index'))
        else:
             session.pop('user_login', None)
             session.pop('user_curr', None)
             return render_template("index-register.html",error_msg=register['error'],session=session)

@app.route('/logout')
def do_logout():
    session.pop('user_login', None)
    session.pop('user_curr', None)
    return redirect(url_for('index'))


# -------------- albums ----------------

@app.route('/albums')
def albums():
    if 'user_login' in session:
        albums_inst = Albums()
        albums_list = albums_inst.get_albums(session['user_curr'])
        return render_template("index-albums.html", albums=albums_list, session=session)
    else:
        return redirect(url_for("index"))


@app.route('/albums/add', methods=['POST'])
def add_album():
    if 'user_login' in session:
        if request.method == "POST":
            album_name = request.form['album_name']
            if len(album_name)>20:
                response = {'success': False, 'error':error_list[6]}
            else:
                album_obj = Albums()
                result = album_obj.add_album(album_name,session['user_curr'])
                response = {'success': result['status'], 'error':result['error']}
            return json.dumps(response)
    else:
        response = {'success': False,'error':error_list[7]}
        return json.dumps(response)


@app.route('/albums/delete', methods=['POST'])
def delete_album():
    if request.method == "POST":
        album_name = request.form['album_name']
        album_obj = Albums()
        result = album_obj.delete_album(album_name,session['user_curr'])
        response = {'success': result['status'], 'error':result['error']}
        return json.dumps(response)


# -------------- photos ----------------

@app.route('/album/<album_name>/<owner_name>', methods=['GET'])
def gallery(album_name,owner_name):
    if 'user_login' in session:
        error_code = request.args.get('error') if request.args.get('error') else 0
        try:
            error_code=int(error_code)
        except:
            error_code=0
        photos_obj = Photos()
        photos = photos_obj.get_photos(album_name,owner_name)
        photo_list=[]
        for photo in photos:
            decode=photo["img"].decode()
            img_tag = "data:image/png;base64,{0}".format(decode)
            photo_list.append({'img':img_tag,'id':photo["_id"]})
        return render_template("index-photos.html", photos=photo_list, album_name=album_name, session=session,owner_name=owner_name,error=error_list[error_code])
    else:
        return redirect(url_for("index"))

# can only delete by owner
@app.route('/album/photos/delete', methods=['POST'])
def delete_gallery_photo():

    if request.method == "POST":
        album_name = request.form['albumName']
        photo_name = request.form['photoName']
        owner_name = request.form['ownerName']

        #if current user is the owner
        if owner_name == session['user_curr']:
            photos_obj = Photos()
            result = photos_obj.delete_photo(album_name, photo_name,owner_name)
        else:
            result=False
        response = {'success': result}
        return json.dumps(response)

@app.route('/album/<album_name>/<owner_name>/upload', methods=['POST'])
def upload_gallery_photo(album_name,owner_name):

    if request.method == 'POST':
        error_num=0
        try:
            # check if the post request has the file part
            if 'file' not in request.files:
                error_num=1
                return redirect(url_for('gallery', album_name=album_name,owner_name=owner_name,error=error_num))
            
            file = request.files['file']
            if file.filename == '':
                error_num=1
                msg = error_code[error_num]
                return redirect(request.url)

            # if the current user is the owner
            if session['user_curr'] == owner_name:
                # check the data formate
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    encoded_file = base64.b64encode(file.read())
                    photos_obj = Photos()
                    photos = photos_obj.add_photo(encoded_file,filename, album_name, owner_name)
                else:
                    error_num=4
            else:
                error_num=3
        except:
            error_num=2
    return redirect(url_for('gallery', album_name=album_name,owner_name=owner_name,error=error_num))

# -------------- others ----------------

@app.route('/test', methods=['GET'])
def test():
    albums_inst = Albums()
    albums_list = albums_inst.get_albums(session['user_curr'])
    return render_template("index-register.html")

# direct every other links to the login page
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return redirect(url_for("index"))

# check the file types
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__  == "__main__":
    app.run(debug=True)



