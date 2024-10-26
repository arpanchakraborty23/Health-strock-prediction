from setuptools import setup,find_packages
from typing import List

Hypen_dot_e='-e .'
def get_requirements(filepth:str)->[List]:
    requirements=[]
    with open(filepth) as f:
        requirements=f.readlines()
        requirements=[req.replace('/n','') for req in requirements]

        if Hypen_dot_e in requirements:
            requirements.remove(Hypen_dot_e)

    return requirements

setup(
    name='Health-stroke-Prediction',
    version='0.3',
    author='Arpanchakraborty23',
    author_email='arpanchakaborty500@gmail.com',
    url='https:\\github.com/arpanchakraborty23/Health-strock-prediction.git',
    packages=find_packages(),
    install_requries=get_requirements('requirements.txt')
)