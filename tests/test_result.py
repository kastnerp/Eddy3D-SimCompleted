import unittest   # The test framework
from sim_completed import SimCompleted

from pathlib import Path

class Test_SimCompleted(unittest.TestCase):

    def test_crashed(self):       

        s = SimCompleted.Sim_Completed("tests/12_Case_Type_Slab_NS_Height_30_Dist_20_dir_0_crashed")
        s.analyze()

        
        self.assertEqual(s.n_crashed, 1)
        self.assertEqual(s.n_completed, 0)
        self.assertEqual(s.n_inprogress, 0)
        self.assertEqual(s.n_not_started, 0)
        self.assertEqual(s.n_converged, 0)

    def test_completed(self):       

        s = SimCompleted.Sim_Completed("tests/6_Case_Type_Scatter_Height_20_Dist_20_dir_30_completed")
        s.analyze()

        
        self.assertEqual(s.n_crashed, 0)
        self.assertEqual(s.n_completed, 1)
        self.assertEqual(s.n_inprogress, 0)
        self.assertEqual(s.n_not_started, 0)
        self.assertEqual(s.n_converged, 0)

    def test_inprogress(self):       

        s = SimCompleted.Sim_Completed("tests/6_Case_Type_Scatter_Height_20_Dist_20_dir_40_inprogress")
        s.analyze()

        
        self.assertEqual(s.n_crashed, 0)
        self.assertEqual(s.n_completed, 0)
        self.assertEqual(s.n_inprogress, 1)
        self.assertEqual(s.n_not_started, 0)
        self.assertEqual(s.n_converged, 0)

    def test_converged(self):       

        s = SimCompleted.Sim_Completed("tests/6_Case_Type_Scatter_Height_20_Dist_20_dir_40_converged")
        s.analyze()

        
        self.assertEqual(s.n_crashed, 0)
        self.assertEqual(s.n_completed, 1)
        self.assertEqual(s.n_inprogress, 0)
        self.assertEqual(s.n_not_started, 0)
        self.assertEqual(s.n_converged, 1)

    def test_notstarted(self):       

        s = SimCompleted.Sim_Completed("tests/6_Case_Type_Scatter_Height_20_Dist_20_dir_40_notstarted")
        s.analyze()

        
        self.assertEqual(s.n_crashed, 0)
        self.assertEqual(s.n_completed, 0)
        self.assertEqual(s.n_inprogress, 0)
        self.assertEqual(s.n_not_started, 1)
        self.assertEqual(s.n_converged, 0)

    def test_all(self):       
        s = SimCompleted.Sim_Completed()
        s.analyze()

        
        #self.assertEquals(s.n_crashed, 1)
        #self.assertEquals(s.n_completed, 2)
        self.assertEqual(s.n_inprogress, 1)
        self.assertEqual(s.n_not_started, 1)
        #self.assertEquals(s.n_converged, 1)


    def test_all_inprogress(self):       
        s = SimCompleted.Sim_Completed()
        s.analyze()

        
        #self.assertEquals(s.n_crashed, 1)
        #self.assertEquals(s.n_completed, 2)
        self.assertEqual(s.n_inprogress, 1)
        #self.assertEquals(s.n_converged, 1)


    def test_all_notstarted(self):       
        s = SimCompleted.Sim_Completed()
        s.analyze()

        
        #self.assertEquals(s.n_crashed, 1)
        #self.assertEquals(s.n_completed, 2)
        self.assertEqual(s.n_not_started, 1)
        #self.assertEquals(s.n_converged, 1)

    def test_all_completed(self):       
        s = SimCompleted.Sim_Completed()
        s.analyze()

        
        #self.assertEquals(s.n_crashed, 1)
        self.assertEqual(s.n_completed, 2)
        #self.assertEquals(s.n_not_started, 1)
        #self.assertEquals(s.n_converged, 1)

    def test_all_crashed(self):       
        s = SimCompleted.Sim_Completed()
        s.analyze()

        
        self.assertEqual(s.n_crashed, 1)
        #self.assertEquals(s.n_completed, 2)
        #self.assertEquals(s.n_not_started, 1)
        #self.assertEquals(s.n_converged, 1)


    def test_all_simfolders(self):       
        s = SimCompleted.Sim_Completed()
        s.analyze()
        
        self.assertEqual(s.number_sim_dirs, 5)
       

if __name__ == '__main__':
    unittest.main()

    