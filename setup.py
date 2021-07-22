import os.path
from setuptools import setup, find_packages


THIS = __file__
HERE = os.path.dirname(THIS)
README = os.path.join(HERE, 'README.md')

__author__ = 'ping <lastmodified@gmail.com>, reala10n <downtown2u@gmail.com>'
__version__ = '1.6.0'


with open(README, encoding='utf8') as f:
    long_description = f.read()

setup(
    name='pipaw',
    version=__version__,
    author='ping, reala10n',
    author_email='lastmodified@gmail.com, downtown2u@gmail.com',
    license='MIT',
    url='https://github.com/reala10n/pipaw',
    keywords='instagram private api bot',
    description='A client interface for the private Instagram API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'flake8',
        ],
    },
    packages=find_packages(),
    platforms=['any'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
