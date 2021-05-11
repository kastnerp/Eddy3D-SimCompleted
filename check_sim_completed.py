import os
from pathlib import Path
import re
from termcolor import colored
import colorama

colorama.init()

cwd = Path.cwd()

# List files to see what is mounted
#cwd = r"E:\CampusSmallPatch_BS5"


def print_progress(cnt):
    progress = int(last_iters[cnt]) / int(end_times[cnt]) * 100
    if progress > 0:
        print(str(sim_dirs[cnt]), "-", colored(str(round(progress, 1)) + "% Done", "cyan"))
    else:
        print(str(sim_dirs[cnt]), "-", colored("Not Started", "white"))


def get_all_subdirs(path):
    l = []
    for root, subdirectories, files in os.walk(path):
        for subdirectory in subdirectories:
            l.append(subdirectory)

    return l


def get_control_dicts(cwd):
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

    return control_dicts, end_times


def get_last_iterations(control_dicts):
    sim_dirs = []
    last_iters = []

    for d in control_dicts:
        path = os.sep.join(d.split(os.sep)[0:-2])
        sim_dirs.append(path)
        l = get_all_subdirs(path)
        last_iter = 0
        for el in l:
            if el.isnumeric():
                if int(el) > int(last_iter):
                    last_iter = el
        last_iters.append(last_iter)

    return sim_dirs, last_iters




def check_if_converged(dir, cnt):
    # Check if converged
    converged = False
    crashed = False
    logfile = dir / Path("log")
    if logfile.is_file():
        fp = open(logfile)
        lines = fp.readlines()
        try:
            for line in lines:
                if "SIMPLE solution converged in" in str(line):
                    converged = True
                    #break
                elif "job aborted:" in str(line):
                    crashed = True
                    #break
                elif "simpleFoam ended prematurely and may have crashed. exit code 3" in str(line):
                    crashed = True
                    #break
                elif "[0] process exited without calling finalize" in str(line):
                    crashed = True
                    #break
                elif "---- error analysis -----" in str(line):
                    crashed = True
                    #break
                #elif "Exec   : simpleFoam":
                    #crashed = False
                    #break

            if converged == True:
                print(str(dir), "-", colored("Done", "green"))
            elif crashed == True:
                print(str(dir), "-", colored("Crashed", "red"))
            else:

                print_progress(cnt)

        finally:
            fp.close()

    else:
        print_progress(cnt)



control_dicts, end_times = get_control_dicts(cwd)

sim_dirs ,  last_iters = get_last_iterations(control_dicts)




for cnt, dir in enumerate(sim_dirs):
    # print(cnt,dir)
    wind_dir_directory = Path(sim_dirs[cnt] + "\\" + end_times[cnt])
    try:
        if wind_dir_directory.is_dir():
            l = os.listdir(wind_dir_directory)

            # Checking if the directory is empty or not
            if len(l) != 0:
                print(str(wind_dir_directory), "-", colored("Done", "green"))
            else:
                print(str(wind_dir_directory), "-", colored("Directory empty", "white"))
        else:
            check_if_converged(sim_dirs[cnt], cnt)




    except:

        check_if_converged(sim_dirs[cnt], cnt)
