# create the .canvas file and push to the remote repository
import yaml

def create_assignment_dot_file(lesson, course):
    lesson_data = {
        'lessons': [
            {
            "id": lesson.id,
            "course_id": course.id,
            "instance": course.instance,
            "canvas_url": lesson.canvas_url,
            "type": lesson.type,
            "grading_type": lesson.grading_type,
            "points_possible": lesson.points,
            "submission_type": lesson.submissions
            }
        ]
    }  
    return yaml.dump(lesson_data)

def create_page_dot_file(lesson, course):
    lesson_data = {
        'lessons': [
            {
                'id': lesson.id,
                'course_id': course.id,
                'canvas_url': lesson.canvas_url,
                'type': lesson.type
            }
        ]
    }

def update_assignment_dot_file(lesson, course, yaml_file):
    canvas_data = yaml.load(yaml_file)
    lesson_data = {
                'id': lesson.id,
                'course_id': course.id,
                'instance': course.instance,
                'canvas_url': lesson.canvas_url,
                'type': lesson.type
            }
    updated_file = canvas_data['lessons'].update(lesson_data)
    return updated_file

def update_page_dot_file(lesson, course, yaml__file):
    canvas_data = yaml.load(yaml__file)
    lesson_data = {
            "id": lesson.id,
            "course_id": course.id,
            "instance": course.instance,
            "canvas_url": lesson.canvas_url,
            "type": lesson.type,
            "grading_type": lesson.grading_type,
            "points_possible": lesson.points,
            "submission_type": lesson.submissions
            }
    updated_file = canvas_data['lessons'].update(lesson_data)
    return updated_file