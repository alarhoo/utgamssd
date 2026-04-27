# Code to parse XML data 
# Checks for the negative values in <Value> tag which 
# would be in incorrect format like <28.11-> and corrects it 
# correct format. <-28.11>.

import xml.etree.ElementTree as ET
import os
path = 'C:/Users/rajath.gowda/Desktop/Python'
for filename in os.listdir(path):
	if not filename.endswith('.xml'): continue
	fullname = os.path.join(path, filename)
	tree = ET.parse(fullname)
	root = tree.getroot()
	lastEntry = sum([1 for entry in root.getiterator('Value')])
	print('lastEntry', lastEntry)
	i = 0
	for val in root.iter('Value'):
		i = i + 1
		if val.text.endswith('-'):
			print(val.text)
			val.text = '-' +  val.text[:-1]
			print(val.text)
			print('i', i)
			if i == lastEntry:
				tree.write(filename)
				print('Values have been updated to ' + filename)