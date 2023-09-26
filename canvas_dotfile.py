# create the .canvas file and push to the remote repository
import yaml
import base64

def create_assignment_dot_file(lesson):
    lesson_data = {
        ':lessons': [
            {
            ":id": lesson.id,
            ":course_id": lesson.course_id,
            ":instance": lesson.instance,
            ":canvas_url": lesson.canvas_url,
            ":type": lesson.type,
            }
        ]
    }  
    lesson_yaml = yaml.dump(lesson_data)
    return base64.b64encode(lesson_yaml.encode()).decode()

def create_page_dot_file(lesson):
    lesson_data = {
        ':lessons': [
            {
                ':id': lesson.id,
                ':course_id': lesson.course_id,
                ':instance': lesson.instance,
                ':canvas_url': lesson.canvas_url,
                ':type': lesson.type
            }
        ]
    }
    lesson_yaml = yaml.dump(lesson_data)
    return base64.b64encode(lesson_yaml.encode()).decode()

def update_assignment_dot_file(lesson, yaml_file):
    canvas_data = yaml.safe_load(yaml_file)
    course_list = []
    for item in canvas_data[':lessons']:
        course_list.append(item[':course_id'])
    if item[':course_id'] in course_list:
        print("The .canvas file already contains the data for this lesson")
        updated_file_yaml = yaml.dump(canvas_data)
        return base64.b64encode(updated_file_yaml.encode()).decode()
    else:
        lesson_data = {
                    ':id': lesson.id,
                    ':course_id': lesson.course_id,
                    ':instance': lesson.instance,
                    ':canvas_url': lesson.canvas_url,
                    ':type': lesson.type
                }
        canvas_data[':lessons'].update(lesson_data)
        updated_file_yaml = (yaml.dump(canvas_data))
        return base64.b64encode(updated_file_yaml.encode()).decode()

def update_page_dot_file(lesson, yaml__file):
    canvas_data = yaml.safe_load(yaml__file)
    course_list = []
    for item in canvas_data[':lessons']:
        course_list.append(item[':course_id'])
    if item[':course_id'] in course_list:
        print("The .canvas file already contains the data for this lesson")
        updated_file_yaml = yaml.dump(canvas_data)
        return base64.b64encode(updated_file_yaml.encode()).decode()
    else:
        lesson_data = {
                ":id": lesson.id,
                ":course_id": lesson.course_id,
                ":instance": lesson.instance,
                ":canvas_url": lesson.canvas_url,
                ":type": lesson.type,
                }
        canvas_data[':lessons'].append(lesson_data)
        updated_file_yaml = (yaml.dump(canvas_data))
        return base64.b64encode(updated_file_yaml.encode()).decode()