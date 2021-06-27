"""One command to run Coverage"""
set -e  # Configure shell to exit if one command fails
coverage erase
coverage run manage.py test --settings=docvault.test_settings
coverage report