import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OnlySnarf",
    version="2.17.8",
    author="Skeetzo",
    author_email="WebmasterSkeetzo@gmail.com",
    url = 'https://github.com/skeetzo/onlysnarf',
    keywords = ['OnlyFans', 'OnlySnarf'],
    description="OnlyFans Content Distribution Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'selenium',
        'pydrive',
        'pathlib', 
        'chromedriver-binary',
        'geckodriver-autoinstaller',
        'moviepy',
        'google-api-python-client',
        'httplib2',
        'python-crontab',
        'pyinquirer',
        'ffmpeg'
        ],
    entry_points={
        'console_scripts' : [
            'onlysnarf = OnlySnarf.bin.menu:main',
            'onlysnarfpy = OnlySnarf.src.snarf:main',
            'onlysnarf-config = OnlySnarf.bin.config:main'
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