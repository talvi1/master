import os
abs = os.path.abspath("Images") + "/"
cwd = os.listdir(abs)
list = [abs + x for x in cwd]
print (list)

i = 0
for filename in list:
        rename = "pothole" + str(i) + ".jpg"
        i += 1
        os.rename(filename, rename)
