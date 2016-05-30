#!/usr/bin/python
"""Use to clean the directory after the run of HubArchiveCreator.py manually"""
import os
import shutil

# Remove 'myHub.zip at root folder
try:
    os.remove('myHub.zip')
except OSError as o:
    # We don't need to crash the program
    print 'Warning: ' + str(o)

# Remove 'myHub' folder and its content
shutil.rmtree('myHub', ignore_errors=True)
