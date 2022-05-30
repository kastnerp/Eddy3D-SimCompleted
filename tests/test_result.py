import pathlib
import unittest  # The test framework

from sim_completed import SimCompleted


class Test_SimCompleted(unittest.TestCase):

    def printout(self, s):
        print("Crashed " + str(s.n_crashed))
        print("Completed " + str(s.n_completed))
        print("In progress " + str(s.n_inprogress))
        print("Not started " + str(s.n_not_started))
        print("Converged " + str(s.n_converged))

    def test_crashed(self):

        print("CWD: " + str(pathlib.Path.cwd()))
        cwd_mod = pathlib.Path.cwd() / "tests" if not str(pathlib.Path.cwd()).endswith("\\tests") else pathlib.Path.cwd()
        path = cwd_mod / "12_Case_Type_Slab_NS_Height_30_Dist_20_dir_0_crashed"
        print(path)

        s = SimCompleted.Sim_Completed(path)
        s.analyze()

        self.printout(s)

        self.assertEqual(s.n_crashed, 1)
        self.assertEqual(s.n_completed, 0)
        self.assertEqual(s.n_inprogress, 0)
        self.assertEqual(s.n_not_started, 0)
        self.assertEqual(s.n_converged, 0)

    def test_crashed_2(self):
        print("CWD: " + str(pathlib.Path.cwd()))
        cwd_mod = pathlib.Path.cwd() / "tests" if not str(pathlib.Path.cwd()).endswith(
            "\\tests") else pathlib.Path.cwd()
        path = cwd_mod / "Case_36_crashed"
        print(path)

        s = SimCompleted.Sim_Completed(path)
        s.analyze()

        self.printout(s)

        self.assertEqual(s.n_crashed, 1)
        self.assertEqual(s.n_completed, 0)
        self.assertEqual(s.n_inprogress, 0)
        self.assertEqual(s.n_not_started, 0)
        self.assertEqual(s.n_converged, 0)

    def test_completed(self):
        print("CWD: " + str(pathlib.Path.cwd()))
        cwd_mod = pathlib.Path.cwd() / "tests" if not str(pathlib.Path.cwd()).endswith(
            "\\tests") else pathlib.Path.cwd()
        path = cwd_mod / "6_Case_Type_Scatter_Height_20_Dist_20_dir_30_completed"
        print(path)

        s = SimCompleted.Sim_Completed(path)
        s.analyze()

        self.printout(s)

        self.assertEqual(s.n_crashed, 0)
        self.assertEqual(s.n_completed, 1)
        self.assertEqual(s.n_inprogress, 0)
        self.assertEqual(s.n_not_started, 0)
        self.assertEqual(s.n_converged, 0)

    def test_inprogress(self):
        print("CWD: " + str(pathlib.Path.cwd()))
        cwd_mod = pathlib.Path.cwd() / "tests" if not str(pathlib.Path.cwd()).endswith(
            "\\tests") else pathlib.Path.cwd()
        path = cwd_mod / "6_Case_Type_Scatter_Height_20_Dist_20_dir_40_inprogress"
        print(path)

        s = SimCompleted.Sim_Completed(path)
        s.analyze()

        self.printout(s)

        self.assertEqual(s.n_crashed, 0)
        self.assertEqual(s.n_completed, 0)
        self.assertEqual(s.n_inprogress, 1)
        self.assertEqual(s.n_not_started, 0)
        self.assertEqual(s.n_converged, 0)

    def test_converged(self):
        print("CWD: " + str(pathlib.Path.cwd()))
        cwd_mod = pathlib.Path.cwd() / "tests" if not str(pathlib.Path.cwd()).endswith(
            "\\tests") else pathlib.Path.cwd()
        path = cwd_mod / "6_Case_Type_Scatter_Height_20_Dist_20_dir_40_converged"
        print(path)

        s = SimCompleted.Sim_Completed(path)
        s.analyze()

        self.printout(s)

        self.assertEqual(s.n_crashed, 0)
        self.assertEqual(s.n_completed, 1)
        self.assertEqual(s.n_inprogress, 0)
        self.assertEqual(s.n_not_started, 0)
        self.assertEqual(s.n_converged, 1)

    def test_notstarted(self):
        print("CWD: " + str(pathlib.Path.cwd()))
        cwd_mod = pathlib.Path.cwd() / "tests" if not str(pathlib.Path.cwd()).endswith(
            "\\tests") else pathlib.Path.cwd()
        path = cwd_mod / "6_Case_Type_Scatter_Height_20_Dist_20_dir_40_notstarted"
        print(path)

        s = SimCompleted.Sim_Completed(path)
        s.analyze()

        self.printout(s)

        self.assertEqual(s.n_crashed, 0)
        self.assertEqual(s.n_completed, 0)
        self.assertEqual(s.n_inprogress, 0)
        self.assertEqual(s.n_not_started, 1)
        self.assertEqual(s.n_converged, 0)

    def test_all(self):
        s = SimCompleted.Sim_Completed()
        s.analyze()

        self.printout(s)

        # self.assertEquals(s.n_crashed, 1)
        # self.assertEquals(s.n_completed, 2)
        self.assertEqual(s.n_inprogress, 1)
        self.assertEqual(s.n_not_started, 1)
        # self.assertEquals(s.n_converged, 1)

    def test_all_inprogress(self):
        s = SimCompleted.Sim_Completed()
        s.analyze()

        self.printout(s)

        # self.assertEquals(s.n_crashed, 1)
        # self.assertEquals(s.n_completed, 2)
        self.assertEqual(s.n_inprogress, 1)
        # self.assertEquals(s.n_converged, 1)

    def test_all_notstarted(self):
        s = SimCompleted.Sim_Completed()
        s.analyze()

        self.printout(s)

        # self.assertEquals(s.n_crashed, 1)
        # self.assertEquals(s.n_completed, 2)
        self.assertEqual(s.n_not_started, 1)
        # self.assertEquals(s.n_converged, 1)

    def test_all_completed(self):
        s = SimCompleted.Sim_Completed()
        s.analyze()

        self.printout(s)

        # self.assertEquals(s.n_crashed, 1)
        self.assertEqual(s.n_completed, 2)
        # self.assertEquals(s.n_not_started, 1)
        # self.assertEquals(s.n_converged, 1)

    def test_all_crashed(self):
        s = SimCompleted.Sim_Completed()
        s.analyze()

        self.printout(s)

        self.assertEqual(s.n_crashed, 2)
        # self.assertEquals(s.n_completed, 2)
        # self.assertEquals(s.n_not_started, 1)
        # self.assertEquals(s.n_converged, 1)

    def test_all_simfolders(self):
        s = SimCompleted.Sim_Completed()
        s.analyze()

        self.printout(s)

        self.assertEqual(s.number_sim_dirs, 6)


if __name__ == '__main__':
    unittest.main()
