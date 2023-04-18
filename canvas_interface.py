import requests

def get_course_assignments(API_KEY, API_PATH, course_id):
    """pulls the data for all assignments and pages in the specified canvas course.

    Args:
        API_KEY (str): api key for the specified canvas instance
        API_PATH (str): api path for the specified canvas instance
        course_id (int): _description_

    Returns:
        json: lessons, assignments, and pages from the specified canvas course.
    """
    
    headers = {
            'Authorization': f'Bearer {API_KEY}'
        }

    done = False
    page = 1
    assignments = []
    while(not done):
        assn_url = f"{API_PATH}/courses/{course_id}/assignments?per_page=100&page={page}"
        assn_response = requests.get(assn_url, headers=headers)
        response_list = assn_response.json()
        assignments.extend(response_list)
        
        if (len(response_list) < 100):
            done = True
        else:
            page += 1

    print(f"There are, {len(assignments)}, assignments in this course")
    return assignments