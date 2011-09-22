from setuptools import setup, find_packages

setup(
    name='michel',
    version='0.0.1',
    author='Christophe-Marie Duquesne',
    author_email='chm.duquesne@gmail.com',
    packages=find_packages(),
    url='https://github.com/chmduquesne/michel',
    license='LICENSE.txt',
    description='pushes/pull flat text files to google tasks',
    long_description=open('README.md').read(),
    install_requires = ['google-api-python-client'],
    entry_points=("""
    [console_scripts]
    michel = michel.michel:main
    """)
)
