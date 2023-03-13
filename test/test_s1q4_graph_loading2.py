# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network")

from graph import Graph, graph_from_file

import unittest   # The test framework

input="/home/onyxia/projet_ENSAE_1A/input/"

class Test_Reachability(unittest.TestCase):
    def test_network4(self):
        g = graph_from_file(input+"network.04.in")
        self.assertEqual(sorted(g.graph[2],key=lambda x:x[0]), [[1, 4, 89],[3, 4, 3]])
        self.assertEqual(sorted(g.graph[3],key=lambda x:x[0]), [[2, 4, 3], [4, 4, 2]])

if __name__ == '__main__':
    unittest.main()
