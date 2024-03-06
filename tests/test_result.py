import pathlib
import unittest  # The test framework

from pyEddy3D import SimCompleted


class Test_SimCompleted(unittest.TestCase):

    def fix_cwd(self, p):
        print("CWD: " + str(pathlib.Path.cwd()))
        cwd_mod = pathlib.Path.cwd() / "tests" if not str(pathlib.Path.cwd()).endswith(
            "\\tests") else pathlib.Path.cwd()
        path = cwd_mod / p
        print(path)
        return path

    def printout(self, s):
        print("Mesh Crashed " + str(s.n_mesh_crashed))
        print("Crashed " + str(s.n_crashed))
        print("Completed " + str(s.n_completed))
        print("In progress " + str(s.n_inprogress))
        print("Not started " + str(s.n_not_started))
        print("Converged " + str(s.n_converged))

    def test_crashed(self):
        folder = "12_Case_Type_Slab_NS_Height_30_Dist_20_dir_0_crashed"
        path = self.fix_cwd(folder)

        s = SimCompleted.Simulation(path)
        s.analyze()

        self.printout(s)

        self.assertEqual(1, s.n_crashed)
        self.assertEqual(0, s.n_mesh_crashed)
        self.assertEqual(0, s.n_completed)
        self.assertEqual(0, s.n_inprogress)
        self.assertEqual(0, s.n_not_started)
        self.assertEqual(0, s.n_converged)

    def test_crashed_2(self):
        folder = "Case_36_crashed"
        path = self.fix_cwd(folder)

        s = SimCompleted.Simulation(path)
        s.analyze()

        self.printout(s)

        self.assertEqual(1, s.n_crashed)
        self.assertEqual(0, s.n_mesh_crashed)
        self.assertEqual(0, s.n_completed)
        self.assertEqual(0, s.n_inprogress)
        self.assertEqual(0, s.n_not_started)
        self.assertEqual(0, s.n_converged)

    def test_mesh_crashed(self):
        folder = "Case_17_m_crashed"
        path = self.fix_cwd(folder)

        s = SimCompleted.Simulation(path)
        s.analyze()

        self.printout(s)

        self.assertEqual(0, s.n_crashed)
        self.assertEqual(1, s.n_mesh_crashed)
        self.assertEqual(0, s.n_completed)
        self.assertEqual(0, s.n_inprogress)
        self.assertEqual(0, s.n_not_started)
        self.assertEqual(0, s.n_converged)

    def test_completed(self):
        folder = "6_Case_Type_Scatter_Height_20_Dist_20_dir_30_completed"
        path = self.fix_cwd(folder)

        s = SimCompleted.Simulation(path)
        s.analyze()

        self.printout(s)

        self.assertEqual(0, s.n_crashed)
        self.assertEqual(0, s.n_mesh_crashed)
        self.assertEqual(1, s.n_completed)
        self.assertEqual(0, s.n_inprogress)
        self.assertEqual(0, s.n_not_started)
        self.assertEqual(0, s.n_converged)

    def test_in_progress(self):
        folder = "6_Case_Type_Scatter_Height_20_Dist_20_dir_40_inprogress"
        path = self.fix_cwd(folder)

        s = SimCompleted.Simulation(path)
        s.analyze()

        self.printout(s)

        self.assertEqual(0, s.n_crashed)
        self.assertEqual(0, s.n_mesh_crashed)
        self.assertEqual(0, s.n_completed)
        self.assertEqual(1, s.n_inprogress)
        self.assertEqual(0, s.n_not_started)
        self.assertEqual(0, s.n_converged)

    def test_converged(self):
        folder = "6_Case_Type_Scatter_Height_20_Dist_20_dir_40_converged"
        path = self.fix_cwd(folder)

        s = SimCompleted.Simulation(path)
        s.analyze()

        self.printout(s)

        self.assertEqual(0, s.n_crashed)
        self.assertEqual(0, s.n_mesh_crashed)
        self.assertEqual(1, s.n_completed)
        self.assertEqual(0, s.n_inprogress)
        self.assertEqual(0, s.n_not_started)
        self.assertEqual(1, s.n_converged)

    def test_not_started(self):
        folder = "6_Case_Type_Scatter_Height_20_Dist_20_dir_40_notstarted"
        path = self.fix_cwd(folder)

        s = SimCompleted.Simulation(path)
        s.analyze()

        self.printout(s)

        self.assertEqual(0, s.n_crashed)
        self.assertEqual(0, s.n_mesh_crashed)
        self.assertEqual(0, s.n_completed)
        self.assertEqual(0, s.n_inprogress)
        self.assertEqual(1, s.n_not_started)
        self.assertEqual(0, s.n_converged)

    def test_all(self):
        s = SimCompleted.Simulation()
        s.analyze()

        self.printout(s)

        self.assertEqual(2, s.n_crashed)
        self.assertEqual(1, s.n_mesh_crashed)
        self.assertEqual(2, s.n_completed)
        self.assertEqual(1, s.n_inprogress)
        self.assertEqual(1, s.n_not_started)
        self.assertEqual(1, s.n_converged)

    def test_all_in_progress(self):
        s = SimCompleted.Simulation()
        s.analyze()

        self.printout(s)

        # self.assertEquals(s.n_crashed, 1)
        # self.assertEquals(s.n_completed, 2)
        self.assertEqual(1, s.n_inprogress)
        # self.assertEquals(s.n_converged, 1)

    def test_all_not_started(self):
        s = SimCompleted.Simulation()
        s.analyze()

        self.printout(s)

        # self.assertEquals(s.n_crashed, 1)
        # self.assertEquals(s.n_completed, 2)
        self.assertEqual(1, s.n_not_started)
        # self.assertEquals(s.n_converged, 1)

    def test_all_completed(self):
        s = SimCompleted.Simulation()
        s.analyze()

        self.printout(s)

        # self.assertEquals(s.n_crashed, 1)
        self.assertEquals(2, s.n_completed)
        # self.assertEquals(s.n_not_started, 1)
        # self.assertEquals(s.n_converged, 1)

    def test_all_crashed(self):
        s = SimCompleted.Simulation()
        s.analyze()

        self.printout(s)

        self.assertEqual(2, s.n_crashed)
        self.assertEqual(1, s.n_mesh_crashed)
        # self.assertEquals(s.n_completed, 2)
        # self.assertEquals(s.n_not_started, 1)
        # self.assertEquals(s.n_converged, 1)

    def test_all_simfolders(self):
        s = SimCompleted.Simulation()
        s.analyze()

        self.printout(s)

        self.assertEqual(7, s.number_sim_dirs)


if __name__ == '__main__':
    unittest.main()
