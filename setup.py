import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-merged-inlines',
    version='0.1',
    packages=['merged_inlines'],
    include_package_data=True,
    license='MIT License',
    description='A Django Admin extension that allows you to mix and reorder multiple inline classes together',
    long_description=README,
    url='https://github.com/MattBroach/Django-Merged-Inlines',
    author='Matt Broach',
    author_email='broach@aya.yale.edu',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)