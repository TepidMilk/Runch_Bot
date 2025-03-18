import unittest
from graph import HomiePointsGraph

class GraphTest(unittest.TestCase):
    def test_add_user(self):
        homie_graph = HomiePointsGraph()
        homie_graph.add_user("Noah")
        self.assertAlmostEqual(homie_graph.graph, {"Noah": {}})

if __name__ == "__main__":
    unittest.main()