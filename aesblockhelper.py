import sys
inpfile = sys.argv[1]
inp = open(inpfile,"r").read()
if inp[-1] == "\n":
  inp = inp[:-1]

inpList = inp.split(" ")
newList = [inpList[0]+"  ",inpList[4]+"  ",inpList[8]+"  ",inpList[12]+"  ",
          inpList[1]+"  ",inpList[5]+"  ",inpList[9]+"  ",inpList[13]+"  ",
          inpList[2]+"  ",inpList[6]+"  ",inpList[10]+"  ",inpList[14]+"  ",
          inpList[3]+"  ",inpList[7]+"  ",inpList[11]+"  ",inpList[15]+"  "]

endString = ''.join(newList)
print(endString)
