import os
import datetime

#Thư mục nguồn
SRC_DIR = "D:\\sample-shit\\input"

#Thư mục đích
DST_DIR = "D:\\sample-shit\\output"

#Nơi lưu danh sách đối tượng
LIST_OF_TARGET = "D:\\sample-shit\\danh_sach_doi_tuong"

#Nơi lưu file Excel thống kê
EXCEL_FILE_LOC = "D:\\sample-shit\\bao_cao\\"


#Nơi lưu file csv trung gian
CSV_FILE_LOC = "D:\\sample-shit\\csv\\"
##################
##################
INPUT_DIR_NAME = os.path.basename(SRC_DIR)
OUTPUT_DIR_NAME = os.path.basename(DST_DIR)

CURRENT_DAY = str(datetime.datetime.now().day) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().year) 
CSV_EXTENSION = '.csv'
EXCEL_EXTENSION = '.xlsx'






folder_watch_list = [""]

CONFIG_FILE_LOC = "D:\\email-classification-as-service\\"
CONFIG_FILE_SUFFIX = ["*.txt"]
CONFIG_FILE_CHANGED = False

STATUS = False

EMAIL_COUNT_FOR_CURRENT_SESSION = 0
