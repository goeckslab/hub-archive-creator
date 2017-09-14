import os
import sys
import json
import logging
import logging.config

#from util.Filters import TraceBackFormatter

def setup_logging(
    config_path='logging.json',
    default_level=logging.INFO,
    debug="False",
    extra_files_path=None
    ):
    """Setup logging configuration
       reference: https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
    """
    config_path = config_path
    if debug.lower() == "true":
        default_level=logging.DEBUG
    if os.path.exists(config_path):
        with open(config_path, 'rt') as f:
            config = json.load(f)
        config["root"]["level"] = default_level
        if extra_files_path:
            config["base_directory"] = extra_files_path
            for i in config["handlers"]:
                if "filename" in config["handlers"][i]:
                    config["handlers"][i]["filename"] = config["base_directory"] + config["handlers"][i]["filename"]
            logging.config.dictConfig(config)
        else:
            logging.warn("Extra files path is not set. The log files will exist at current working directory instead of final output folder")
    else:
        logging.basicConfig(level=default_level)
        logging.warn("Cannot find logging configuration file!\n")

