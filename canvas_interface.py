import requests
import credentials
import yaml
import pandas as pd
from csv import writer
import lesson_content

class Course:
    def __init__(self, API_KEY, API_PATH, course_id):
        """
        Queries a canvas course and collects all pages and assignments. Pages will be stored as a page object and assignments will be stored as an assignment object.

        Args:
            json_response (_type_): _description_
        """
        self.API_KEY = API_KEY
        self.API_PATH = API_PATH
        self.course_id = course_id
        
    def get_pages(self):
        """pulls the data for all assignments and pages in the specified canvas course.

        Args:
            API_KEY (str): api key for the specified canvas instance
            API_PATH (str): api path for the specified canvas instance
            course_id (int): _description_

        Returns:
            json: lessons, assignments, and pages from the specified canvas course.
        """

        headers = {
                'Authorization': f'Bearer {self.API_KEY}'
            }

        done = False
        page = 1
        pages = []
        while(not done):
            assn_url = f"{self.API_PATH}/courses/{self.course_id}/pages?per_page=100&page={page}"
            assn_response = requests.get(assn_url, headers=headers)
            response_list = assn_response.json()
            pages.extend(response_list)
            
            if (len(response_list) < 100):
                done = True
            else:
                page += 1

        self.pages = pages
        self.number_of_pages = len(pages)
    def get_assignments(self):
        """pulls the data for all assignments and pages in the specified canvas course.

        Args:
            API_KEY (str): api key for the specified canvas instance
            API_PATH (str): api path for the specified canvas instance
            course_id (int): _description_

        Returns:
            json: lessons, assignments, and pages from the specified canvas course.
        """
    
        headers = {
                'Authorization': f'Bearer {self.API_KEY}'
            }

        done = False
        page = 1
        assignments = []
        while(not done):
            assn_url = f"{self.API_PATH}/courses/{self.course_id}/assignments?per_page=100&page={page}"
            assn_response = requests.get(assn_url, headers=headers)
            response_list = assn_response.json()
            assignments.extend(response_list)
            
            if (len(response_list) < 100):
                done = True
            else:
                page += 1
        
        clean_list = list(filter(lambda x: x['description'] != None, assignments))
        
        saturncloud_tag = 'saturnenterprise.io/dash/resources'
        saturncloud_assign = list(filter(lambda x: saturncloud_tag in x['description'], clean_list))


        self.assignments = saturncloud_assign
        self.number_of_assignments = len(saturncloud_assign)
    
class Assignment:
    def __init__(self, lesson, course_id, instance):
        """takes one element of a json response from course.get_course_assignments and converts it to an Assignment object. If creating a new assignment you can pass the information as a dictionary

        Args:
            assignment (json): single element of the response from course.get_course_assignments
        """
        self.id = lesson['id']
        self.content = lesson['description']
        self.submissions = lesson['submission_types']
        self.url = lesson_content.lesson_name(lesson['description'])[1]
        self.name = lesson_title(self.url)
        self.course_id = course_id
        self.type = "assignment"
        self.instance = instance

def lesson_title(lesson_url):
    """Creates a page title from either the H1 tag or the url of the repo.

    Args:
        lesson_url (str): The github url

    Returns:
        _type_: _description_
    """
    
    lesson_repo = lesson_url.split('/')[-1]
    remove_characters = lesson_repo.split('-')[1:]
    words = []
    articles = ['but', 'and', 'nor', 'for', 'or', 'so', 'as', 'if', 'yet', 'a', 'the', 'of', 'in', 'as', 'at', 'by', 'to']
    for word in remove_characters:
        if word not in articles:
            words.append(word.title())
        else:
            words.append(word)
    return ' '.join(words)
            
class Page:
    def __init__(self, lesson, course_id, instance):
        self.id = lesson['url']
        self.type = "page"
        self.instance = instance
        self.course_id = course_id
        self.canvas_url = lesson['html_url']
        self.name = lesson['title']
        
class Get_lesson:
    def __init__(self, course_id, id, instance, assign_type):
        """Initiates a lesson object for a single page or assignment

        Args:
            instance (str): your canvas instance abbreviation (consumer: "e" default, enterprise: "e", moringa: "m", academyxi: "a", vangard: "v")
            course_id (int): the canvas course id of the course your lesson is located in
            id (str): the id of the lesson. In the case of an assignment this will be a number, in the case of a page this will be the "sluggified" page id which is the page name as seen in the url.
            type (str): The type of lesson either a page: "p" or an assignment: "a"(default)
        """
        auth = credentials.Credentials(instance)
        
        self.API_KEY = auth.API_KEY
        self.API_PATH = auth.API_PATH
        self.course_id = course_id
        self.id = id
        self.instance = instance
        if assign_type == "a":
            self.type = "assignment"
        else:
            self.type = "page"

        
    def get_lesson(self):
        
        """Retrieves the lesson from canvas and converts the information to an Assignment object

        Returns:
            Assignment obj: Assignment object
        """
    
        headers = {
                'Authorization': f'Bearer {self.API_KEY}'
            }
        assn_url = f"{self.API_PATH}/courses/{self.course_id}/{self.type}s/{self.id}"
        assn_response = requests.get(assn_url, headers=headers)
        #return Assignment(assn_response.json())
        lesson = assn_response.json()
        if self.type == "page":
            return Page(lesson, self.course_id, self.instance)
        if self.type == "assignment":
            return Assignment(lesson, self.course_id, self.instance)
        
    
def create_assignment(instance, remote=True, remote_url=None, sc=False, course_id=0):
    """Creates a canvas assignment in the course with the course_id provided.

    Args:
        instance (str): The single letter representation of the instance you are working with. This gets passed to the credentials function to generate the a credentials object
        remote (bool, optional): Specify whether you are working with a remote repository or a local one. Defaults to True.
        remote_url (GitHub SSH URL, optional): This is the Github SSH url for the repository you are working on. It must be the SSH clone link for authentication purposes. Defaults to None.
        sc (bool, optional): Specify if the lesson is a SaturnCloud lesson. if True, the SaturnCloud button will either be created or updated. Defaults to False.
        course_id (int, optional): This is the course_id of the course you are working on. It defaults to 0 for when it is not necessary. Defaults to 0.
    """
    
    auth = credentials.Credentials(instance)
    
    headers = {
            'Authorization': f'Bearer {auth.API_KEY}'
            }

    if remote:
        content = lesson_content.GithubContent(auth.instance, sc, remote_url)
    else:
        content = lesson_content.LocalContent(auth.instance, sc)
    
    if sc:
        new_description = f'{content.data_element} {content.header} {content.intro} {content.button}'
        
    else:
        new_description = f'{content.data_element} {content.header} {content.html}'

        # setting up the payload for delivery

    payload = {
        "assignment[name]": content.title,
        "assignment[description]": new_description,
        "assignment[submission_types]": ['none'],
        "external_tool_tag_attributes": 'none'
        }

    assignment_url = f"{auth.API_PATH}/courses/{course_id}/assignments/"

    put_response = requests.put(assignment_url, headers=headers, data=payload)
    print(content.title, 'Completed')
    print(f"The lesson can be found at: {put_response.json()['html_url']}")
    
def create_page(instance, course_id=0, remote=True, remote_url=None, sc=False):
    auth = credentials.Credentials(instance)
    
    headers = {
            'Authorization': f'Bearer {auth.API_KEY}'
            }

    if remote:
        content = lesson_content.GithubContent(auth.instance, sc, remote_url)
    else:
        content = lesson_content.LocalContent(auth.instance, sc)
    
    if sc:
        new_description = f'{content.data_element} {content.header} {content.intro} {content.button} {content.meta}'
        
    else:
        new_description = f'{content.data_element} {content.header} {content.html} {content.meta}'

        # setting up the payload for delivery

    payload = {
        "wiki_page[title]": content.title,
        "wiki_page[body]": new_description
        }

    page_url = f"{auth.API_PATH}/courses/{course_id}/pages/{content.slug}"

    put_response = requests.put(page_url, headers=headers, data=payload)
    print(content.title, 'Completed')
    print(f"The lesson can be found at: {put_response.json()['url']}")
    



def course_query(instance, course_id, destination=None, output='yml'):
    auth = credentials.Credentials(instance)
    headers = {
            'Authorization': f'Bearer {auth.API_KEY}'
            }
    course_file = []
    course_url = f'{auth.API_PATH}/courses/{course_id}'
    course_response = requests.get(course_url, headers=headers)
    course_file.append(course_response.json())

    done = False
    page = 1
    pages = []
    while(not done):
        page_url = f"{auth.API_PATH}/courses/{course_id}/modules?per_page=100&page={page}"
        page_response = requests.get(page_url, headers=headers)
        response_list = page_response.json()
        for i, module in enumerate(response_list):
            items_url = module['items_url']
            items_response = requests.get(items_url, headers=headers)
            response_list[i]['module_items'] = items_response.json()
        pages.extend(response_list)
        if (len(response_list) < 100):
            done = True
        else:
            page += 1
    course_file[0]['modules'] = pages
    
    if output == 'yml':
        course_contents = course_file
    if output == 'csv':
        course_items = []
        for module in pages:
            course_items.extend(module['module_items'])
        course_items_df = pd.DataFrame(course_items)

        course_contents = course_items_df.to_csv(destination)
    return course_contents


def update_lesson(lesson, instance, sc, remote, course_id, remote_url=''):
    auth = credentials.Credentials(instance)
    
    headers = {
            'Authorization': f'Bearer {auth.API_KEY}'
            }

    if remote:
        content = lesson_content.GithubContent(lesson, auth.instance, sc, remote_url, course_id)
    else:
        content = lesson_content.LocalContent(auth.instance, course_id, sc)
    
    if sc:
        new_description = f'{content.data_element} {content.header} {content.intro} {content.button} {content.meta}'
        
    else:
        new_description = f'{content.data_element} {content.header} {content.html} {content.meta}'

        # setting up the payload for delivery
        
    if lesson.type == 'a':

        payload = {
            "assignment[name]": lesson.name,
            "assignment[id]": lesson.id,
            "assignment[description]": new_description,
            "assignment[submission_types]": ['none'],
            "external_tool_tag_attributes": 'none'
            }

        assignment_url = f"{auth.API_PATH}/courses/{lesson.course_id}/assignments/{lesson.id}"

        put_response = requests.put(assignment_url, headers=headers, data=payload)
        print(lesson.name, 'Completed')
        print(f"The lesson can be found at: {put_response.json()['html_url']}")
    
    if lesson.type == 'page':
        payload = {
        "wiki_page[body]": new_description
        }

        page_url = f"{auth.API_PATH}/courses/{course_id}/pages/{content.slug}"

        put_response = requests.put(page_url, headers=headers, data=payload)
        print(content.name, 'Completed')
        print(f"The lesson can be found at: {put_response.json()['url']}")