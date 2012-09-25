import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'pyramid',
    'pyramid_beaker',
    'pyramid_zcml',
    'repoze.tm2',
    'WebError',
    'pywurfl'
    ]

test_requires = [
    "mock",
]

setup(name='mappp.me',
      version='0.0',
      description='mappp.me',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='mappp.me',
      install_requires = requires,
      extras_require = {
        "tests": test_requires,
      },
      entry_points = """\
      [paste.app_factory]
      main = mappp.me:main
      """,
      paster_plugins=['pyramid'],
      )

