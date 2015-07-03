from setuptools import setup, find_packages


requires = [
    'clld>=0.20',
    'clldmpg>=0.5',
    'pyramid>=1.5.1',
    'SQLAlchemy==0.9.8',
    'transaction',
    'pyramid_tm',
    'zope.sqlalchemy',
    'waitress',
]

tests_require = [
    'WebTest >= 1.3.1', # py3 compat
    'mock',
]


setup(name='grambank',
      version='0.0',
      description='grambank',
      long_description='',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=tests_require,
      test_suite="grambank",
      entry_points="""\
[paste.app_factory]
main = grambank:main
""",
      )
