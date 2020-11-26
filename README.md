# Better Classroom

A terminal app to fetch study materials (pdf, ppt and doc for now) from Google Classroom easily.

## Steps to use
- Clone the repo
- Go to https://developers.google.com/classroom/quickstart/python download credentials.json and rename it as classroom_creds.json and put in project folder
- Go to https://developers.google.com/drive/api/v3/quickstart/python download credentials.json and rename it as client_secrets.json and put in project folder
- Run main.py
- For the first run, you will be asked to authenticate classroom as well as drive apis, using a link, do that
- Now type the material name (for eg, if material is "UML diagrams", just typing uml is enough)
- The file(s) will be downloaded in the 'materials' folder in project folder
- Run all_of_sub.py if you want to get all materials of a course
- The files will be downloaded to a new folder of the course within materials folder
- Run lsd.py (after changing the hardcoded course id inside it) if any of your sirs posts Youtube vids for materials :joy::joy:
- The links to the videos and the material title will be saved as a csv
- Now Say goodbye to scrolling through sluggish classroom website!!

##### More updates coming soon!
##### Contributions will be appreciated :slightly_smiling_face:
