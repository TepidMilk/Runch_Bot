class HomiePointsGraph():
    def __init__(self):
        self.graph = {}

    def add_user(self, user_node):
        if user_node not in self.graph:
            self.graph[user_node] = {}

    def add_debt(self, user_node, to_node, points=1):
        if points < 1:
            raise Exception("Invalid Debt")
        
        if user_node not in self.graph:
            self.add_user(user_node)
            self.graph[user_node][to_node] = points
        else:
            self.graph[user_node][to_node] += points

    def settle_debt(self, user_node, to_node, points=0):
        if points < 0:
            raise Exception("Invalid Settlement")
        if user_node not in self.graph:
            raise Exception("User not found")
        if to_node not in self.graph[user_node]:
            raise Exception("Invalid target")
        if points == 0:
            self.graph[user_node][to_node] = 0
        elif points >= self.graph[user_node][to_node]:
            self.graph[user_node][to_node] = 0
        else:
            self.graph[user_node][to_node] -= points
    
    def get_total_owed(self, user_node):
        return self.graph.get(user_node, [])
    
    def get_debt(self, user_node):
        return self.graph[user_node]
    
    def show_all(self):
        return self.graph
        