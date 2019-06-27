from setuptools import setup

from cwt_cert._version import __version__

setup(
    name='cwt-cert',
    description='Certification tool for Official ESGF Compute nodes',
    packages=['cwt_cert'],
    package_data={
        "": ["*.json"]
    },
    author='Jason Boutte',
    author_email='boutte3@llnl.gov',
    version=__version__,
    url='https://github.com/ESGF/esgf-compute-cert',
    entry_points={
        'console_scripts': [
            'cwt-cert=cwt_cert:main',
        ]
    },
)
