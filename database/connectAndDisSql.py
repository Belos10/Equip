import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(BASE_DIR ,'NuclearManageSystem.db'))
cur = conn.cursor()

