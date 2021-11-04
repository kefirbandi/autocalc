from os import path
import codecs
from setuptools import setup, find_packages

import versioneer

HERE = path.abspath(path.dirname(__file__))

with codecs.open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

test_requires = [
    # add test dependencies here
]

doc_build_requires = [
    'sphinx',
    'sphinx-rtd-theme',
    'sphinx-argparse',
    'nbsphinx',
]

extras_require = {
    'test': test_requires,
    'doc_build': doc_build_requires
}

if __name__ == "__main__":
    setup(
        name='autocalc',
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        packages=find_packages(exclude=('tests',)),
        include_package_data=True,      
        url='',
        license='MIT',
        author='Andras Gefferth',
        author_email='andras.gefferth@gmail.com',
        description='A framework to keep track of dependencies in non-linear workflows',
        long_description=LONG_DESCRIPTION,
        install_requires=[
            'IPython',
            'ipywidgets'
        ],
        test_requires=test_requires,
        extras_require=extras_require
    )

