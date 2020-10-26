import classroom

Classroom = classroom.Classroom()
ClassroomStuff = classroom.GetClassroomStuff(classroom=Classroom)



if __name__ == "__main__":
    Classroom.initialize()
    student = Classroom.service.userProfiles().get(userId="me").execute()
    name = student.get("name").get("fullName")
    print("Name: "+name)

    courses = ClassroomStuff.getCourses()
    print('Courses\n'+str(courses))
