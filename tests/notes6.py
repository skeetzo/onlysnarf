PROXY = "hub_subdomain.gridlastic.com:8001"; # hosted Squid proxy on your selenium grid hub
#PROXY = "your_gridlastic_connect_subdomain.gridlastic.com:9999"; # An example Gridlastic Connect endpoint

desired_capabilities['proxy'] = {
    "httpProxy":PROXY,
    "ftpProxy":PROXY,
    "sslProxy":PROXY,
    "noProxy":None,
    "proxyType":"MANUAL",
    "class":"org.openqa.selenium.Proxy",
    "autodetect":False
}