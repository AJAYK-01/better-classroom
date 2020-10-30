from __future__ import print_function
import pickle
import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# pylint: disable=import-error
from apiclient.http import BatchHttpRequest

SCOPES = [
    # 'https://www.googleapis.com/auth/classroom.coursework.students.readonly',
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.rosters',
    'https://www.googleapis.com/auth/classroom.rosters.readonly',
    'https://www.googleapis.com/auth/classroom.profile.emails',
    'https://www.googleapis.com/auth/classroom.profile.photos',
    'https://www.googleapis.com/auth/classroom.coursework.me',
    'https://www.googleapis.com/auth/classroom.courseworkmaterials',
    'https://www.googleapis.com/auth/classroom.announcements',
# 'https://www.googleapis.com/auth/classroom.coursework.me.readonly',
'https://www.googleapis.com/auth/classroom.coursework.students'
]

class GetClassroomStuff():
    gclassroom = None

    def __init__(self, classroom):
        self.gclassroom = classroom

    def getCourses(self):
        """ Gets list of course names """

        if 'courses' in globals():
            return

        results = self.gclassroom.service.courses().list(pageSize=100).execute()
        global courses
        courses = results.get('courses', [])

        courseNames = []
        for course in courses:
            courseNames.append(dict({'id': course['id'], 'name': course['name']}))

        return courseNames

    def getPosts(self, courseId):
        """ Gets classroom posts """

        materialsList = []

        try:
            # for materials posted as course work materials
            results = self.gclassroom.service.courses().courseWorkMaterials().list(courseId=courseId).execute()
            try:
                materials =  results['courseWorkMaterial']

                for material in materials:
                    files = []
                    try:
                        files = material['materials']
                    except Exception as e:
                        pass

                    for file in files:
                        try:
                            title = str(file['driveFile']['driveFile']['title'])
                            fileId = file['driveFile']['driveFile']['id']
                            materialsList.append(dict({'title': title, 'id': fileId}))
                        except Exception as e:
                            # print(str(e))
                            x = 1

            
            except Exception as e:
                # print(str(e))
                x = 1


            # for materials posted within announcements
            results = self.gclassroom.service.courses().announcements().list(courseId=courseId).execute()
            try:
                materials =  results['announcements']

                for material in materials:

                    files = []
                    try:
                        files = material['materials']
                    except Exception as e:
                        pass

                    for file in files:    
                        try:
                            title = str(file['driveFile']['driveFile']['title'])
                            fileId = file['driveFile']['driveFile']['id']
                            materialsList.append(dict({'title': title, 'id': fileId}))
                        except Exception as e:
                            # print(str(e))
                            x = 1

            
            except Exception as e:
                # print(str(e))
                x = 1

            # for materials posted within assignments
            results = self.gclassroom.service.courses().courseWork().list(courseId=courseId).execute()
            try:
                materials =  results['courseWork']

                for material in materials:

                    files = []
                    try:
                        files = material['materials']
                    except Exception as e:
                        pass

                    for file in files:    
                        try:
                            title = str(file['driveFile']['driveFile']['title'])
                            fileId = file['driveFile']['driveFile']['id']
                            materialsList.append(dict({'title': title, 'id': fileId}))
                        except Exception as e:
                            # print(str(e))
                            x = 1

            
            except Exception as e:
                # print(str(e))
                x = 1

        except Exception as e:
            materialsList=[]
            # print(str(e))


        return materialsList

        
    
class Classroom:
    service = None
    driveService = None

    def initialize(self):
        creds = None
        drive_creds = None

        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'classroom_creds.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        
        self.service = build('classroom', 'v1', credentials=creds)
      
