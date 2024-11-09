import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
TEMPLATES_DIR = os.path.join(dir_path, "frontend")
CLF_ADDRESS = 'http://127.0.0.1:1234/v1/chat/completions'
