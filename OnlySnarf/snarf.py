#!/usr/bin/python3

import logging
logger = logging.getLogger('snarf_logger')

from .classes.snarf import Snarf

def main(config=None):
    from .util.args import args
    from .util.config import get_config
    try:
        if not config: config = get_config(args)
        snarf_logger.log("Running - {}".format(args.action))
        snarf = Snarf(config)
        getattr(snarf, args.action)()
    except Exception as e:
        snarf_logger.error(e)
        snarf_logger.info("shnarf??")
    finally:
        snarf_logger.info("shnarrf!")
        exit_handler()

if __name__ == "__main__":
    main()