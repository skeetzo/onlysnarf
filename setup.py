import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OnlySnarf",
    version="4.7.0",
    author="Skeetzo",
    author_email="WebmasterSkeetzo@gmail.com",
    url = 'https://github.com/skeetzo/onlysnarf',
    keywords = ['OnlyFans', 'OnlySnarf', 'selenium', 'snarf'],
    description="OnlyFans Content Distribution Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # packages=setuptools.find_packages(),
    packages=["OnlySnarf","OnlySnarf/classes","OnlySnarf/lib/webdriver","OnlySnarf/conf","OnlySnarf/lib","OnlySnarf/util"],
    include_package_data=True,
    install_requires=[
        'dropbox',
        'ffmpeg',
        'inquirer',
        'marshmallow',
        'wget',
        'selenium==4.8.3',
        'webdriver_manager==4.0.0',
        'validators',
        'flask'
    ],
    extras_require={
        'dev': [
            'pytest',
            'flask-unittest'
        ]
    },
    entry_points={
        'console_scripts' : [
            'snarf = OnlySnarf.snarf:main'
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