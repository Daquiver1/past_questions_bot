from .scapper import Scapper
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

STUDENTID = os.environ.get('STUDENTID')
PASSW = os.environ.get('PASSW')

scapper = Scapper(STUDENTID, PASSW)    

