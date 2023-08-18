#!/usr/bin/python3

import logging
logger = logging.getLogger('snarf_logger')

from .classes.snarf import Snarf
from .util.args import args as ARGS
from .util.config import get_config, apply_args

def main(args={}, config=None):
    try:
        if not config: config = get_config()
        if args: apply_args(args)
        snarf_logger.log("Running - {}".format(ARGS.action))
        snarf = Snarf(config)
        getattr(snarf, ARGS.action)()
    except Exception as e:
        snarf_logger.error(e)
        snarf_logger.info("shnarf??")
    finally:
        snarf_logger.info("shnarrf!")
        exit_handler()

if __name__ == "__main__":
    main()