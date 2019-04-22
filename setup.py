import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OnlySnarf",
    version="1.0.0",
    author="Skeetzo",
    author_email="WebmasterSkeetzo@gmail.com",
    url = 'https://github.com/skeetzo/onlysnarf',   # Provide either the link to your github or to your website
    download_url = 'https://github.com/skeetzo/onlysnarf/archive/v_01.tar.gz',    # I explain this later on
    keywords = ['OnlyFans', 'Content', 'OnlySnarf'],   # Keywords that define your package best
    description="OnlyFans Content Distribution Tool",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/skeetzo/onlysnarf",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'selenium',
        'pydrive',
        'pathlib',
        'chromedriver-binary',
        'moviepy',
        'apiclient',
        'httplib2',
        # 'oauth2client'
        ],
    entry_points={
        'console_scripts' : [
            'onlysnarf = OnlySnarf.__main__:main',
            'onlysnarf-menu = OnlySnarf.menu:main_other',
            'onlysnarf-config = OnlySnarf.config:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)