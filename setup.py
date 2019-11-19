import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OnlySnarf",
    version="2.14.0",
    author="Skeetzo",
    author_email="WebmasterSkeetzo@gmail.com",
    url = 'https://github.com/skeetzo/onlysnarf',
    keywords = ['OnlyFans', 'Content', 'OnlySnarf'],
    description="OnlyFans Content Distribution Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    # package_data={'': ['/path/to/google']},
    # include_package_data=True,
    install_requires=[
        'selenium',
        'pydrive',
        'pathlib', 
        'chromedriver-binary==77.0.3865.40',
        'moviepy',
        'google-api-python-client',
        'httplib2',
        'python-crontab'
        ],
    entry_points={
        'console_scripts' : [
            'onlysnarf = OnlySnarf.menu:main_other',
            'onlysnarfpy = OnlySnarf.onlysnarf:main',
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

## TEST
# 'imageio<3.0,>=2.5'
# imageio req, maybe not needed?