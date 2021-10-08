from setuptools import setup


with open('requirements.txt', 'r') as f:
    install_reqs = [
        s for s in [
            line.split('#', 1)[0].strip(' \t\n') for line in f
        ] if s != ''
    ]


with open("README.md", 'r') as f:
    long_description = f.read()


setup(
    name='Volby.cz',
    version='0.1',
    description='Module for retrieving and parsing open data from the website volby.cz, portal of the '
                'Czech Statistical Office in the Czech Republic, presenting the election results.',
    author='Jakub Janeček',
    author_email='jakub.janecek@fw-fw.cz',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/geekmoss/py-volby.cz',
    install_requires=install_reqs,
    packages=['volby_cz'],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)