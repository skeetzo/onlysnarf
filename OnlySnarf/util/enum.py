from enum import Enum

class Source(Enum):
     REMOTE = "remote"
     LOCAL = "local"
     IPFS = "ipfs"
     GOOGLE = "google"
     ONLYFANS = "onlyfans"
     ONLYSNARF = "onlyfans"


class Types(Enum):
	POST = "post"
	MESSAGE = "message"
     AUTO = "auto"
     FIREFOX = "firefox"
     GOOGLE = "google"
     RECONNECT = "reconnect"
     REMOTE = "remote"
