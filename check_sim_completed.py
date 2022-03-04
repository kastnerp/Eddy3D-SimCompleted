import os
from pathlib import Path
import re
from turtle import done
from termcolor import colored
import colorama
from enum import Enum

colorama.init()


# List files to see what is mounted
#cwd = r"E:\CampusSmallPatch_BS5"


class SimStatus(Enum):
    DONE = 0
    CRASHED = 1
    NOTSTARTED = 2
    CONVERGED = 3
    INPROGRESS = 4


class SimCompleted():
    def __init__(self):
        self.cwd = Path.cwd()

        self.subdirs = self.get_subdirs(self.cwd)
        self.control_dicts, self.end_times = self.get_control_dicts(self.cwd)
        self.sim_dirs,  self.last_iters = self.get_last_iterations(self.control_dicts)


        self.sim_status = SimStatus(2)

        self.cases_crashed = []
        self.cases_not_started = []
        self.cases_done = []
        self.cases_converged = []

        self.progress = 0
        self.number_sim_dirs = len(self.sim_dirs)
        self.analyze()

        self.n_completed = len(self.cases_done) + len(self.cases_converged)
        self.n_crashed = len(self.cases_crashed) 
        self.n_not_started = len(self.cases_not_started) 

        self.verdict()


    def verdict(self):




        string_done = str(self.n_completed) + " out of " + str(self.number_sim_dirs) + " simulations done or " + str(round(100*self.n_completed/self.number_sim_dirs, 1))+"%"
        print(colored(string_done, "green"))

        print("\n###")
        print("\nCrashed Cases:", str(self.n_crashed))



        for i in self.cases_crashed: print("start",i)


        print("\n###")
        print("\nNot started:", str(self.n_not_started))

        for i in self.cases_not_started: print("\\".join(i.split('\\')[:-1])+"\\run.bat")

        print("\n###")
        print("\nRename cases remaining")
        for i in self.cases_not_started: print("ren " + "\\".join(i.split('\\')[:-1])+"\\Batch_ESLTower64\_mesh_and_sim_ESLTower64.bat _mesh_and_sim_ESLTower64_next.bat")




    def analyze(self):

        for cnt, dir in enumerate(self.sim_dirs):
            self.check_case_status(dir, cnt)
            self.print_status(dir)       




    def print_status(self,  current_dir ):
        if self.sim_status == SimStatus.CONVERGED:
            self.cases_converged.append(current_dir)
            print(str(current_dir), "-", colored("Converged", "green"))        

        elif self.sim_status ==  SimStatus.INPROGRESS:
            self.cases_inprogress.append(current_dir)
            print(str(current_dir), "-", colored(str(round(self.progress, 1)) + "% Done", "cyan"))

        elif self.sim_status ==  SimStatus.NOTSTARTED:
            self.cases_not_started.append(current_dir)
            print(str(current_dir), "-", colored("Not Started", "white"))

        elif self.sim_status ==  SimStatus.CRASHED:
            self.cases_crashed.append(current_dir)
            print(str(current_dir), "-", colored("Crashed", "red"))

        elif self.sim_status ==  SimStatus.DONE: 
            self.cases_done.append(current_dir)        
            print(str(current_dir), "-", colored("Done", "cyan"))



    def check_case_status(self, dir, cnt):
            wind_dir_directory = Path(dir + "\\" + self.end_times[cnt])
            try:
                self.check_if_done(wind_dir_directory)    
            except:
                self.check_if_converged(dir, cnt)
        


    def check_if_done(self, dir, cnt):
        if dir.is_dir():
            l = os.listdir(dir)

            # Checking if the directory is empty or not
            if len(l) != 0:
                self.sim_status = SimStatus.DONE





    def get_subdirs(self, path):
        l = []
        for root, subdirectories, files in os.walk(path):
            for subdirectory in subdirectories:
                l.append(subdirectory)

        return l

    def get_control_dicts(self, cwd):
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

    def get_last_iterations(self, control_dicts):
        sim_dirs = []
        last_iters = []

        for d in control_dicts:
            path = os.sep.join(d.split(os.sep)[0:-2])
            sim_dirs.append(path)
            l = self.get_subdirs(path)
            last_iter = 0
            for el in l:
                if el.isnumeric():
                    if int(el) > int(last_iter):
                        last_iter = el
            last_iters.append(last_iter)

        return sim_dirs, last_iters

    def check_case_progress(self, cnt):
        progress = int(self.last_iters[cnt]) / int(self.end_times[cnt]) * 100
        if progress > 0 and progress <  100:
            self.sim_status = SimStatus.INPROGRESS
            self.progress = progress

        elif progress == 100:
            self.sim_status = SimStatus.DONE
            self.progress = progress

        else:
            self.sim_status = SimStatus.NOTSTARTED



    def check_if_converged(self, dir, cnt):
        # Check if converged

        logfile = dir / Path("log")
        if logfile.is_file():
            fp = open(logfile)
            lines = fp.readlines()
            try:
                for line in lines:
                    if "SIMPLE solution converged in" in str(line):
                        self.sim_status = SimStatus.CONVERGED
                        break
                    elif "job aborted:" in str(line):
                        self.sim_status = SimStatus.CRASHED
                        # break
                    elif "simpleFoam ended prematurely and may have crashed. exit code 3" in str(line):
                        self.sim_status = SimStatus.CRASHED
                        # break
                    elif "[0] process exited without calling finalize" in str(line):
                        self.sim_status = SimStatus.CRASHED
                        # break
                    elif "---- error analysis -----" in str(line):
                        self.sim_status = SimStatus.CRASHED
                        # break
                    elif "Finalising parallel run":
                        self.sim_status = SimStatus.DONE
                        break

    

            finally:
                fp.close()

        else:
            self.check_case_progress(cnt)




SimCompleted()
