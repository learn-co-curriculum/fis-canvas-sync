import canvas_interface
#import canvas_dotfile
import credentials
import lesson_content
import saturncloud
import argparse
from latex import latex_to_img
import images

parser = argparse.ArgumentParser(description="Canvas interface for Flatiron School")

parser.add_argument('course_id', type=int, help='Canvas course ID', default=0, nargs='?')

parser.add_argument('-i', '--instance', type=str, default='c', choices=['c', 'e', 'm', 'a', 'v', 'C'], help='Canvas instance abbreviation')

parser.add_argument('-q', '--query')

parser.add_argument('--csv', action='store_true')

parser.add_argument('--fix_images', action='store_true', help="fix image url's and upload the image to the FIS s3 bucket")

parser.add_argument('-c', '--create', action='store_true', help='creates a new lesson')

parser.add_argument('-r', '--remote', action='store_true', help='the location of the repository you are working with. default=false. If it is remote you must provide the url location with --repo_url')

parser.add_argument('--remote_url', help='Github repository url')

parser.add_argument('--s3_directory', help="directory to store the images in the FIS s3 bucket. For example, data science would use `data-science/images`")

parser.add_argument('-d', '--data_science', action='store_true', help='if the course you are working on is a data science course, use this flag for automatic SaturnCloud functionality')

parser.add_argument('-v', '--version', help='current version', action='store_true')

parser.add_argument('--saturn_update', action='store_true', help='update saturncloud links in the course')

parser.add_argument('--sc', action='store_true', help='the lesson is a saturncloud lesson and will need a button created or updated.')

parser.add_argument('-u', '--update', action='store_true', help='update an existing lesson in canvas')

parser.add_argument('--type', choices=['p', 'a'], help='Specify whether the lesson is an assignment or a page')

parser.add_argument('--id', help='Assignment id or the sluggified version of the page name')

parser.add_argument('--output', default='yml', help='output "csv", or "yml". Default is "yml". Must provide destination path')

parser.add_argument('--destination_path', help='destination path to save file. Must include file name and extension')
args = parser.parse_args()

#this line is for testing and will be removed at distribution
print(args)

# Initialize credentials for Canvas API interaction
auth = credentials.Credentials(args.instance)
    
if args.fix_images:
    images.fix_image_src(args.remote_url, args.s3_directory, args.remote)
    
if args.version:
    print("Version 0.0.1")

if args.saturn_update:
    links = saturncloud.UpdatedLinksDf()
    saturncloud.update_course(auth.API_KEY, auth.API_PATH, auth.instance, args.course_id, links.df)

if args.update:
    lesson = canvas_interface.Get_lesson(args.course_id, args.id, args.instance, args.type)
    lesson = lesson.get_lesson()
    canvas_interface.update_lesson(lesson, args.instance, args.sc, args.remote, args.course_id, args.remote_url)
    
if args.create:
    if args.type == 'a':
        canvas_interface.create_assignment(args.instance, args.course_id, args.remote, remote_url=args.remote_url, sc=args.sc)
    if args.type == 'p':
        canvas_interface.create_page(args.instance, args.course_id, args.remote, remote_url=args.remote_url, sc=args.sc)

if args.query:
    if args.output == 'yml':
        canvas_interface.course_query(args.instance, args.course_id, args.destination_path, args.output)
    if args.output == 'csv':
        canvas_interface.course_query(args.instance, args.course_id, args.destination_path, args.output)
    

