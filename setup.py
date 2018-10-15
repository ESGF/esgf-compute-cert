from setuptools import setup

setup(name='esgf-compute-cert', version='0.1.0', packages=['cwt_cert'],
      entry_points={
          'console_scripts': [
              'cwt_cert = cwt_cert.cli:run',
          ]
      })
