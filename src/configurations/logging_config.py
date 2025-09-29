import logging.config
from functools import lru_cache
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

def configure_logging():
	config_file = Path(f"{Path.home()}/PycharmProjects/exp/logger_config.yml")
	with open(config_file) as file:
		config = yaml.safe_load(file)
	logging.config.dictConfig(config=config)


@lru_cache
def get_exp_logger():
	return logger

if __name__ == '__main__':
	configure_logging()