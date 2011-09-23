from setuptools import setup, find_packages

setup(
    name='michel',
    version='0.0.6',
    author='Christophe-Marie Duquesne',
    author_email='chm.duquesne@gmail.com',
    packages=find_packages(),
    url='https://github.com/chmduquesne/michel',
    license=open('LICENSE.txt').read(),
    description='pushes/pull flat text files to google tasks',
    long_description=open('README.md').read(),
    install_requires = ['google-api-python-client'],
    entry_points=("""
    [console_scripts]
    michel = michel.michel:main
    """)
)
