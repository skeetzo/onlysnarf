import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OnlySnarf",
    version="4.1.5",
    author="Skeetzo",
    author_email="WebmasterSkeetzo@gmail.com",
    url = 'https://github.com/skeetzo/onlysnarf',
    keywords = ['OnlyFans', 'OnlySnarf'],
    description="OnlyFans Content Distribution Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # packages=setuptools.find_packages(),
    packages=["OnlySnarf", "OnlySnarf/classes","OnlySnarf/conf","OnlySnarf/elements","OnlySnarf/lib","OnlySnarf/util"],
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
        'pillow'
        ],
    entry_points={
        'console_scripts' : [
            'onlysnarf = OnlySnarf.menu:main',
            'snarf = OnlySnarf.snarf:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: System :: Shells',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        "Operating System :: OS Independent"
    ]
)