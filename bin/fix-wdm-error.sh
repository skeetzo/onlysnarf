#!/bin/bash
# fixes error: Exec format error: '/home/ubuntu/.wdm/drivers/chromedriver/linux64/129.0.6668/chromedriver-linux64/THIRD_PARTY_NOTICES.chromedriver'
# https://stackoverflow.com/questions/78806812/third-party-notices-chromedriver-exec-format-error-undetected-chromedriver

rm -rf /home/user/.wdm
pip uninstall webdriver-manager
pip install webdriver-manager