import os
import sys
import json
import ctypes
import hashlib

AUG = ['sha256', 'sha1', 'sha512', 'md5']	# AUG==algorithms_usually_guaranteed# crc32?

hashes = dict(zip(AUG, [None]*len(AUG)))

def determineBS(file_size):
	if file_size < 15 * 1024:
		return file_size
	else:
		free_ram = 0# 2G or less than 2G
		if file_size <= free_ram/10:
			return file_size
		else:
			return 100 * 1024
	return

def main(filePath):
	try:
		fp = open(filePath, mode="rb")
	except:
		# alert user in box
		return
	with fp:
		file_size = os.stat(filePath).st_size
		BLOCK_SIZE = determineBS(file_size)
		done = 0
		for _ in AUG:
			hashes[_] = getattr(hashlib, _)()
		while True:
			print("hash calculation %2f completed . . ." % ((done/file_size)*100))
			x = fp.read(BLOCK_SIZE)
			if len(x) == 0:	break
			for _ in hashes.keys():
				hashes[_].update(x)
			done+= BLOCK_SIZE
		for _ in sorted(hashes.keys()):
			print("%s\t%s" % (_, hashes[_].hexdigest()))
	# print(hashes)
	# json.dumps(hashes, sort_keys=True, indent=4)
	return

if __name__ == '__main__':
	for _ in sys.argv[1:]:
		main(_)
