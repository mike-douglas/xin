from setuptools import setup, find_packages

readme = ''

with open('README.md') as r:
    readme = r.read()

setup(
    name = 'Xin',
    version = '0.1',
    description = 'A command line tool',
    long_description = readme,
    packages = find_packages(),

    entry_points = {
        'console_scripts': [
            'xin = xin:main',
        ],
    },

    test_suite = 'tests',

    include_package_data = True,
    zip_safe=False,

    install_requires = [
    ],

    dependency_links = [
    ]
)
