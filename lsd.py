import classroom
import drive

Classroom = classroom.Classroom()
ClassroomStuff = classroom.GetClassroomStuff(classroom=Classroom)
Drive = drive.GDrive()

if __name__ == "__main__":
    Classroom.initialize()
    student = Classroom.service.userProfiles().get(userId="me").execute()
    name = student.get("name").get("fullName")
    print("Name: "+name)

    courses = ClassroomStuff.getCourses()
    # print('Fetching data...')

    file = open('lsd.csv', 'w')


    try:    
        for course in courses:
            id = course['id']
            if(id == '118744664902'):
                videos = ClassroomStuff.lsd_mode(courseId=id)
                for video in videos:
                    title = video['title'].replace(",", " -")
                    link = video['link']
                    file.write(title+','+link+'\n')
                    # print(title+' - '+link)

        print('\nSaved all youtube link materials as lsd.csv\n')
    
    except Exception as e:
        print(str(e))
    

