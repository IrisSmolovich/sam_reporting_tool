
import yaml
from pathlib import Path
import os
from dotenv import load_dotenv


def load_domains_from_file(path: str = None):
    """
    helper function for domains
    :return: domains list
    """
    if path:
        file_path = Path(path)
    else:
        file_path = Path(__file__).resolve().parent.parent.parent / "domains.yaml"
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
    return data["domains"]


def get_api_token():
    """
    helper function for api token
    :return: api_token
    """
    load_dotenv()
    api_token = os.getenv('API_TOKEN')
    return api_token
