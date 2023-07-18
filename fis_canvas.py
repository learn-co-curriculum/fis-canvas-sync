#import canvas_interface
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

parser.add_argument('--fix-images', action='store_true', help="fix image url's and upload the image to the FIS s3 bucket")

parser.add_argument('-r', '--remote', action='store_false', help='the location of the repository you are working with. default=true. If it is remote you must provide the url location with --repo_url')

parser.add_argument('--repo_url')

parser.add_argument('--s3_directory', help="directory to store the images in the FIS s3 bucket. For example, data science would use `data-science/images`")

parser.add_argument('-d', '--data_science', action='store_true', help='if the course you are working on is a data science course, use this flag for automatic SaturnCloud functionality')

parser.add_argument('-v', '--version', help='current version', action='store_true')

parser.add_argument('--saturn_update', action='store_true', help='update saturncloud links in the course')

args = parser.parse_args()

#this line is for testing and will be removed at distribution
print(args)

# Initialize credentials for Canvas API interaction
auth = credentials.Credentials(args.instance)

if args.remote == False:
    content = lesson_content.LocalContent()

if args.data_science:
    content = latex_to_img(content)

if args.fix_images:
    images.fix_image_src(args.repo_url, args.s3_directory)
    
if args.version:
    print("Version 0.0.1")

if args.saturn_update:
    links = saturncloud.UpdatedLinksDf()
    saturncloud.update_course(auth.API_KEY, auth.API_PATH, auth.instance, args.course_id, links.df)

