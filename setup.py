from setuptools import setup

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='characterai'
    version='0.2.7',
    author='kramcat',
    description='An unofficial API for character.ai for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kramcat/CharacterAI',
    packages=['characterai'],
    install_requires=['playwright==1.32.1'],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],
)
