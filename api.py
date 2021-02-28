import json
import classroom

Classroom = classroom.Classroom()
ClassroomStuff = classroom.GetClassroomStuff(classroom=Classroom)
Classroom.initialize()

def subjects():
    file = open('./json/data_new.json', 'w+')

    courses = ClassroomStuff.getCourses()

    sub = []
    for course in courses:
        cid = course['id']
        title = course['name']
        material = materials(cid)
        sub.append(dict({'id': cid, 'title': title, 'youtube': material['youtube'], 'materials': material['materials']}))

    subs = dict({'subjects': sub})
    json.dump(subs, file, indent=4)

def materials(cid):
    # file = open('./json/'+cid+'.json', 'w+')

    # if(cid == '118744664902'):
    ytb = []
    try:    
        videos = ClassroomStuff.lsd_mode(courseId=cid)
        for video in videos:
            topic = video['topic']
            title = video['title']
            link = video['link']
            ytb.append(dict({'topic_group': topic, 'title': title, 'url': link}))
            # file.write(topic+','+title+','+link+'\n')
        # return materials
    except Exception as e:
        print(e)

    course_materials = ClassroomStuff.get_posts(courseId=cid)
    
    materials = []

    for material in course_materials:
        title = material['title']
        url = 'https://drive.google.com/file/d/' + material['id']
        materials.append(dict({'title': title, 'url': url}))

    return dict({'youtube': ytb, 'materials': materials})
    # return materials
    # json.dump(materials, file, indent=4)

subjects()