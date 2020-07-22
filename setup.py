import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OnlySnarf",
    version="2.17.19",
    author="Skeetzo",
    author_email="WebmasterSkeetzo@gmail.com",
    url = 'https://github.com/skeetzo/onlysnarf',
    keywords = ['OnlyFans', 'OnlySnarf'],
    description="OnlyFans Content Distribution Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'selenium',
        'pydrive',
        'pathlib', 
        'chromedriver-binary',
        'geckodriver-autoinstaller',    
        'google-api-python-client',
        'httplib2',
        'python-crontab',
        'pyinquirer',
        'ffmpeg',
        'wget',
        'pysftp',
        'moviepy'
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