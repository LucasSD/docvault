![](docvaultcover.png)
# Introduction


The aim of this project was to create a website to upload and store important documents. The website is currently not deployed, having been deployed previously using AWS Elastic Beanstalk.

## To Use

The site is fairly self-explanatory. New users must first register and log in. Once logged in, users can upload, view, download, or delete their documents from the database. Multiple file uploads are possible. Users can only view their own documents. Documents can be assigned tags to categorise them on upload (tags must currently be added in admin though). Passwords can be changed when logged in, and can be reset if forgotten via an e-mail link. 

## Technologies

Python 3.9, Django==3.2.4, coverage==5.5, Black, AWS Elastic Beanstalk

## Getting Started and Contributing

Please follow the instructions below to run this application. Feel free to create your own branch, make a change, and submit a pull request. 

1 - fork this repository
2 - install Python 3.9 if you haven't already

## (Optional) Create and use a virtual environment:
## https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment
```python -m venv env```

```source env/bin/activate```

## Install Django and my other dependencies (ensure you are in the coding-exercise-main directory):
## https://pip.pypa.io/en/stable/user_guide/#requirements-files
```pip install -r requirements.txt```

## Run my tests (all should pass):
```python manage.py test --settings=docvault.test_settings```

## Optional: run Coverage (using batch file) to receive a test coverage report in stdout
```cvrg.bat```

## Build the database:
```python manage.py migrate --settings=docvault.dev_settings```

## Start the Django development server:
## https://docs.djangoproject.com/en/3.2/ref/django-admin/#django-admin-runserver
```python manage.py runserver --settings=docvault.dev_settings```


After these commands, you should be able to see the homepage at http://localhost:8000/.

You will need to create a super user to access the Django admin site and to 
login (https://docs.djangoproject.com/en/3.2/ref/contrib/admin/): to do this, 
run `python manage.py createsuperuser --settings=docvault.dev_settings` and follow the instructions. 

It's a small part of the website's functionality, but for e-mails to send correctly for resetting forgotten passwords, you will need to set up an email server and update the e-mail settings in your dev_settings.py file. You can set them as environment variables or hard code them. I recommend https://www.sendinblue.com because it's free, quick and easy.  

## Project Status

Still being developed. 
###### To do:

- Deploy once again using AWS or similar
- Enable file uploads from mobile devices
- Add a way of checking for duplicate file uploads
- Improve tag functionality, so that users can create tags themselves and filter by them
- Add an update view, so that the tags for a document can be edited by the user
- Add integrated tests using Selenium
