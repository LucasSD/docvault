Hi Josh and Jonny

I have written my own _Getting Started_ section below, to run my solution. 

Some points to note:

I seriously considered using Notion to journal my progress, since it's what you use at Nomio. I signed up and it certainly looks helpful. 

I have not yet implemented file validation based on MIME. I understand this will be essential before deployment, togther with other security improvements.

I have a separate test_settings file. 

I have a setup.cfg file to configure Coverage (and a cvrg.bat file to run it more easily from the terminal). 

I have not tested templates directly, but I have tested the context data sent to them. My understanding is that this is considered sufficient by some, but it would be interesting to discuss this point with you. I wanted to run some integrated tests with Selenium, but ran out of time. I believe some of my tests are somewhat integrated anyway. 

I decided not to include type annotation, but would be interested in your guidance on this (I note that you used it in your initial view included in the exercise). 

## Getting Started

Please follow the instructions below to run and test my solution. 

``sh
# (Optional) Create and use a virtual environment:
# https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment
python -m venv env
source env/bin/activate

# Install Django and my other dependencies:
# https://pip.pypa.io/en/stable/user_guide/#requirements-files
pip install -r requirements.txt

# Run my tests(all should pass):
python manage.py test --settings=nomio.test_settings

## Optional: run Coverage (using batch file) to receive a test coverage report in stdout
cvrg.bat

# Build the database:
python manage.py migrate

# Start the Django development server:
# https://docs.djangoproject.com/en/3.2/ref/django-admin/#django-admin-runserver
python manage.py runserver
```

After these commands, you should be able to test my app manually at http://localhost:8000/.

You will need to create a super user to access the Django admin site and to login (https://docs.djangoproject.com/en/3.2/ref/contrib/admin/): to do this, run `python manage.py createsuperuser` and follow the instructions.





######################################################################################################################################

# Nomio Interview Exercise

At Nomio, we turn documents into data. Unsurprisingly, the first step of this is getting the documents from the user.

For your first task, we'd like you to take our existing basic system and add a way for users to upload files.

## Getting Started

You will need to have at least Python 3.6 installed on your machine: if you don't, you can install the latest version [from these instructions](https://wiki.python.org/moin/BeginnersGuide/Download).

Once you have Python installed, you should be able to get set up with the following commands:

```sh
# (Optional) Create and use a virtual environment:
# https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment
python -m venv env
source env/bin/activate

# Install Django:
# https://pip.pypa.io/en/stable/user_guide/#requirements-files
pip install -r requirements.txt

# Start the Django development server:
# https://docs.djangoproject.com/en/3.2/ref/django-admin/#django-admin-runserver
python manage.py runserver
```

After these commands, you should be able to see a page when you visit http://localhost:8000/.

You will need to create a super user to access the [Django Admin site](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/): to do this, run `python manage.py createsuperuser` and follow the instructions.

## What's already done

We've created a basic Django project (`nomio`) with two applications:

- `nomio.landing` is for our basic Landing Page, which simply handles user login at `/`. (You shouldn't need to modify this app as part of this task.)
- `nomio.documents` is for our document listing and uploading application at `/documents`, which hasn't been completed yet. (That's where you come in!)

## What we'd like you to do

- Allow authenticated users to upload files to Nomio.
- Show authenticated users the list of files that they've uploaded. (Don't show files for other users!)
- Allow users to download files that they've uploaded to Nomio.

## What we're looking for

When we get your solution, we will:

- run the instructions in _Getting Started_ to start the server, and assess your solution is complete
- run the tests to ensure they pass
- assess how well your code, tests and documentation are written

## Hints & Tips

- To run the tests, use `python manage.py test`.
- You are free to use as many (or as few!) packages as you like, but make sure they're [specified](https://pip.pypa.io/en/stable/user_guide/#requirements-files) in `requirements.txt` so we install them when setting up your solution.
