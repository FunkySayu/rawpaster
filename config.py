import os
import re


THIS_PATH = os.path.dirname(os.path.realpath(__file__))
DEFAULT_INDEX_FILE = "index.html"
FILE_ID_LENGTH = 5

index_page = os.path.join(THIS_PATH, DEFAULT_INDEX_FILE)
data_folder = "data/"
master_key = "toto"
authorized_keys_file = os.path.join(THIS_PATH, "authorized_keys.txt")

valid_file_id = re.compile("^[a-zA-Z0-9]{%s}$" % FILE_ID_LENGTH)
