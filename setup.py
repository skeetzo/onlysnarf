import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OnlySnarf",
    version="4.3.10",
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
        # 'geckodriver-autoinstaller',    
        'chromedriver-binary',
        'httplib2',
        'ffmpeg',
        'pathlib', 
        'pillow',
        'pysftp',
        'pyinquirer',
        'wget',
        'selenium'
        ],
    entry_points={
        'console_scripts' : [
            'snarf = OnlySnarf.menu:main',
            'onlysnarf = OnlySnarf.snarf:main'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: System :: Emulators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        "Operating System :: OS Independent"
    ]
)