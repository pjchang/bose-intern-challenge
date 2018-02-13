import os
from definition import *
import json
from pymongo import MongoClient

class Albums:

    def __init__(self):
        # self.client = MongoClient(host='localhost', port=27017)
        # self.db = self.client['Bose']
        pass

    def get_all_albums(self,username):
        if not os.path.isdir(Gallery_Folder+username+"/"):
            os.mkdir(Gallery_Folder+username+"/")
        galleries = [name for name in os.listdir(Gallery_Folder+username+"/")]
        return galleries

    def add_album(self,album_name,username):
        if os.path.isdir(Gallery_Folder+username+"/"+album_name) is False:
            if os.mkdir(Gallery_Folder+username+"/"+album_name):
                return True
        else:
            return False

    def delete_album(self, album_name,username):
        if os.path.isdir(Gallery_Folder+username+"/"+album_name) is True:
            if os.removedirs(Gallery_Folder+username+"/"+album_name):
                return True
            else:
                return False
        else:
            return False


    def edit_gallery_name(self,oldName,newName,username):
        if os.path.isdir(Gallery_Folder+username+"/"+oldName) is True:
            if os.rename(Gallery_Folder+username+"/"+oldName, Gallery_Folder+username+"/"+newName):
                return True
        else:
            return False

class Login:

    # Constructor
    def __init__(self):
        # self.client = MongoClient(host='localhost', port=27017)
        # self.db = self.client['Bose']
        self.connection = MongoClient('ds231568.mlab.com', 31568)
        self.db = self.connection['bose']
        self.db.authenticate('admin', 'pass')

    # login existing user
    def sign_in(self,username,password):
        user=self.db.users.find_one({'name':username,'pass':password})
        return True if user else False


    def logout(self):
        pass

    def register(self, username,password, email):

        # check if the username has been claimed
        user_pre = self.db.users.find_one({'name':username})
        if user_pre:
            return {'status':False,'error':'username has been claimed'}
        self.db.users.insert({'name':username,'pass':password,'email':email})
        return {'status':True,'error':''}



class Photos:

    def __init__(self):
        pass

    def get_photos(self, album_name,username):
        photos = [name for name in os.listdir(Gallery_Folder+username+"/"+album_name) if(name.split(".")[0] != "Thumbs")]
        return photos

    def delete_photos(self, album_name, photo_name,username):
        if os.path.exists(Gallery_Folder+username+"/" + album_name+"/"+photo_name) is True:
            print 'find photo'
            if os.remove(Gallery_Folder+username+"/"+album_name+"/"+photo_name):
                return True
            else:
                return False
        else:
            return False