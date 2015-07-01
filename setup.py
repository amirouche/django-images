import os
from codecs import open
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(here, 'README.md')) as f:
    README = f.read()


setup(
    name='django-images',
    version='0.1',
    description='Upload, resize and save images in Django',
    long_description=README,
    url='https://github.com/VingtCinq/django-images',
    author='Charles TISSIER',
    author_email='charles@vingtcinq.io',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='image resize bootstrap django',
    packages=['django_images'],
    install_requires=['python-image-resize', 'Django'],
    test_suite='tests',
)
