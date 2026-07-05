import yaml
from typing import Any, Dict


def load_config() -> Dict[str, Any]:
    """
    Load configuration from YAML file.

    Returns:
        Dictionary with configuration values.
    """
    with open("config/config.yaml", "r") as file:
        return yaml.safe_load(file)


CONFIG = load_config()
