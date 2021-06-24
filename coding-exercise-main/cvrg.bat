"""One command to run Coverage"""
set -e  # Configure shell to exit if one command fails
coverage erase
coverage run manage.py test --settings=nomio.test_settings
coverage report