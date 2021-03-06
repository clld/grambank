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
        'cldfcatalog',
        'clld>=6.0.1',
        'clldmpg>=3.5.0',
        'clld-glottologfamily-plugin',
        'clld-phylogeny-plugin',
        'pyglottolog>=2.0',
        'sqlalchemy',
        'waitress',
    ],
    extras_require={
        'dev': [
            'flake8',
            'psycopg2',
            'tox',
        ],
        'test': [
            'mock',
            'pytest>=3.6',
            'pytest-clld',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
            'selenium',
            'zope.component>=3.11.0',
        ],
    },
    test_suite="grambank",
    entry_points={
        'console_scripts': [
            'grambank-app=grambank.__main__:main',
        ],
        'paste.app_factory': [
            'main = grambank:main',
        ],
    },
)
