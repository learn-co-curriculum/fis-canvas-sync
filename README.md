# FIS-Canvas package

## fis-canvas.py
Main 
Main script which will accept all arguments and execute all necessary functions
	Arguments:
* <course_id> 
(positional in the first position)
Canvas course ID as an integer.
* <--instance>, <-i>
 * Canvas instance
  * ‘c’ - Consumer
(Default)
  * ‘e’ - Enterprise
  * ‘m’ - Moringa
  * ‘a’ - Academy Xi
  * ‘v’ - Vanguard
* <--query>, <-q>
Retrieves the course information from Canvas and returns it as a yaml file. Specify the destination path directly after the flag. Default output is `.yml`
* <--csv>
Changes the output of <query> to csv. Specify the destination path directly after the flag.

## credentials.py
class Credentials
This will select the proper credentials as environment variables. The variables need to be set up with the following format:
* <INSTANCE>_CANVAS_API_KEY
* <INSTANCE>_CANVAS_API_PATH
* Requires <instance>
* Returns the necessary variables for authentication as a credentials object.
credentials.API_PATH
credentials.API_KEY
Credentials.instance

canvas_interface.py
class Course
Creates a course object.
<Course.pages>
Contains all of the lessons in the course with the type ‘page’
<Course.assignments>
Contains all of the lessons in the course with type ‘assignment’
<Course.get_pages()>
Pulls all lessons with the type ‘page’ and returns a list of json objects
<Course.get_assignments()>

Class Assignment
Creates an Assignment object
<Assignment.id> - the canvas assignment id
<Assignment.name> - the name of the assignment which will be pulled from the repository information.
<Assignment.force_name> - a custom name for the assignment which will override the name derived from the repository.
<Assignment.content> - the html content of the repository. This will be pulled from github and converted to html. 
FIS header will be added to the beginning of the content. 
FIS data tag will be added to the beginning of the content. 
SaturnCloud button will be added to the end if it is a DataScience SaturnCloud lesson

Images
Checks for images with relative links and or references and uploads the image to FIS s3 bucket and modifies the img tag to include the updated src reference.


