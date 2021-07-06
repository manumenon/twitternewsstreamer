import json
import os
import sys

CONFIGURATION_FILE = os.path.join(os.getcwd(), "conf{0}config.json".format(os.sep))
sys.stdout.write("Reading Config from  {} \n".format(CONFIGURATION_FILE))
with open(CONFIGURATION_FILE,"r") as f:
    config = json.loads(f.read())
LOG_HANDLER_WHEN = config.get("log_handler_when", "M")
LOG_HANDLER_INTERVAL = int(config.get("log_handler_interval", 5))
LOG_HANDLER_BACKUP_COUNT = int(config.get("log_handler_backup_count", 10))
LOG_LEVEL = config.get("log_level", "INFO").upper()
LOG_HANDLER_NAME = config.get("log_handler_name", "ilens")
BASE_LOG_PATH = config.get('base_log_path',
                           os.path.join(os.getcwd(), "logs".format()))

