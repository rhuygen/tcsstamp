"""Setup script for tcs-stamp-converter"""
import os
import pathlib
import sys
from shutil import rmtree

from setuptools import setup, Command

# Package meta-data.

NAME = "tcs-stamp-converter"
PACKAGE_NAME = "tcsstamp"
DESCRIPTION = "Convert the telemetry stream from the TCS EGSE into a STAMP compatible interface."
URL = "https://github.com/rhuygen/tcsstamp"
EMAIL = "rik.huygen@kuleuven.be"
AUTHOR = "Rik Huygen"
REQUIRES_PYTHON = '>=3.8.0'
VERSION = None

# The directory containing this file

HERE = pathlib.Path(__file__).parent

# The text of the README file

README = (HERE / "README.md").read_text()

# Load the package's __version__.py module as a dictionary.

about = {}
if VERSION is None:
    with open(os.path.join(HERE, PACKAGE_NAME, '__version__.py')) as f:
        exec(f.read(), about)
        VERSION = about['__version__']


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package to PyPI.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(HERE, 'dist'))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system(f"{sys.executable} setup.py sdist bdist_wheel --universal")

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system(f"git tag v{VERSION}")
        os.system('git push --tags')

        sys.exit()


class UploadTestCommand(Command):
    """Support setup.py upload-test."""

    description = 'Build and publish the package to Test PyPI.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(HERE, 'dist'))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system(f"{sys.executable} setup.py sdist bdist_wheel --universal")

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload --repository-url https://test.pypi.org/legacy/ dist/*')

        sys.exit()


# This call to setup() does all the work

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["tcsstamp"],
    extras_require={
        "fancy output": ["rich"]
    },
    entry_points={
        "console_scripts": [
            "tcs_stamp=tcsstamp.__main__:main",
            "echo_server=tcsstamp.echo_server:main",
        ]
    },
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
        'upload_test': UploadTestCommand,
    },
)
