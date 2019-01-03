from flask import Flask
from flask import request
import json
import base64
import os, time
import threading
import time


indir="/home/ubuntu/filestore/IN"
outdir="/home/ubuntu/filestore/OUT"

path_to_watch = indir
translated={}

app = Flask(__name__)

fIndex=0

@app.route('/api/atranslatefile', methods = ['POST'])
def atranslatefile():
    global fIndex
    fIndex = fIndex + 1
    content = request.get_json()

    fileType = content['fileType']
    source = content['source']
    token = content['token']
    target = content['target']
    encodedcontents=content['file']

    print("request from",token, "(", source,target,fileType,")", "received", "Requestid:", fIndex)
    decodedcontents=base64.b64decode(encodedcontents)
    output_file = open(outdir+"/"+str(fIndex) + "_"+ token +  "_" + source + "_" + target +'.' + fileType , 'wb')
    output_file.write(decodedcontents)
    output_file.close()
    result={
        "success": "true",
        "error": "null",
        "data": {
            "guid": fIndex
        }
    }
    return json.dumps(result)



@app.route('/api/aretrievefiletranslation', methods = ['POST'])
def aretrievefiletranslation():
    global translated
    content = request.get_json()

    guid = content['guid']
    token = content['token']
    print("Retrieve request for:", guid)
    if guid in translated:
        print("Retrieve request for:", guid, "found")
        result={
            "success": "true",
            "error": "null",
            "data": {
                "guid": guid,
                "fileType": "txt",
                "file": translated[guid].decode('utf-8')
                }
            }
        del translated[guid]
    else:
        print("Retrieve request for:", guid, "NOT found")
        result ={
            "success": "false",
            "error": {
                "statusCode": 400,
                "code": 16,
                "message": "Missing <guid>"
                },
            "data": "null"
            }

    return json.dumps(result)




def watcher():
    global translated
    before={}
    for root, subdirs, files in os.walk(path_to_watch):
        for file in os.listdir(root):
            filePath = os.path.join(root, file)
            if os.path.isdir(filePath):
                pass
            else:
                before[filePath]=None

    #before = dict([(f, None) for f in os.listdir(path_to_watch)])
    while 1:
        time.sleep(1)
        after={}
        for root, subdirs, files in os.walk(path_to_watch):
            for file in os.listdir(root):
                filePath = os.path.join(root, file)
                if os.path.isdir(filePath):
                    pass
                else:
                    after[filePath]=None
        #after = dict([(f, None) for f in os.listdir(path_to_watch)])


        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]
        if added:
            print("Added: ", ", ".join(added))

        if removed:
            print("Removed: ", ", ".join(removed))
        before = after

        for f in added:
            base = os.path.basename(f)
            (name, ext) = os.path.splitext(base)
            print ("added", base, name, ext)
            if ext==".txt":
                index = base.split("_")[0]
                print("translated file index",index,"found:", base)
                tt=""
                with open(f,'r') as t:
                    tt=t.readlines()
                tt='\n'.join(tt)
                print("file:", tt)
                tu=tt.encode('utf-8')
                encoded = base64.b64encode(tu)
                print("Encoded:", encoded)
                translated[index]=encoded



a = threading.Thread(target=watcher, name='Thread-a', daemon=True)
a.start()
app.run(host='0.0.0.0', port= 8090)