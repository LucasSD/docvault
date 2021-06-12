set -e  # Configure shell so that if one command fails, it exits
coverage erase
coverage run manage.py test --settings=nomio.test_settings
coverage report