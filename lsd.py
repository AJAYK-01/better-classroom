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

    
    for course in courses:
        id = course['id']
        if(id == '118744664902'):
            videos = ClassroomStuff.lsdMode(courseId=id)
            for video in videos:
                title = video['title']
                link = video['link']
                file.write(title+','+link+'\n')
                # print(title+' - '+link)
    

