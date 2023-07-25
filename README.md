# FIS-Canvas package
This package is meant to be an all inclusive tool for FIS curriculum developers to help with the interaction between canvas, your local machine, and github. This tool will create Pages and Assignments, update existing Pages and Assignments, as well as convert LaTeX equations and upload 

# Installation
- Clone the repository to your machine.
- Note the path where you cloned it to. it should be something similar to:
> /Users/{username}/fis-canvas-sync/
The main script is named `fis-canvas.py`
In order to run the script you will need to type the following command in the command line:
> python /Users/{username}/fis-canvas-sync/fis-canvas.py {arguments}

## Requirements

Authorization and credential handling is handled by credentials.py. Inside you will find a Credentials class which return a credentials object (normally called auth) which contains API_KEY, API_PATH, instance. In order for this to function you will need the proper credentials for the instance you are working with stored as an environment variable formatted in the following manner using enterprise as the example (replace “ENTERPRISE” with the instance of your need.)
- ENTERPRISE_CANVAS_API_KEY={your api key here}
- ENTERPRISE_CANVAS_API_PATH=https://my.learn.co/api/v1

For working with the images and uploading to the s3 bucket, you will need the proper credentials set up for the bucket. If you need these you will need to reach out to me. The following credentials are necessary:

- PATH=/usr/local/bin:$PATH

- AWS_ACCESS_KEY_ID={awx access key id}

- AWS_SECRET_ACCESS_KEY={secret access key}

- AWS_REGION={proper region settings}



### Create an Alias
In order to make the usage much easier, you may want to create an alias in your `.bash_profile`.   
To create the alias, simply add the following line to your `.bash_profile`:  
`alias fis-canvas="python {insert the path to the repository location}/fis-canvas-sync/fis-canvas.py"`

### Example
You have a lesson cloned to your local machine and you want to update the content in a consumer course with the course number 6363 and a assignment number 214169. Following is a summary of the necessary information to perform this task:
{course_id}: 6363 (this is positional)
{instance}: consumer
{assignment_number}: 214169
{lesson_type}: a
{saturncloud}: yes
{operation}: update

In order to process this command you would enter the following command:

`python /Users/{username}/fis-canvas-sync/fis-canvas.py fis-canvas 6363 --update --id 214169 --type a --sc`


## fis-canvas.py
Main 
Main script which will accept all arguments and execute all necessary functions
	Arguments:
* <course_id> 
(positional in the first position)
Canvas course ID as an integer.
* <--instance>, <-i>
 * Canvas instance
  - ‘c’ - Consumer
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

# Usage

## Update an assignment or page
fis-canvas 6363 --update --id 214169 --type a --sc


