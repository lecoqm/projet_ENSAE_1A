# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network")

from graph import Graph, graph_from_file

import unittest   # The test framework

input="/home/onyxia/projet_ENSAE_1A/input/"

class Test_Reachability(unittest.TestCase):
    def test_network4(self):
        g = graph_from_file(input+"network.04.in")
        self.assertEqual(g.get_path_with_power(1, 4, 4), [1, 2, 3, 4])
        self.assertEqual(g.get_path_with_power(1, 4, 89), [1,4])

if __name__ == '__main__':
    unittest.main()
