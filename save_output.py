import subprocess

example = "del"
option = ""
f = open("output/" + example + ".txt", "w")
subprocess = subprocess.Popen("ILASP --version=4 " + example + ".las " + option, shell=True, stdout=f)
# subprocess_return = subprocess.stdout.read()
# print(subprocess_return)