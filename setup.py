import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OnlySnarf",
    version="4.4.4",
    author="Skeetzo",
    author_email="WebmasterSkeetzo@gmail.com",
    url = 'https://github.com/skeetzo/onlysnarf',
    keywords = ['OnlyFans', 'OnlySnarf', 'selenium', 'snarf'],
    description="OnlyFans Content Distribution Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # packages=setuptools.find_packages(),
    packages=["OnlySnarf", "OnlySnarf/classes","OnlySnarf/conf","OnlySnarf/elements","OnlySnarf/lib","OnlySnarf/util"],
    include_package_data=True,
    install_requires=[
        'chromedriver_autoinstaller',
        'ffmpeg',
        'pillow',
        'pyinquirer',
        'wget',
        'selenium==4.5.0',
        'webdriver_manager'
        ],
    extras_require={
        'dev': [
            'pytest'
        ]
    },
    entry_points={
        'console_scripts' : [
            # 'snarf = OnlySnarf.menu:main',
            'onlysnarf = OnlySnarf.snarf:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Topic :: System :: Emulators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        "Operating System :: OS Independent"
    ]
)