
from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name = 'PbIO4',
    version = '0.1.70',
    description = 'Python-based Interface for Online-Judges.',
    long_description = 'Interace with Online Judges with one set of API in Python.',
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Intended Audience :: Education',
        'Programming Language :: C',
        'Programming Language :: C#',
        'Programming Language :: C++',
        'Programming Language :: Go',
        'Programming Language :: Haskell',
        'Programming Language :: Java',
        'Programming Language :: Pascal',
        'Programming Language :: Perl',
        'Programming Language :: PHP',
        'Programming Language :: Python',
        'Programming Language :: Python',
        'Topic :: Education :: Testing',
    ],
    keywords = 'api interface oi oj',
    url = 'https://github.com/jeffswt/PbIO4',
    author = 'PbIO4',
    author_email = '',
    license = 'LGPLv3',
    packages = [
        'PbIO4',
    ],
    install_requires = [
        'requests',
        'bs4',
        'html5lib',
        'Pillow',
    ],
    entry_points = {
    },
)
