import os, time
import threading
import time
import urllib.request
import json

indir="/home/ubuntu/filestore/IN"
outdir="/home/ubuntu/filestore/OUT"

path_to_watch = indir

def watcher():
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
                print("to translate", base)
                translated=[]
                with open(f, "r") as myfile:
                    for linea in myfile:
                        print("linea:", linea)
                        body = {
                                "src":"es",
                                "tgt":"en",
                                "apikey":"000000",
                                "mode":"2",
                                "text":[linea]
                                }

                        myurl = "http://prod.pangeamt.com:8080/NexRelay/v1/translate"
                        req = urllib.request.Request(myurl)
                        req.add_header('Content-Type', 'application/json; charset=utf-8')
                        jsondata = json.dumps(body)
                        jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
                        req.add_header('Content-Length', len(jsondataasbytes))
                        print(jsondataasbytes)
                        response = urllib.request.urlopen(req, jsondataasbytes)
                        # Convert bytes to string type and string type to dict
                        string = response.read().decode('utf-8')
                        json_obj = json.loads(string)

                        translated.append(json_obj[0][0]["tgt"])

                with open(outdir + "/" + base, 'w') as f:
                    for item in translated:
                        print("Translated:",item)
                        f.write("%s\n" % item)

watcher()


