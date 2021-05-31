import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def readQss():
    with open(os.path.join(BASE_DIR ,'LCY.qss'), encoding='utf-8') as f:
        return f.read()