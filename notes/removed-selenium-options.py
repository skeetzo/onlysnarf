
# Chrome
options.add_argument("--disable-setuid-sandbox")
options.add_argument("--disable-dev-shm-usage") # overcome limited resource problems
options.add_argument("--disable-gpu") # applicable to windows os only
options.add_argument('--disable-smooth-scrolling')
options.add_argument("--start-maximized")
options.add_argument("--window-size=1920,1080")
options.add_argument("--user-data-dir=/tmp/")
options.add_argument('--disable-login-animations')
options.add_argument('--disable-modal-animations')
options.add_argument('--disable-sync')
options.add_argument('--disable-background-networking')
options.add_argument('--disable-web-resources')
options.add_argument('--disable-logging')
options.add_argument('--no-experiments')
options.add_argument('--incognito')
options.add_argument('--user-agent=MozillaYerMomFox')
options.add_argument("--acceptInsecureCerts")
options.add_experimental_option("prefs", {
    "download.default_directory": str(DOWNLOAD_PATH),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

