import os.path
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class GDrive():

    gauth = GoogleAuth()
    # gauth.LocalWebserverAuth()

    gauth.LoadCredentialsFile("drive_creds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("drive_creds.txt")


    drive = GoogleDrive(gauth)
        
        
    def downloadFile(self, fileId, fileName):

        if not os.path.exists('materials'):
            os.makedirs('materials')

        fileName = os.path.normpath('./materials/'+fileName)

        if os.path.exists(fileName):
            try:
                print('Material '+fileName.split('/')[-1]+' already downloaded')
            except Exception:
                print('Material '+fileName+' already downloaded')
            return 

        file = self.drive.CreateFile({'id': fileId})
        if 'pdf' in file['title'] or 'ppt' in file['title'] or 'doc' in file['title']:
            print('Downloading file %s ' % file['title'])
            file.GetContentFile(fileName)
