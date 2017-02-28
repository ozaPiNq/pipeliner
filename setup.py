from setuptools import setup, find_packages


setup(
    name="imgrabber",
    version="0.0.1",
    author="Nikolay Sedelnikov",
    author_email="n.sedelnikov@gmail.com",
    packages=find_packages(),
    install_requires=[
        'gevent',
        'six',
    ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest',
        'pytest-cov',
    ],
    include_package_data=True,
    zip_safe=True,
)
