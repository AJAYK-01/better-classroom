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

    
    def get_coursework_materials(self, course_id):
        ''' returns all stuff posted AS "materials" as dict '''
        
        results = self.gclassroom.service.courses().courseWorkMaterials().list(courseId=course_id).execute()
        try:
            materials =  results['courseWorkMaterial']
            return materials

        except Exception as e:
            # print(str(e)+'line 57')
            pass
        
        return []

    
    def get_announcements(self, course_id):
        ''' return all announcements as dict '''

        results = self.gclassroom.service.courses().announcements().list(courseId=course_id).execute()
        try:
            announcements =  results['announcements']
            return announcements

        except Exception as e:
            # print(str(e)+'line 72')
            pass
        
        return []


    def get_assignments(self, course_id):
        ''' returns all posted assignments as a dict '''
        results = self.gclassroom.service.courses().courseWork().list(courseId=course_id).execute()
        try:
            assignments =  results['courseWork']
            return assignments
        
        except Exception as e:
            # print(str(e)+'line 86')
            pass
        
        return []


    def get_posts(self, courseId, noassmnts=False):
        """ Gets classroom posts """

        materialsList = []

        try:

            ''' for materials posted as course work materials '''
            materials =  self.get_coursework_materials(course_id=courseId)
            for material in materials:
                files = []
                try:
                    files = material['materials']
                except Exception as e:
                    # print(str(e)+'line 106')
                    continue

                for file in files:
                    try:
                        title = str(file['driveFile']['driveFile']['title'])
                        fileId = file['driveFile']['driveFile']['id']
                        materialsList.append(dict({'title': title, 'id': fileId}))
                    except Exception as e:
                        # print(str(e)+'line 115')
                        continue

            

            ''' for materials posted within announcements '''
            materials = self.get_announcements(course_id=courseId)
            for material in materials:

                files = []
                try:
                    files = material['materials']
                except Exception as e:
                    # print(str(e)+'line 128')
                    continue

                for file in files:    
                    try:
                        title = str(file['driveFile']['driveFile']['title'])
                        fileId = file['driveFile']['driveFile']['id']
                        materialsList.append(dict({'title': title, 'id': fileId}))
                    except Exception as e:
                        # print(str(e)+'line 137')
                        continue


            if noassmnts == False:
                ''' for materials posted within assignments '''
                materials = self.get_assignments(course_id=courseId)
                for material in materials:

                    files = []
                    try:
                        files = material['materials']
                    except Exception as e:
                        # print(str(e)+'line 149')
                        continue

                    for file in files:    
                        try:
                            title = str(file['driveFile']['driveFile']['title'])
                            fileId = file['driveFile']['driveFile']['id']
                            materialsList.append(dict({'title': title, 'id': fileId}))
                        except Exception as e:
                            # print(str(e)+'line 158')
                            continue


        except Exception as e:
            materialsList=[]
            print(str(e))


        return materialsList

    def lsd_mode(self, courseId):
        """ Gets all lsd youtube links """

        materialsList = []

        materials = self.get_coursework_materials(course_id=courseId)    
        for material in materials:
            files = []
            material_topic = ""
            try:
                files = material['materials']
                material_topic = material['title']
            except Exception as e:
                # print(str(e))
                continue

            for file in files:
                try:
                    topic = material_topic
                    title = str(file['youtubeVideo']['title'])
                    link = str(file['youtubeVideo']['alternateLink'])
                    materialsList.append(dict({'topic': topic, 'title': title, 'link': link}))
                except Exception as e:
                    # print(str(e))
                    continue
            
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
      
