from setuptools import setup,find_packages
from typing import List

HYPEN_E_DOT = '-e .'
def get_requirements(source_path:str) -> List[str]:
    requirements =[]
    with open(source_path,'r') as file_obj:
        requirements = file_obj.readlines()
        [req.replace('\n','') for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements

setup(
    name = 'Whatsapp chat analyser',
    version = '0.1',
    author_name = 'Mr Khan',
    author_email= 'aqleemhan408@gmail.com',
    requires= get_requirements('requirements.txt'),
    pakcages = find_packages()

)
