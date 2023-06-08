from setuptools import setup, find_packages

with open('README.md', encoding='utf8') as f:
    long_description = f.read()

setup(
    name='characterai',
    version='0.6.0',
    author='kramcat',
    description='An unofficial API for character.ai for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kramcat/characterai',
    packages=find_packages(),
    install_requires=["playwright>=1.32.1"],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],
)
