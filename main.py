import classroom
import drive

Classroom = classroom.Classroom()
ClassroomStuff = classroom.GetClassroomStuff(classroom=Classroom)
Drive = drive.GDrive()

def fetchMaterials(reqFile, reqCourse, courses):

    # I had 10 courses so :)
    x = 1
    posts = []
    if reqCourse == '0':
        for course in courses:
            courseId = course['id']
            courseMaterials = ClassroomStuff.getPosts(courseId=courseId)
            for material in courseMaterials:
                posts.append(material)

    else:
        course = courses[int(reqCourse) - 1]
        courseId = course['id']
        courseMaterials = ClassroomStuff.getPosts(courseId=courseId)
        for material in courseMaterials:
            posts.append(material)

    for post in posts:
        # print(str(post))
        title = post['title']
        if reqFile.casefold() in title.casefold():
            file_id = post['id']
            Drive.downloadFile(fileId=file_id, fileName=title)

    

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
        request = input("\n  Enter course no (space) material name (1/2/3/4/5/6/7/8/9/10) \n  [ 0 to search in all courses, q to exit ] \n  ")
        reqCourse = request.split(' ')[0]
        if reqCourse == 'q':
            break
        reqFile = request.split(' ')[1]

        print()
        fetchMaterials(reqFile, reqCourse, courses)
