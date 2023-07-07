#import canvas_interface
#import canvas_dotfile
import credentials
#import lesson_content
#import saturncloud
import argparse

parser = argparse.ArgumentParser(description="Canvas interface for Flatiron School")
parser.add_argument('course_id', type=int, help='Canvas course ID')
parser.add_argument('-i', '--instance', type=str, default='c', choices=['c', 'e', 'm', 'a', 'v'], help='Canvas instance abbreviation')

parser.add_argument('-q', '--query')
parser.add_argument('--csv')
args = parser.parse_args()

#this line is for testing and will be removed at distribution
print(args)

# Initialize credentials for Canvas API interaction
auth = credentials.Credentials(args.instance)

