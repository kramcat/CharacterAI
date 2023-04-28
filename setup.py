from setuptools import setup

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='CharacterAPI',
    version='0.1.0',
    author='kramcat',
    description='An unofficial API for character.ai for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kramcat/CharacterAPI',
    packages=['CharacterAPI'],
    install_requires=open('requirements.txt').read().strip().split('\n'),
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],
)