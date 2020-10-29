import classroom

Classroom = classroom.Classroom()
ClassroomStuff = classroom.GetClassroomStuff(classroom=Classroom)



if __name__ == "__main__":
    Classroom.initialize()
    student = Classroom.service.userProfiles().get(userId="me").execute()
    name = student.get("name").get("fullName")
    print("Name: "+name)

    courses = ClassroomStuff.getCourses()
    # courseWork = ClassroomStuff.getPosts()
    # print('Courses\n'+str(courses))
    # print('Coursework\n'+ courseWork)

    posts = []
    for course in courses:
        id = course['id']
        courseMaterials = ClassroomStuff.getPosts(courseId=id)
        for material in courseMaterials:
            posts.append(material)

    print(str(posts))

    reqFile = input('Enter material name')

    for post in posts:
        # print(str(post))
        title = post['title']
        if reqFile.casefold() == title.casefold():
            file_id = post['id']
            ClassroomStuff.downloadMaterial(fileId=file_id, filename=title)