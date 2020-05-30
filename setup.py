from setuptools import setup
setup(
    name='entropy',
    version='0.1.0',
    description='entropy is a command line friend that helps you reduce entropy in your life',
    long_description=open('README.md').read(),
    author='Gyanendra Mishra',
    author_email='anomaly.the@gmail.com',
    license='MIT',
    keywords=['entropy', 'productivity', 'journaling'],
    url='https://github.com/h4ck3rk3y/entropy',
    install_requires=[
        'colorama>=0.4.3',
        'docopt>=0.6.2',
        'setuptools>=42.0.2'
    ],
    packages=['entropy'],
    entry_points={
        'console_scripts': [
            'entropy = entropy.entropy:main'
        ]
    })
