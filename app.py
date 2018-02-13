from flask import Flask
from flask import session
from flask import request
from flask import render_template
from flask import redirect, url_for
from werkzeug.utils import secure_filename
import json
import os
from modules import Login, Albums, Photos
from definition import *
from pymongo import MongoClient

app = Flask(__name__)
app.config.update(dict(SECRET_KEY='mylongsecretkeys'))

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg','png',])
photos_obj = Photos()


@app.route('/')
# @app.route('/index')
def index():
    # if user already logged in, go to albums
    if 'user_login' in session:
        if session['user_login'] == True:
            return redirect(url_for('albums'))

    # if user havent logged in, go to login page
    return redirect(url_for('login'))


@app.route('/login', methods=['GET','POST'])
def login():

    # visited by url
    if request.method == "GET":
        return render_template("index-login.html")

    # visited by form
    if request.method == "POST":
        login_inst=Login()
        login_status=login_inst.sign_in(request.form['username'],request.form['password'])
        if login_status:
            session['user_login'] = True
            session['user_curr'] = request.form['username']
        
        return redirect(url_for('index'))
        

@app.route('/register', methods=['GET','POST'])
def register():

    # visited by url
    if request.method == "GET":
        return render_template("index-register.html", error={'error':''} )
    # visited by form
    if request.method == "POST":
        login_inst=Login()
        register=login_inst.register(request.form['username_reg'],request.form['password_reg'],request.form['email_reg'])
        # if successfully register
        if register['status']:
            session['user_login'] = True
            session['user_curr'] = request.form['username_reg']
            return redirect(url_for('index'))
        else:
            session['user_login'] = False
            session['user_curr'] = ''
            return render_template("index-register.html",error={'error':register['error']})

@app.route('/logout')
def do_logout():
    session.pop('user_login', None)
    session.pop('user_curr', None)
    return redirect(url_for('index'))


# -------------- Gallery Routes ----------------


@app.route('/albums')
def albums():
    if 'user_login' in session:
        albums_inst = Albums()
        albums_list = albums_inst.get_all_albums(session['user_curr'])
        return render_template("index-albums.html", albums=albums_list, session=session, owner_name=session['user_curr'])
        #return render_template("gallery.html", albums=albums_list, session=session, owner_name=session['user_curr'])
    else:
        return redirect(url_for("index"))


@app.route('/albums/add', methods=['POST'])
def add_album():
    if 'user_login' in session:
        if request.method == "POST":
            album_name = request.form['album_name']

            album_obj = Albums()
            result = album_obj.add_album(album_name,session['user_curr'])

            response = {'success':result}
            return json.dumps(response)
    else:
        response = {'success': False}
        return json.dumps(response)


@app.route('/albums/delete', methods=['POST'])
def delete_album():
    if request.method == "POST":
        album_name = request.form['album_name']

        album_obj = Albums()
        result = album_obj.delete_album(album_name,session['user_curr'])

        response = {'success': result}
        return json.dumps(response)

# -------------- Gallery Routes ----------------


# -------------- Gallery Photos Routes ----------------
@app.route('/album/<album_name>/<owner_name>', methods=['GET'])
def gallery(album_name,owner_name):
    if 'user_login' in session:
        photos_obj = Photos()
        photos = photos_obj.get_photos(album_name,owner_name)
        return render_template("index-photos.html", photos=photos, gallery_folder=Gallery_Folder,album_name=album_name, session=session,owner_name=owner_name)
    else:
        return redirect(url_for("index"))

# can only delete by owner
@app.route('/album/photos/delete', methods=['POST'])
def delete_gallery_photo():
    if request.method == "POST":
        album_name = request.form['albumName']
        photo_name = request.form['photoName']
        owner_name = request.form['ownerName']

        # if owner is current user
        if owner_name == session['user_curr']:
            result = photos_obj.delete_photos(album_name, photo_name,owner_name)
        else:
            result=False

        response = {'success': result}
        return json.dumps(response)

# can only upload by owner
@app.route('/album/<album_name>/<owner_name>/upload', methods=['POST'])
def upload_gallery_photo(album_name,owner_name):
    app.config['UPLOAD_FOLDER'] = Gallery_Folder+owner_name+'/'+album_name

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(url_for('gallery', album_name=album_name,owner_name=owner_name))
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            msg = 'No selected file'
            return redirect(request.url)

        # if the current user is the owner
        if session['user_curr'] == owner_name:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return redirect(url_for('gallery', album_name=album_name,owner_name=owner_name))


@app.route('/test', methods=['GET'])
def test():
    return render_template("index-register.html")

# check the file types
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__  == "__main__":
    app.run(debug=True)



