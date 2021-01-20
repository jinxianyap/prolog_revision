import subprocess

example = "add2"
f = open("output/" + example + ".txt", "w")
proc = subprocess.Popen("ILASP --version=4 --max-rule-length=3 " + example + ".las -s", shell=True, stdout=f)
proc = subprocess.Popen("ILASP --version=4 --max-rule-length=3 " + example + ".las ", shell=True, stdout=f)
try:
    outs, errs = proc.communicate(timeout=20)
except:
    proc.kill()
    outs, errs = proc.communicate()
# subprocess_return = subprocess.stdout.read()
# print(subprocess_return)