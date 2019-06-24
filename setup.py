from setuptools import setup

setup(
    name='cwt-cert',
    description='Certification tool for Official ESGF Compute nodes',
    packages=['cwt_cert'],
    package_data={
        "": ["*.json"]
    },
    author='Jason Boutte',
    author_email='boutte3@llnl.gov',
    version='0.1.0',
    url='https://github.com/ESGF/esgf-compute-cert',
    entry_points={
        'console_scripts': [
            'cwt-cert=cwt_cert:main',
        ]
    },
)
