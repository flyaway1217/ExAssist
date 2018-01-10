from setuptools import setup
import os

import ExAssist

PACKAGE_NAME = 'ExAssist'
REQUIREMENT_DIR = 'requirements'


with open(os.path.join(REQUIREMENT_DIR, 'dev-requirements.txt')) as f:
    tests_require = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, 'requirements.txt')) as f:
    install_require = [line.strip() for line in f if line.strip()]

setup(
        name=PACKAGE_NAME,
        version=ExAssist.__version__,
        packages=['ExAssist'],
        url='https://github.com/flyaway1217/ExAssist',
        license='GPL',
        keywords='Experiment Assist',

        author='Flyaway',
        author_email='flyaway1217@gmail.com',

        description='Experiment Assist',
        long_description=open('README.rst', encoding='utf8').read(),
        install_requires=install_require,
)
