import unittest
from graph import HomiePointsGraph

class GraphTest(unittest.TestCase):
    def test_add_user(self):
        homie_graph = HomiePointsGraph()
        homie_graph.add_user("Noah")
        self.assertEqual(homie_graph.graph, {"Noah": {}})
    
    def test_add_debt(self):
        homie = HomiePointsGraph()
        homie.add_debt("Noah", "Mitch")
        self.assertEqual(homie.graph, {"Noah": {"Mitch": 1}})

    def test_add_debt_large(self):
        homie = HomiePointsGraph()
        homie.add_debt("Noah", "Mitch", 999999999999999999)
        self.assertEqual(homie.graph, {"Noah": {"Mitch": 999999999999999999}})
    
    def test_add_debt_float(self):
        homie = HomiePointsGraph()
        homie.add_debt("Noah", "Mitch", 1.5)
        self.assertEqual(homie.graph, {"Noah": {"Mitch": 1.5}})

    def test_add_debt_float_int(self):
        homie = HomiePointsGraph()
        homie.add_debt("Noah", "Mitch", 1.5)
        homie.add_debt("Noah", "Mitch", 1)
        self.assertEqual(homie.graph, {"Noah": {"Mitch": 2.5}})

    def test_add_debt_negative(self):
        homie = HomiePointsGraph()
        with self.assertRaises(Exception):
            homie.add_debt("Noah", "Mitch", -1)

    def test_settle_debt(self):
        homie = HomiePointsGraph()
        homie.add_debt("Noah", "Mitch")
        homie.settle_debt("Noah", "Mitch")
        self.assertEqual(homie.graph, {"Noah": {"Mitch":0}})
        


if __name__ == "__main__":
    unittest.main()