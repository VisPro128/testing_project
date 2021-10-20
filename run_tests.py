import os

os.system("coverage run --branch -m pytest tests.py")
os.system("coverage html")