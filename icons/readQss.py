import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
qss = None
with open(os.path.join(BASE_DIR ,'resource.qss'), encoding='utf-8') as f:
    qss = f.read()
