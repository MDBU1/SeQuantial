import argparse
import sys
from datetime import datetime
from typing import Any
import pandas as pd
import logging


logger = logging.getLogger(__name__)

def func_load_yaml_config() -> dict[str, Any]:
    """Load the yaml config file to use as argparse defaults"""
    try:
        with open("config/config.yml") as yaml_file:
            return yaml.safe_load(yaml_file)
    except FileNotFoundError:
        logger.error("config.yml not found in config directory")
        exit(1)
        
        
def func_load_csv_config() -> dict[str, Any]:
    """Load the yaml config file to use as argparse defaults"""
    try:
        df_config = pd.read_csv("config/config.csv")
        return df_config
    except FileNotFoundError:
        logger.error("config.csv not found in config directory")
        exit(1)

# config = func_load_csv_config()

def func_return_commands():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--logging_level",
        "-logging",
        dest="logging_level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    group_run_type = parser.add_mutually_exclusive_group(
        required=True,
    )
    group_run_type.add_argument(
        "--terminal",
        "-terminal",
        dest="run_type",
        action="store_true"
    )
    group_run_type.add_argument(
        "--dash",
        "-dash",
        dest="run_type",
        action="store_false"
    )
    parser.add_argument(
        "--number_of_synthetic",
        "-no",
        dest="int_no_synthetic",
        type=int,
        default=10,
        required=False,
        help="enter the number of synthetic sequences to be produced, default is 1"
    )
    parser.add_argument(
        "--boolean_weightings",
        "-weightings",
        dest="boolean_weightings",
        default=False,
        # required="-dash" not in sys.argv,
        help="set to True if attaching weightings file"
    )
    parser.add_argument(
        "--type_weightings"
        "-type_weightings",
        dest="type_weightings",
        default=None,
        choices=["bases", "codons"],
        required=False,
    )
    parser.add_argument(
        "--path_weightings_csv",
        "-weights",
        dest="path_weightings_csv"
    )
    parser.add_argument(
        "--alt_base_inclusion",
        "-add_bases",
        dest="alt_base_inclusion",
        type=str,
        choices=[""],
        default=False,
        required=False,
    )
    parser.add_argument(
        "--include_nonsense",
        "-nonsense"
    )
    args = parser.parse_args()

    return args
