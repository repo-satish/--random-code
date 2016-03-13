"""

	learn multi-threading here

"""

import os
import sys
import json
import pprint
import hashlib
import concurrent.futures 

BLOCK_SIZE = 5 * 1024

class FileWisdom():
	""" stores key:value pairs of hash:filePaths in a large(?) dict """

	fileDict = dict()		# static var
	ansDict = dict(zip(["unique", "redundant"], [list(), list()]))

	@classmethod			# no need to mk obj of class to call membr fn
	def makeEntry(self, filePath):
		""" using dict as data structure, stores filePath of files which are
		unique as string, if not unique then filePath(s) refering to that file
		are stored as a list of strings. Unique-ness of a file is determined
		by SHA1 of that file.
		"""
		h = calcSHA1(filePath)
		try:
			self.fileDict[h].append(filePath)
			print("dup")
		except KeyError:
			self.fileDict[h] = filePath
			print("new")
		except AttributeError:
			temp = self.fileDict[h]
			self.fileDict[h] = [temp]
			self.fileDict[h].append(filePath)
			print("cng")
		return

	@classmethod
	def report(self):
		""" traverses fileDict by key and reports only if associated value is
		of 'list' type
		"""
		for aKey in self.fileDict.keys():
			if type(self.fileDict[aKey]) is list:
				self.ansDict["redundant"].append({aKey:self.fileDict[aKey]})				# print("\n----> File with SHA1: `%s...%s` is stored in following locations:" % (aKey[:6], aKey[-3:]))				# print("\n".join(self.fileDict[aKey]))				# input("\t . . . press <Enter> key to continue.")
			else:
				self.ansDict["unique"].append({aKey:self.fileDict[aKey]})
		input("DONE")
		for _ in self.ansDict.keys():
			pprint.pprint(self.ansDict[_])
			json.dumps(self.ansDict[_], sort_keys=True, indent=4)
			input()
		return




def calcSHA1(filePath):
	hashVal = hashlib.sha1()
	with open(filePath, mode="rb") as fh:
		while True:
			x = fh.read(BLOCK_SIZE)
			if len(x) is 0:	break
			hashVal.update(x)
	return hashVal.hexdigest()

def process(fileList):
	# for aFile in fileList:
	# 	FileWisdom.makeEntry(aFile)
	with concurrent.futures.ThreadPoolExecutor(max_workers=4) as runMany:
		runMany.map(FileWisdom.makeEntry, fileList)
	return

def main(targetDir):
	targetDir = os.path.abspath(targetDir)
	for root, dirs, files in os.walk(targetDir, topdown=True, onerror=None, followlinks=False):
		files = [os.path.join(root, _) for _ in files]
		process(files)
	FileWisdom.report()
	return

if __name__ == '__main__':
	for _ in sys.argv[1:]:
		main(_)
