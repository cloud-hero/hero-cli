from distutils.core import setup
from pip.req import parse_requirements

from hero.constants import CLI_VERSION

DOWNLOAD_URL = ('https://github.com/cloud-hero/hero-cli/tarball/{version}'
                .format(version=CLI_VERSION))
LONG_DESCRIPTION = ('Use hero to create any type of server environments or '
                    'a scalable container service on top of major public or '
                    'private cloud providers.')

required_packages = [str(package.req)
                     for package in parse_requirements('hero/requirements.txt',
                                                       session=False)]


setup(
    name='hero',
    packages=['hero'],

    version=CLI_VERSION,
    url='https://github.com/cloud-hero/hero-cli',
    description='Simple server environments set-up.',
    long_description=LONG_DESCRIPTION,

    author='CloudHero',
    author_email='founders@cloudhero.io',
    license='GNU General Public License',

    install_requires=required_packages,
    download_url=DOWNLOAD_URL,
    keywords=['CloudHero CLI', 'software-defined infrastructure',
              'Server set-up'],
    entry_points={
        'console_scripts':
            ['hero = hero.hero:hero_cli']
    },

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
)
