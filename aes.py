import sys
mode = sys.argv[1]
keyfile = sys.argv[2]
inpfile = sys.argv[3]
key = open(keyfile,"r").read()[:-1]
inp = open(inpfile,"r").read()[:-1]
debug = True

if(len(key) != 16):
  print("the key length must be 16 characters")

if(len(inp) != 16):
  print("the input length must be 16 characters")

if(debug):
  print("mode:"+mode)
  print("key: "+key)
  print("inp: "+inp)

SBox = [0x63 ,0x7c ,0x77 ,0x7b ,0xf2 ,0x6b ,0x6f ,0xc5 ,0x30 ,0x01 ,0x67 ,0x2b ,0xfe ,0xd7 ,0xab ,0x76
 ,0xca ,0x82 ,0xc9 ,0x7d ,0xfa ,0x59 ,0x47 ,0xf0 ,0xad ,0xd4 ,0xa2 ,0xaf ,0x9c ,0xa4 ,0x72 ,0xc0
 ,0xb7 ,0xfd ,0x93 ,0x26 ,0x36 ,0x3f ,0xf7 ,0xcc ,0x34 ,0xa5 ,0xe5 ,0xf1 ,0x71 ,0xd8 ,0x31 ,0x15
 ,0x04 ,0xc7 ,0x23 ,0xc3 ,0x18 ,0x96 ,0x05 ,0x9a ,0x07 ,0x12 ,0x80 ,0xe2 ,0xeb ,0x27 ,0xb2 ,0x75
 ,0x09 ,0x83 ,0x2c ,0x1a ,0x1b ,0x6e ,0x5a ,0xa0 ,0x52 ,0x3b ,0xd6 ,0xb3 ,0x29 ,0xe3 ,0x2f ,0x84
 ,0x53 ,0xd1 ,0x00 ,0xed ,0x20 ,0xfc ,0xb1 ,0x5b ,0x6a ,0xcb ,0xbe ,0x39 ,0x4a ,0x4c ,0x58 ,0xcf
 ,0xd0 ,0xef ,0xaa ,0xfb ,0x43 ,0x4d ,0x33 ,0x85 ,0x45 ,0xf9 ,0x02 ,0x7f ,0x50 ,0x3c ,0x9f ,0xa8
 ,0x51 ,0xa3 ,0x40 ,0x8f ,0x92 ,0x9d ,0x38 ,0xf5 ,0xbc ,0xb6 ,0xda ,0x21 ,0x10 ,0xff ,0xf3 ,0xd2
 ,0xcd ,0x0c ,0x13 ,0xec ,0x5f ,0x97 ,0x44 ,0x17 ,0xc4 ,0xa7 ,0x7e ,0x3d ,0x64 ,0x5d ,0x19 ,0x73
 ,0x60 ,0x81 ,0x4f ,0xdc ,0x22 ,0x2a ,0x90 ,0x88 ,0x46 ,0xee ,0xb8 ,0x14 ,0xde ,0x5e ,0x0b ,0xdb
 ,0xe0 ,0x32 ,0x3a ,0x0a ,0x49 ,0x06 ,0x24 ,0x5c ,0xc2 ,0xd3 ,0xac ,0x62 ,0x91 ,0x95 ,0xe4 ,0x79
 ,0xe7 ,0xc8 ,0x37 ,0x6d ,0x8d ,0xd5 ,0x4e ,0xa9 ,0x6c ,0x56 ,0xf4 ,0xea ,0x65 ,0x7a ,0xae ,0x08
 ,0xba ,0x78 ,0x25 ,0x2e ,0x1c ,0xa6 ,0xb4 ,0xc6 ,0xe8 ,0xdd ,0x74 ,0x1f ,0x4b ,0xbd ,0x8b ,0x8a
 ,0x70 ,0x3e ,0xb5 ,0x66 ,0x48 ,0x03 ,0xf6 ,0x0e ,0x61 ,0x35 ,0x57 ,0xb9 ,0x86 ,0xc1 ,0x1d ,0x9e
 ,0xe1 ,0xf8 ,0x98 ,0x11 ,0x69 ,0xd9 ,0x8e ,0x94 ,0x9b ,0x1e ,0x87 ,0xe9 ,0xce ,0x55 ,0x28 ,0xdf
 ,0x8c ,0xa1 ,0x89 ,0x0d ,0xbf ,0xe6 ,0x42 ,0x68 ,0x41 ,0x99 ,0x2d ,0x0f ,0xb0 ,0x54 ,0xbb ,0x16]

#method to print out in hex
def hexOut(list):
    out = ""
    for i in list:
        out += hex(i)[2:4] + ' '
    print(out)

#method to xor lists
def xor(key,inp):
    xoredList = []
    for i in range(0,len(key)):
      xoredList += [key[i] ^ inp[i]]
    return xoredList

#row offset method (2nd row shifted 1 space left, 3rd row 2 spaces left, 4th row 3 spaces left)
def shiftRow(list):
  final = []
  for i in range(0,16):
    final += [0]
  #create list with 16 items
  for i in range(0,16):
    final[i] = list[(i + 4*(i%4)) % 16]
    #add rotated values to list
  return final

#use lookup table
def byteSubstitution(list):
  newList = []
  for i in range(0,len(list)):
    newList.append(SBox[list[i]])
  return newList

#multiplication with small numbers
def simplify(k,num):
  if k == 0:
    return 0
  if k == 1:
    return num
  if k == 2:
    if 2*num < 256:
      return 2*num
    return (2*num) ^ 283
  if k == 3:
    return simplify(2,num) ^ num

#mix columns by multiplying matrix
def mixColumn(list):
  newList = []
  multiplier = [2,1,1,3,3,2,1,1,1,3,2,1,1,1,3,2]
  u = []
  v = []
  for i in range(0,4):
    u += [2 * (i // 2)]
    v += [i % 2]
  for i in range(0,16):
    a = i % 4
    b = i // 4
    newList += [simplify(multiplier[a],list[4*b]) ^ simplify(multiplier[a+4],list[4*b+1]) ^ simplify(multiplier[a+8],list[4*b+2]) ^ simplify(multiplier[a+12],list[4*b+3])]
  return newList

def rCon(j):
  if j == 1:
    return 1
  else:
    if 2*rCon(j-1) < 256:
      return 2*rCon(j-1)
    return (2*rCon(j-1))^283

def rotatevec(v):
  return [v[1],v[2],v[3],v[0]]

def iterateRoundKey(list,k):
  v0 = [list[0],list[1],list[2],list[3]]
  v1 = [list[4],list[5],list[6],list[7]]
  v2 = [list[8],list[9],list[10],list[11]]
  v3 = [list[12],list[13],list[14],list[15]]
  w3 = rotatevec(v3)
  v = byteSubstitution(w3)
  v[0] = v[0]^rCon(k)
  w4 = []
  w5 = []
  w6 = []
  w7 = []
  for i in range(0,4):
    w4.append(v0[i]^v[i])
  for i in range(0,4):
    w5.append(v1[i]^w4[i])
  for i in range(0,4):
    w6.append(v2[i]^w5[i])
  for i in range(0,4):
    w7.append(v3[i]^w6[i])
  return w4+w5+w6+w7



hexkey = []
#convert key to hex
for i in key:
  hexkey += [ord(i)]

hexinp = []
#convert inp to hex
for i in inp:
  hexinp += [ord(i)]



def roundKey(lst,k):
  newlst = []
  for i in lst:
    newlst += [i]
  for j in range(1,k+1):
    newlst = iterateRoundKey(newlst,j)
  return newlst
      



def fullIteration(state,key):
  state = byteSubstitution(state)
  state = shiftRow(state)
  state = mixColumn(state)
  state = xor(state,key)
  return state



def fullCipherText(hexinp,hexkey):
  state = xor(hexkey,hexinp)
  for i in range(1,10):
    newkey = roundKey(hexkey,i)
    state = fullIteration(state,newkey)
  newkey = roundKey(hexkey,10)
  state = xor((shiftRow(byteSubstitution(state))),newkey)
  return state


def inverseMixColumn(list):
  return mixColumn(mixColumn(mixColumn(list)))

def inverseShiftRow(list):
  return shiftRow(shiftRow(shiftRow(list)))

def inverseSubstituteByte(list):
  newList = []
  for i in range(0,len(list)):
    newList.append(SBox.index(list[i]))
  return newList


def reverseIteration(state,key):
  state = xor(state,key)
  state = inverseMixColumn(state)
  state = inverseShiftRow(state)
  state = inverseSubstituteByte(state)
  return state

hexOut(reverseIteration([9,102,139,120,162,209,154,101,240,252,230,196,123,59,48,137],roundKey(hexkey,9)))
hexOut([9,102,139,120,162,209,154,101,240,252,230,196,123,59,48,137])
  
  

hexOut(fullCipherText(hexinp,hexkey))


  

