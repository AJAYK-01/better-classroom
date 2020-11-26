import classroom
import drive
import os

Classroom = classroom.Classroom()
ClassroomStuff = classroom.GetClassroomStuff(classroom=Classroom)
Drive = drive.GDrive()

def fetch_all_materials(reqCourse, courses):

    posts = []
    courseName = ''

    course = courses[int(reqCourse) - 1]
    courseId = course['id']
    courseName = course['name']

    if not os.path.exists('materials'):
        os.makedirs('materials')

    ''' dumping all materials in a separate folder for the particular subject '''
    if not os.path.exists('materials/'+courseName):
        os.makedirs('materials/'+courseName)

    courseMaterials = ClassroomStuff.get_posts(courseId=courseId, noassmnts=True)
    for material in courseMaterials:
        posts.append(material)

    for post in posts:
        # print(str(post))
        title = post['title']
        file_id = post['id']
        Drive.downloadFile(fileId=file_id, fileName=courseName+'/'+title)

    

if __name__ == "__main__":
    Classroom.initialize()
    student = Classroom.service.userProfiles().get(userId="me").execute()
    name = student.get("name").get("fullName")
    print("Name: "+name)

    courses = ClassroomStuff.getCourses()
    # print('Fetching data...')

    x = 1
    print("Courses are: ")
    for course in courses:
        id = course['id']
        title = course['name']
        print('  '+str(x)+'. '+title)
        x = x+1
    
    while(1):
        # I had 10 courses so :)
        try:
            request = input("\n  Enter course no 1/2/3/4/5/6/7/8/9/10) \n [ 0 to exit ] \n  ")
        
        except Exception as e:
            print(str(e))

        if request == '0':
            break

        print()
        try:
            fetch_all_materials(request, courses)
            print("\nSaved in /materials/"+courses[int(request) - 1]['name'])
        except Exception as e:
            print(str(e))
