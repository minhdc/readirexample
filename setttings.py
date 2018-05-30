import os

SRC_DIR = "E:\\sample-shit\\input"
DST_DIR = "E:\\sample-shit\\output"

INPUT_DIR_NAME = os.path.basename(SRC_DIR)
OUTPUT_DIR_NAME = os.path.basename(DST_DIR)

folder_watch_list = [""]

CONFIG_FILE_LOC = "D:\\email-classification-as-service\\"
CONFIG_FILE_SUFFIX = ["*.txt"]
CONFIG_FILE_CHANGED = False

STATUS = False

EMAIL_COUNT_FOR_CURRENT_SESSION = 0
