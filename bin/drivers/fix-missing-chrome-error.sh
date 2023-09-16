#!/bin/bash
# fixes issue of: '/usr/bin/google-chrome: line 49: /usr/bin/chrome: No such file or directory'
sudo ln -f -s /usr/bin/google-chrome-stable /usr/bin/google-chrome
sudo chmod +x /usr/bin/google-chrome