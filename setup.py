from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='python-toggl',
      version='0.1.10',
      description='Python Wrapper for Toggl API',
      long_description=readme(),
      url='https://github.com/swappsco/toggl-python-api-client',
      author='mechastorm',
      author_email='dev@swapps.co',
      license='MIT',
      packages=['toggl'],
      install_requires=[
          'requests',
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'httpretty'],
      zip_safe=False)
