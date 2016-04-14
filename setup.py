from distutils.core import setup
from pip.req import parse_requirements

from lib.constants import CLI_VERSION

DOWNLOAD_URL = ('https://github.com/cloud-hero/hero-cli/tarball/{version}'
                .format(version=CLI_VERSION))
LONG_DESCRIPTION = ('Use hero to create any type of server environments '
                    'on top of major public or private cloud providers. '
                    'An example of such a server environment is a scalable '
                    'container service.')

required_packages = [str(package.req)
                     for package in parse_requirements('requirements.txt',
                                                       session=False)]


setup(
    # Basic metadata
    name='hero',
    version=CLI_VERSION,
    author='CloudHero',
    author_email='founders@cloudhero.io',
    url='https://github.com/cloud-hero/hero-cli',

    # Additional information
    description='Simple server environments set-up.',
    long_description=LONG_DESCRIPTION,
    license='GNU General Public License',

    # How to do the install
    download_url=DOWNLOAD_URL,
    install_requires=required_packages,
    packages=['lib'],
    scripts=[
        'hero',
    ],

    # How to do the tests
    # TODO

    # PyPI metadata.
    # Entire list here:
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Shells'
    ],
    keywords=['CloudHero CLI', 'software-defined infrastructure',
              'Server set-up'],
)
