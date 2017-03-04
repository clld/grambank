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
        'clld>=3.2.0',
        'clldmpg>=2.0.0',
        'clld-glottologfamily-plugin>=2.0.0',
        'pyglottolog>=0.3.1',
    ],
    tests_require=[
        'WebTest >= 1.3.1',  # py3 compat
        'mock',
    ],
    test_suite="grambank",
    entry_points="""\
[paste.app_factory]
main = grambank:main
""",
)
