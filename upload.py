''' cmd line utility to upload file to OnlyFans from filesystem '''
import sys
import argparse

from OnlySnarf import driver as driver
from OnlySnarf.settings import SETTINGS as settings

def parse_args(argv):
    ''' parse arguments from argv using argparse '''

    parser = argparse.ArgumentParser()

    # filename
    parser.add_argument('-f')

    # descriptive text
    parser.add_argument('-t')

    # performers
    parser.add_argument('-p', action='append')

    # keywords
    parser.add_argument('-k', action='append')

    args = parser.parse_args(argv[1:])
    return args

def main():
    ''' main entry point '''

    args = parse_args(sys.argv)

    settings.initialize()
    settings.ACTION = "upload"
    settings.TYPE = 'video'

    driver.upload_to_OnlyFans(
        path=args.f,
        text=args.t,
        keywords=args.k,
        performers=args.p,
        expires=False,
        schedule=False,
        poll=False)

if __name__ == '__main__':
    main()
