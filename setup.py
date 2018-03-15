from setuptools import setup

with open('README.rst', 'rb') as f:
    readme = f.read().decode('utf-8')

setup(
    name='fifslack-bitbucket-pr-reminder',
    version='0.0.1',
    url='http://github.com/ordenador/fifslack-bitbucket-pr-reminder',
    author='Mario Faundez',
    author_email='mariofaundez@hotmail.com',
    description='Posts a Slack reminder with a list of open pull requests for an organization',
    long_description=readme,
    py_modules=['fifslack_bitbucket_pr_reminder'],
    license='MIT',
    install_requires=[
        'fifbucket==0.4',
        'slackclient==1.1.3'
    ],
    entry_points='''
        [console_scripts]
        fifslack-bitbucket-pr-reminder=fifslack_bitbucket_pr_reminder:cli
    '''
)
