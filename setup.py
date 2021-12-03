import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OnlySnarf",
    version="4.0.0",
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
        'selenium==3.141.0',
        'pydrive',
        'pathlib', 
        'chromedriver-binary',
        # 'geckodriver-autoinstaller',    
        'google-api-python-client',
        'httplib2',
        'python-crontab',
        'pyinquirer',
        'ffmpeg',
        'wget',
        'pysftp',
        'pillow',
        'flask'
        ],
    entry_points={
        'console_scripts' : [
            'onlysnarf = src.OnlySnarf.menu:main',
            'onlysnarfpy = src.OnlySnarf.snarf:main',
            'onlysnarf-config = src.OnlySnarf.config:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: System :: Shells',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        "Operating System :: OS Independent",
  ]
)