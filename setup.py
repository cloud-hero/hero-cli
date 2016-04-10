from constants import CLI_VERSION
from distutils.core import setup

LONG_DESCRIPTION = ('Use hero to create any type of server environments or '
                    'a scalable container service on top of major public or '
                    'private cloud providers.')


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

    install_requires=['paramiko==1.15.2', 'requests==2.9.1', 'click==6.4'],
    download_url='https://github.com/cloud-hero/hero-cli/tarball/0.2',
    keywords=['cloud', 'aws', 'digital ocean', ''],

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
        'Topic :: Utilities'
    ],
)
