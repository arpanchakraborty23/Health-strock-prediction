import os
import logging
from pathlib import Path

list_of_files=[
    '.github/workflow',
    'Dataset',
    'expriment/EDA.ipynb',

    'src/components/__init__.py',
    'src/pipline/__init__.py',
    'src/logging/__init__.py',
    'src/exception/__init__.py',
    'src/utils/__init__.py',
    'src/constant/__init__.py',
    'src/entity/__init__.py',
    'src/config_manager/__init__.py',
    '.gitignore',
    'LICENCE',

    'templates/index.html',
    'setup.py',
    'requirements.txt',
    'README.md',
    'params.yaml',
    'config/config.yaml' 
]

for filepath in list_of_files:
    filepath=Path(filepath)
    filedir,filename=os.path.split(filepath)
    if filedir!="":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file: {filename}")
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath,"w") as f:
            pass #create an empty file