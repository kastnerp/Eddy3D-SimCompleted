import os
import pathlib as Path
import re
from termcolor import colored
import colorama

colorama.init()

cwd = Path.Path.cwd()

# List files to see what is mounted
# cwd = r"C:\CornellValidationSnapSimpleModel"

control_dicts = []
end_times = []
for root, dirs, files in os.walk(cwd):
    for file in files:
        if file.startswith("controlDict") and "mesh" not in str(root):
            p = os.path.join(root, file)
            control_dicts.append(p)
            # print(p)
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
    # print(cnt,dir)
    try:
        wind_dir_directory = Path.Path(sim_dirs[cnt] + "\\" + end_times[cnt])
        if wind_dir_directory.is_dir():
            l = os.listdir(wind_dir_directory)

            # Checking if the directory is empty or not
            if len(l) != 0:
                print(str(wind_dir_directory), "-", colored("Done", "green"))
            else:
                print(str(wind_dir_directory), "-", colored("Not Done", "red"))
        else:
            # Check if converged
            converged = False
            crashed = False
            logfile = dir + "\log"
            try:
                fp = open(logfile)
                for cnt, line in enumerate(fp):
                    if "SIMPLE solution converged in" in str(line):
                        converged = True
                    if "job aborted:" in str(line):
                        crashed = True
                    if "Exec   : simpleFoam":
                        crashed = False

                if converged == True:
                    print(str(dir), "-", colored("Done", "green"))
                elif crashed == True:
                    print(str(dir), "-", colored("Crashed", "red"))
                else:

                    print(str(dir), "-", colored("Not Done", "orange"))

            finally:
                fp.close()




    except:
        print(str(wind_dir_directory), "-", colored("Couldn't open", "yellow"))
        # print("Couldn't open", dir)
