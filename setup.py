import os

from setuptools import find_packages, setup

with open('version') as fd:
    version = fd.read().strip()

with open('requirements.txt') as fd:
    requirements = [
        dependency.strip() for dependency in
        [
            (dep.split('#', 1)[0]).strip() for dep in fd
        ]
        if dependency
    ]


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='taxwise',
    version=version,
    url='https://github.com/iamkhaya/taxwise',
    author='Khayelihle Tshuma',
    author_email='khayelihle.tshuma@gmail.com',
    description=('A tax application'),
    long_description=read('Readme.md'),
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    project_urls={
        'Source': 'https://github.com/iamkhaya/taxwise',
        'Tracker': 'https://github.com/iamkhaya/taxwise',
    },
)
