import yaml
import os

DEFAULT_CONFIG_FILE = "./config/config.yml"


def load_config(config_file: str = DEFAULT_CONFIG_FILE) -> dict:
    """
    Loads the configuration from the specified file.

    Args:
        config_file (str, optional): The path to the configuration file. Defaults to DEFAULT_CONFIG_FILE.

    Returns:
        dict: The configuration dictionary.
    """
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
        return config
