from setuptools import setup, find_packages


setup(
    name='grambank',
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
    install_requires=[
        'clldmpg~=3.1.0',
        'clld-glottologfamily-plugin>=2.0.0',
        'pyglottolog>=0.3.1',
    ],
    extras_require={
        'dev': ['flake8', 'waitress'],
        'test': [
            'psycopg2',
            'tox',
            'mock',
            'pytest>=3.1',
            'pytest-clld',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
            'selenium',
            'zope.component>=3.11.0',
        ],
    },
    test_suite="grambank",
    entry_points="""\
[paste.app_factory]
main = grambank:main
""",
)
