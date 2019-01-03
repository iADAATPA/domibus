from flask import Flask
from flask import request
import json
import base64
import os, time
import threading
import time

t="Hola amiga, ¿Que tal?"
tu=t.encode('utf-8')
encoded = base64.b64encode(tu)
#encode
print(encoded)



