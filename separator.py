example = "ex1_error"
f = open("clingo/" + example + ".txt", "r+")
text = f.read()
f.close()
f = open("clingo/" + example + ".txt", "w")
literals = text.split(' ')
for i in literals:
    if i[:3] != 'use' and i[:3] != 'del' and i[:9] != 'extension':
        f.write(i + "\n")
    
f.close()