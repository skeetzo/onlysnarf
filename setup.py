import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OnlySnarf",
    version="1.1.9",
    author="Skeetzo",
    author_email="WebmasterSkeetzo@gmail.com",
    url = 'https://github.com/skeetzo/onlysnarf',
    download_url = 'https://github.com/skeetzo/onlysnarf/archive/v1.1.9.tar.gz',
    keywords = ['OnlyFans', 'Content', 'OnlySnarf'],
    description="OnlyFans Content Distribution Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'selenium',
        'pydrive',
        'pathlib',
        'chromedriver-binary==74.0.3729.6.0',
        'moviepy',
        'apiclient',
        'google-api-python-client',
        'httplib2',
        'python-crontab'
        ],
    entry_points={
        'console_scripts' : [
            'onlysnarf = OnlySnarf.menu:main_other',
            'onlysnarf-config = OnlySnarf.config:main'
        ]
    },
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: System :: Shells',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.4',
    "Operating System :: OS Independent",
  ]
)