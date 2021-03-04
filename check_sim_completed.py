import os
import pathlib as Path
import re
from termcolor import colored


cwd = Path.Path.cwd()

# List files to see what is mounted
#cwd = r"C:\4_AnnualWindAnalysis"


control_dicts = []
end_times = []
for root, dirs, files in os.walk(cwd):
    for file in files:
        if file.startswith("controlDict") and "mesh" not in str(root):
            p = os.path.join(root, file)
            control_dicts.append(p)
            #print(p)
            try:
                fp = open(p)
                for cnt, line in enumerate(fp):
                    if "endTime" in str(line):
                        words = re.split('\s+', line)
                        if words[2].split(';')[0].isnumeric():
                            end_times.append(words[2].split(';')[0])

            finally:
                fp.close()



sim_dirs = []
for d in control_dicts:
    path = os.sep.join(d.split(os.sep)[0:-2])
    sim_dirs.append(path)

for cnt, dir in enumerate(sim_dirs):
    #print(cnt,dir)
    try:
        dir = Path.Path(sim_dirs[cnt] + "\\" + end_times[cnt])
        if dir.is_dir():
            # Getting the list of directories
            l = os.listdir(dir)

            # Checking if the list is empty or not
            if len(l) != 0:
                print(str(dir), "-", colored("Done", "green"))
            else:
                print(str(dir), "-", colored("Not Done", "RED"))
    except:
        print("Couldn't open", dir)
