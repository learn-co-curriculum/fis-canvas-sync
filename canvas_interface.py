import requests
import credentials

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
        
    def get_course_pages(self):
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
    def get_course_assignments(self):
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

        self.assignments = assignments
        self.number_of_assignments = len(assignments)
    
class Assignment:
    def __init__(self, lesson):
        """takes one element of a json response from course.get_course_assignments and converts it to an Assignment object. If creating a new assignment you can pass the information as a dictionary

        Args:
            assignment (json): single element of the response from course.get_course_assignments
        """
        self.id = lesson['id']
        if lesson['force_name']:
            self.name = lesson['force_name']
        else:
            self.name = lesson['name']
        self.content = lesson['description']
        

class Page:
    def __init__(self, lesson):
        self.id = lesson['url']
        
class Get_lesson:
    def __init__(self, course_id, id, instance='c', type='a'):
        """retrieves the lesson contents for a single page or assignment

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
        if type == "a":
            self.type = "assignment"
        else:
            self.type = "page"
        
    def get_lesson(self):
    
        headers = {
                'Authorization': f'Bearer {self.API_KEY}'
            }
        assn_url = f"{self.API_PATH}/courses/{self.course_id}/{self.type}s/{self.id}"
        assn_response = requests.get(assn_url, headers=headers)
        print(assn_url, "\n", assn_response.status_code)
        #return Assignment(assn_response.json())
        lesson = assn_response.json()
        if self.type == "page":
            return Page(lesson)
        if self.type == "assignment":
            return Assignment(lesson)
        
def create_assignment(assignment):
    payload = {
        assignment[name]: assignment.name,
        assignment[description]: assignment.html
    }