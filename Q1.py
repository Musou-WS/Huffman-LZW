import math;
import struct;

# fname = input(">>>");
import tkinter.filedialog
fname = tkinter.filedialog.askopenfilename()
count = {};
file = open(fname, "rb");
file2 = open("test.Huffman", "wb");
file3 = open("test.LZW", "wb");
s = file.read()
slength = len(s);
samplenum = int((slength-44)/2);
file2.write(s[0:44]);
file3.write(s[0:44]);

class node:
	def __init__(self):
		self.name = None;
		self.left = None;
		self.right = None;
		self.code = "";
		self.count = None;
	def __init__(self, name):
		self.name = name;
		self.left = None;
		self.right = None;
		self.code = "";
		self.count = None;
	def __init__(self, name, count):
		self.name = name;
		self.left = None;
		self.right = None;
		self.code = "";
		self.count = count

def setCode(node, nodes, names, codeDic):
	if (node.left != None):
		if (node.left.name in names):
			nodes.insert(1, node.left);
		node.left.code = node.code + "0";
		codeDic[node.left.name] = node.left.code;
		setCode(node.left, nodes, names, codeDic);
	if (node.right != None):
		if (node.right.name in names):
			nodes.insert(1, node.right);
		node.right.code = node.code + "1";
		codeDic[node.right.name] = node.right.code;
		setCode(node.right, nodes, names, codeDic);

def nodesHuffman(nodes, names):
	num = 0;
	for i in range(len(nodes)-1, -1, -1):
		if (nodes[i].count == 0):
			nodes.pop(i);
	while len(nodes) >1:
		if(nodes[1].count >= nodes[0].count):
			nodemin1 = 0;
			nodemin2 = 1;
		else:
			nodemin1 = 1;
			nodemin2 = 0;

		for i in range(2, len(nodes)):
			if(nodes[i].count < nodes[nodemin2].count):
				if(nodes[i].count < nodes[nodemin1].count):
					nodemin2 = nodemin1;
					nodemin1 = i;
				else:
					nodemin2 = i;
		
		countNew = nodes[nodemin2].count + nodes[nodemin1].count;
		nameNew = "P"+str(num);
		num += 1;
		nodeNew = node(nameNew, countNew);
		nodeNew.left = nodes[nodemin1];
		nodeNew.right = nodes[nodemin2];
		if (nodemin1 < nodemin2):
			nodes.pop(nodemin2);
			nodes.pop(nodemin1);
		else:
			nodes.pop(nodemin1);
			nodes.pop(nodemin2);
		nodes.insert(0, nodeNew);
	codeDic = {};
	setCode(nodes[0], nodes, names, codeDic);
	return [nodes[0], codeDic];

# Huffman count
for i in range(44, slength, 2):
	temp = struct.unpack('h', s[i:i+2])[0];
	if (count.has_key(temp)):
		count[temp] += 1;
	else:
		count[temp] = 1;

# form node array
keys = count.keys();
keylen = len(keys);
nodes = [0 for i in range(keylen)];
for i in range(keylen):
	nodes[i] = node(keys[i], count[keys[i]]);

[nodeOrigin, codeDic] = nodesHuffman(nodes, keys);
tempNow = '';
for i in range(44, slength, 2):
	temp = struct.unpack('h', s[i:i+2])[0];
	tempNow += codeDic[temp];

# add '0' to string to make sure string is 8 times
for i in range(len(tempNow)%8):
	tempNow += '0';

for i in range(0, len(tempNow), 8):
	tempInt = int(tempNow[i:i+8],2);
	temp = struct.pack('B', tempInt);
	file2.write(temp);



# wrinteInteger to file
def writeInt(num, fileWrite):
	binary = bin(num); # '0b......'
	binary = binary[2:];
	bLength = len(binary);
	add0 = bLength % 8;
	for i in range(add0):
		binary = '0' + binary;
	for i in range(0, (bLength+add0) / 8, 8):
		intNow = int(binary[i:i+8], 2);
		temp = struct.pack('B', intNow);
		fileWrite.write(temp);
#LZW
# initial LZW dic
LZWdic = {};
LZWstring = [];

# -32768 to 32767
#-128 to 127
LZWdic = { struct.pack('h', i): i+32768 for i in range(-32768, 32768)};
indexBefore = 44; # start from 44
indexAfter = 46;

codeNow = 32768*2;
while indexAfter < slength:
	sampleNow = s[indexBefore: indexAfter];
	if not(LZWdic.has_key(sampleNow)):
		LZWstring.append(LZWdic[s[indexBefore: indexAfter-2]]);
		LZWdic[s[indexBefore: indexAfter]] = codeNow;
		codeNow += 1;
		indexBefore = indexAfter-2;
	else:
		indexAfter += 2;
		if indexAfter > slength:
			LZWstring.append(LZWdic[s[indexBefore: slength]]);

writeInt(LZWstring[0], file3);
mark = struct.pack('c', ',');
for i in range(1, len(LZWstring)):
	file3.write(mark);
	writeInt(LZWstring[i], file3);

file4 = open("test", "rb");
file5 = open("test2", "rb");
s1=file4.read();
s2=file5.read();
# print(len(s));
# print(len(s1));
# print(len(s2));

print("Huffman Compression Ratio: "),
print(float(len(s1))/slength);
print("LZW Compression Ratio: "),
print(float(len(s2))/slength);







