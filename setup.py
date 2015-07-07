import os
from setuptools import setup


try:
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'README.md')) as f:
        README = f.read()
except IOError:
    # work around packing bug when using tox
    README = ''


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
    install_requires=['python-resize-image', 'Django'],
)
