import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'pyramid_mako',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'passlib',
    'psycopg2',
    'webhelpers2',
    'alembic',
    'awesome-slugify',
    'wtforms',
    'markdown2',
    'pytils',
    'paginate',
    'pillow',
    'paginate_sqlalchemy',
    ]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-cov',
    ]

setup(name='kindergarden',
      version='0.0',
      description='kindergarden',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
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
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = kindergarden:main
      [console_scripts]
      initialize_kindergarden_db = kindergarden.scripts.initializedb:main
      """,
      )
