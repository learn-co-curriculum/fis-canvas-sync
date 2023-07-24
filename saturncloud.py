# takes the lesson name and returns the SaturnCloud link from the df
import requests
import markdown
import os
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
from datetime import date
import canvas_interface
from io import StringIO
import credentials
import lesson_content

# create a list of the lessons with an external tool
def list_of_illumidesk_assignments(assignments):
    external_tool_assign = list(filter(lambda x: "external_tool_tag_attributes" in x.keys(), assignments))
    # filtering to only include the lessons with an illumidesk external tool
    illumidesk_assign = list(filter(lambda x: "url" in x["external_tool_tag_attributes"].keys() and x["external_tool_tag_attributes"]["url"].startswith("https://flatiron.illumidesk.com"), external_tool_assign))
    return external_tool_assign, illumidesk_assign

class UpdatedLinksDf:
    """
    pulls the csv file from the saturncloud github repository and saves it as links_updated_{today's date}.csv
    assigns a dataframe to self.df
    """
    def __init__(self):
        today = date.today().strftime('%m_%d_%Y')
        file_location = 'https://raw.githubusercontent.com/saturncloud/flatiron-curriculum/main/links.csv'
        file_raw = requests.get(file_location)
        file_text = file_raw.text
        file_csv = StringIO(file_raw.text)
        df_raw = pd.read_csv(file_csv)

        #with open(f'links_updated_{today}.csv', 'w') as f:
            #f.write(file_text)

        # create a dataframe of the links for SaturnCloud and remove the notebook file from the name for reference
        #df = pd.read_csv(f'links_updated_{today}.csv', index_col=0)
        df = df_raw

        df['local_path'] = df['local_path'].apply(lambda x: x.split('/')[1])
        df_final = df.drop_duplicates(subset=['local_path'])
        self.file_name = os.path.join(os.getcwd(), f'{today}.csv')
        self.df = df_final

class GetSaturnLink:
    """
    requires the lesson name, DataFrame with the SaturnCloud links, and the canvas instance
    returns the saturncloud link from within the DataFrame
    """
    def __init__(self, repo, instance, df):
        print(f'sc repo {repo}')
        print(df.head())
        print(df.loc[df['local_path'] == repo])
        item = df.loc[df['local_path'] == repo]
        if item.empty:
            link = 'None'
            print(f"There is no SaturnCloud link in the DataFrame for {repo}")
        else:
            result = item[instance]
            link = result.item()
        self.link = link

def lesson_name(lesson):
    if lesson['description'] == '':
        return 'Empty', ""
    else:
        try:
            soup = bs(lesson['description'], 'html.parser')
            href = soup.find("a", {'class':"fis-git-link"}).get('href')
            name = href.split('/')[-1]
            return name.strip(), href
        except:
            return 'Empty', ""

# takes the result of get_saturn_link and returns a functional button with the link to the saturncloud lesson
def make_saturn_button(saturn_link):
    today = date.today().strftime('%m_%d_%Y')
    button = f"""<p id="saturncloud_button_{today}"><span style="color: #34495e;"><span style="font-size: 24pt; background-color: #3598db; border: 2px solid;"><a class="inline_disabled" style="background-color: #3598db; color: #34495e;" href="{saturn_link}" target="_blank" rel="noopener"><span style="background-color: #ced4d9;">&nbsp;Click Here to Launch Lesson&nbsp;</span></a></span></span></p>"""
    return button

def get_intro(repo_markdown):
        m = re.search(r'<h2>.*?</h2>.*?<h2>.*?</h2>.*?</ul.*?>', repo_markdown, re.DOTALL)
        s = m.start()
        e = m.end() - len('<h1>')
        target_html = repo_markdown[s:e]
        return target_html
        
def fix_single_sc(API_KEY, API_PATH, canvas_instance, course_id, assignment_id):
    
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    
    assn_url = f"{API_PATH}/courses/{course_id}/assignments/{assignment_id}"
    assn_response = requests.get(assn_url, headers=headers)
    lesson = assn_response.json()
    name, repo_url = lesson_name(lesson)
    if name == "Empty" or name == '':
        pass

    elif canvas_instance in lesson['description']:
        pass

    else:
        print(f'Pulling HTML from {name}')
        try:
            branch = 'main'
            url = f'http://raw.githubusercontent.com/learn-co-curriculum/{name}/{branch}/README.md'
            resp = requests.get(url)
            resp.raise_for_status()
            print(f'{branch} pulled')
        except:
            print(f'Branch is not: {branch}')
            branch = 'master'
            url = f'http://raw.githubusercontent.com/learn-co-curriculum/{name}/{branch}/README.md'
            resp = requests.get(url)
        resp_text = resp.text
        repo_markdown = markdown.markdown(resp_text)

        df = UpdatedLinksDf()

        link = GetSaturnLink(name, df, canvas_instance)

        if link == 'None':
            print(name, 'is not in the DataFrame')
            pass

        else:
            introduction = "<h2>Introduction</h2>"
            objectives = "<h2>Objectives</h2>"

            button = make_saturn_button(link.link)

            if introduction in lesson['description'] or objectives in lesson['description']:
                lesson_header = lesson['description']
                new_description = lesson_header + button
            else:
                lesson_header = lesson['description']
                intro = get_intro(repo_markdown)
                print(name, " had no description, so one was added")
                new_description = lesson_header + intro + button

            # setting up the payload for delivery

            payload = {
                "assignment[name]": f'{lesson["name"]}',
                "assignment[id]": f'{lesson["id"]}',
                "assignment[description]": f'{new_description}',
                "assignment[submission_types]": ['none'],
                "external_tool_tag_attributes": 'none'
                }

            assignment_id = lesson["id"]
        
            assignment_url = f"{API_PATH}/courses/{course_id}/assignments/{assignment_id}"

            put_response = requests.put(assignment_url, headers=headers, data=payload)
            print(put_response)
            print(name, 'Completed')

def update_course(API_KEY, API_PATH, canvas_instance, course_id, df):
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    course = canvas_interface.Course(API_KEY, API_PATH, course_id)
    course.get_assignments()
    
    missing_assignments = []
    for assignment in course.assignments:
        assignment_number = assignment['id']
        assn_url = f"{API_PATH}/courses/{course_id}/assignments/{assignment_number}"
        assn_response = requests.get(assn_url, headers=headers)
        lesson = canvas_interface.Assignment(assn_response.json())
        name = lesson.name
        lesson_url = lesson.url.split('/')[-1]
        print(f'Working on: {lesson.name}')
        
        if name == "Empty":
            pass

        else:
            print(f'Pulling HTML from Github')
            try:
                branch = 'main'
                url = f'http://raw.githubusercontent.com/learn-co-curriculum/{lesson_url}/{branch}/README.md'
                resp = requests.get(url)
                resp.raise_for_status()
                github_content = resp.text
            except:
                branch = 'master'
                url = f'http://raw.githubusercontent.com/learn-co-curriculum/{lesson_url}/{branch}/README.md'
                resp = requests.get(url)
                github_content = resp.text
                
            try:
                html = lesson_content.HtmlBody(lesson.content, github_content, lesson_url)
            except:
                print(f'Failed to extract content from github. Check repository for formatting issues. \nRepo location: http://github.com/learn-co-curriculum/{lesson_url}')
                continue
                

            link = GetSaturnLink(lesson_url, canvas_instance, df)

            button = make_saturn_button(link.link)
            
            new_description = f'{html.data}\n{html.header}\n{html.intro}\n{button}'

                # setting up the payload for delivery

            payload = {
                "assignment[name]": lesson.name,
                "assignment[id]": lesson.id,
                "assignment[description]": new_description,
                "assignment[submission_types]": ['none'],
                "external_tool_tag_attributes": 'none'
                }

            assignment_id = assignment["id"]
        
            assignment_url = f"{API_PATH}/courses/{course_id}/assignments/{assignment_id}"

            put_response = requests.put(assignment_url, headers=headers, data=payload)
            print(put_response)
            print(name, 'Completed')
    if len(missing_assignments) >=1:
        assign_df = pd.DataFrame(missing_assignments)
        assign_df.to_csv(f'missing_{canvas_instance}{course_id}.csv', index=False)
        print(f'There were {len(missing_assignments)} assignments which were not in the SaturnCloud DataFrame, they were stored as "missing_{canvas_instance}{course_id}.csv"')