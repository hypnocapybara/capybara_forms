import os
import re
from io import open

from setuptools import setup


with open('README.md') as f:
    long_description = f.read()


setup(
    name='capybara_forms',
    version='0.0.2',
    packages=[
        'capybara_forms',
        'capybara_forms.renderers',
        'capybara_forms.migrations',
        'capybara_forms.static',
        'capybara_forms.templates',
    ],
    include_package_data=True,
    install_requires=['Django'],
    url='https://github.com/kenny1992/capybara_forms',
    license='',
    author='kenny1992',
    author_email='apolevki09@gmail.com',
    description='Dynamic Django forms and filters using JSON schema',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
)
