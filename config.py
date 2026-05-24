import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "jlpt.db")
PORT = 5003
SECRET_KEY = "dev-jlpt-estudos-trocar-em-prod"
