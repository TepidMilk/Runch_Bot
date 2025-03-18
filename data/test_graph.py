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
        self.assertEqual(homie.graph, {"Noah": {"Mitch": 1}, "Mitch": {}})

    def test_add_debt_large(self):
        homie = HomiePointsGraph()
        homie.add_debt("Noah", "Mitch", 999999999999999999)
        self.assertEqual(homie.graph, {"Noah": {"Mitch": 999999999999999999}, "Mitch": {}})
    
    def test_add_debt_float(self):
        homie = HomiePointsGraph()
        homie.add_debt("Noah", "Mitch", 1.5)
        self.assertEqual(homie.graph, {"Noah": {"Mitch": 1.5}, "Mitch": {}})

    def test_add_debt_float_int(self):
        homie = HomiePointsGraph()
        homie.add_debt("Noah", "Mitch", 1.5)
        homie.add_debt("Noah", "Mitch", 1)
        self.assertEqual(homie.graph, {"Noah": {"Mitch": 2.5}, "Mitch": {}})

    def test_add_debt_negative(self):
        homie = HomiePointsGraph()
        with self.assertRaises(Exception):
            homie.add_debt("Noah", "Mitch", -1)

    def test_remove_user(self):
        homie = HomiePointsGraph()
        homie.add_user("Noah")
        homie.remove_user("Noah")
        self.assertEqual(homie.graph, {})

    def test_remove_users(self):
        homie = HomiePointsGraph()
        homie.add_user("Noah")
        homie.add_debt("Mitch", "Noah")
        homie.add_debt("Noah", "Mitch")
        homie.remove_user("Noah")
        self.assertEqual(homie.graph, {"Mitch": {}})

    def test_settle_debt(self):
        homie = HomiePointsGraph()
        homie.add_debt("Noah", "Mitch")
        homie.settle_debt("Noah", "Mitch")
        self.assertEqual(homie.graph, {"Noah": {"Mitch":0}, "Mitch": {}})

    def test_settle_debt_excess(self):
        homie = HomiePointsGraph()
        homie.add_debt("Noah", "Mitch")
        homie.settle_debt("Noah", "Mitch", 10)
        self.assertEqual(homie.graph, {"Noah": {"Mitch": 0}, "Mitch": {}})

    def test_settle_debt_no_user(self):
        homie = HomiePointsGraph()
        homie.add_debt("Noah", "Mitch")
        with self.assertRaises(Exception):
            homie.settle_debt("Josie", "Mitch")
            homie.settle_debt("Noah", "Josie")

    def test_get_total_owed(self):
        homie = HomiePointsGraph()
        homie.add_debt("Noah", "Mitch")
        owed = homie.get_total_owed("Mitch")
        self.assertEqual(owed, 1)

    def test_get_total_owed_many(self):
        homie = HomiePointsGraph()
        homie.add_debt("Noah", "Mitch")
        homie.add_debt("Josie", "Mitch")
        homie.add_debt("Owen", "Mitch", 3)
        homie.add_debt("Kevin", "Mitch", 5)
        owed = homie.get_total_owed("Mitch")
        self.assertEqual(owed, 10)

    def test_get_debt(self):
        homie = HomiePointsGraph()
        homie.add_debt("Noah", "Mitch")
        debt = homie.get_debt("Noah")
        self.assertEqual(debt, {"Mitch": 1})

    def test_get_debt_many(self):
        homie = HomiePointsGraph()
        homie.add_debt("Noah", "Mitch")
        homie.add_debt("Noah", "Josie", 2)
        homie.add_debt("Noah", "Owen", )
        homie.add_debt("Noah", "Kevin", 3)
        homie.add_debt("Noah", "Noah", 2)
        debt = homie.get_debt("Noah")
        self.assertEqual(debt, {"Mitch": 1, "Josie": 2, "Owen": 1, "Kevin": 3, "Noah": 2})

    def test_show_all(self):
        homie = HomiePointsGraph()
        homie.add_debt("Noah", "Mitch")
        homie.add_debt("Noah", "Josie", 2)
        homie.add_debt("Devin", "Owen", )
        homie.add_debt("Mitch", "Kevin", 3)
        homie.add_debt("Kevin", "Noah", 2)
        graph = homie.show_all()
        self.assertEqual(graph, homie.graph)
        


if __name__ == "__main__":
    unittest.main()