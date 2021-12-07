import sys
mode = sys.argv[1]
keyfile = sys.argv[2]
inpfile = sys.argv[3]
key = open(keyfile,"rb").read()
inp = open(inpfile,"rb").read()
debug = False

if(debug):
  print("mode:"+mode)
  print("key: "+key)
  print("inp: "+inp)
