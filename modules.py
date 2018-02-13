import os
from definition import *
import json

class Gallery:

    def __init__(self):
        pass

    '''
    * Read folder names inside photo folder
    * @param
    *   NONE
    *
    * @return
    *   $final (ARRAY)
    '''
    def get_all_gallery(self):
        galleries = [name for name in os.listdir(Gallery_Folder)]
        return galleries

    '''
    * Create folder using the name argument
    * @param
    *   $name (string)
    *
    * @return
    *   Boolean
    '''
    def add_gallery(self,gallery_name):
        if os.path.isdir(Gallery_Folder+gallery_name) is False:
            if os.mkdir(Gallery_Folder+gallery_name):
                return True
        else:
            return False


    '''
    * Delete folder using the name argument
    * @param
    *   $name (string)
    *
    * @return
    *   Boolean
    '''
    def delete_gallery(self, gallery_name):
        if os.path.isdir(Gallery_Folder+gallery_name) is True:
            if os.removedirs(Gallery_Folder+gallery_name):
                return True
            else:
                return False
        else:
            return False

    '''
    * rename a gallery folder name
    * @param
    *   $currentName (string)
    *   $newName (string)
    *
    * @return
    *   Boolean
    '''
    def edit_gallery_name(self,oldName,newName):
        if os.path.isdir(Gallery_Folder+oldName) is True:
            if os.rename(Gallery_Folder+oldName, Gallery_Folder+newName):
                return True
        else:
            return False

class Login:

    # Constructor
    def __init__(self):
        pass

    '''
    * Handle the login feature
    * @param username(string)
    * @param password(string)
    *
    * @return Boolean
    '''
    def login(self,username,password):
        data = {}
        logincreds = self.getcredentials()

        for key in logincreds:
            if logincreds[key]['user'] == username and logincreds[key]['password'] == password:
                data['type'] = logincreds[key]['type']
                data['result'] = True

                return data
        return False

    '''
    * Handle the logout feature by destroying session
    * @param NONE
    *
    * @return Boolean
    '''
    def logout(self):
        pass

    '''
    * Read Credentials JSON file to get saved username and password
    * @param NONE
    *
    * @return Array
    '''
    def getcredentials(self):
        data = json.loads(open(CREDENTIALS_FILE).read())
        return data['credentials']


class Photos:

    def __init__(self):
        pass

    '''
    * Read photos names inside photo folder
    * @param gallery_name (String)
    *
    * @return
    *   $final (ARRAY)
    '''
    def get_all_gallery_photos(self, gallery_name):
        photos = [name for name in os.listdir(Gallery_Folder+gallery_name) if(name.split(".")[0] != "Thumbs")]
        return photos

    '''
    * Delete image using the name argument
    * @param gallery_name (string)
    * @param photo_name (string)
    *
    * @return
    *   Boolean
    '''
    def delete_gallery_photos(self, gallery_name, photo_name):
        if os.path.exists(Gallery_Folder + gallery_name+"/"+photo_name) is True:
            if os.remove(Gallery_Folder+gallery_name+"/"+photo_name):
                return True
            else:
                return False
        else:
            return False