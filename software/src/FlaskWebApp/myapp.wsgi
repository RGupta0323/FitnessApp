#!/usr/bin/python
import sysi
mport logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/user/OurApp")
from OurApp.app import app as application