from setuptools import setup

setup(
    name='GithubArchiver',
    version='0.0.1',
    packages=['GithubArchiver'],
    url='',
    license='MIT',
    author='joubin',
    author_email='joubin.jabbari@owasp.org',
    description='Github Archiver',
    entry_points={
        'console_scripts': ['GithubArchiver=GithubArchiver.command_line:main'],
    }
)
