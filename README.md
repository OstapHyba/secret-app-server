# Secret app (server)
Demo version available here: http://oscargibson.pythonanywhere.com/secret/
---
## Requirements:
1. Python3+
2. virtualenv
## Install (on Linux or Mac):
1. Clone repo
`git clone <this repo>`
2. Create and activate virtual environment
`virtualenv venv -p python3`
`source venv/bin/activate`
3. Install packages
`pip install -r requirements/dev.txt` 
4. Migrate DB
`python manage.py migrate`
5. Run server on localhost
`python manage.py runserver`
### Go to http://localhost:8000/secret

6. Run tests
`python manage.py test`