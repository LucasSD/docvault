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
python manage.py test --settings=docvault.test_settings

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
