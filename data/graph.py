class HomiePointsGraph():
    def __init__(self):
        self.graph = {}

    def add_user(self, user_node):
        if user_node not in self.graph:
            self.graph[user_node] = {}
        
    def remove_user(self, user_node):
        for person in self.graph:
            if user_node in self.graph[person]:
                del self.graph[person][user_node]
        del self.graph[user_node]

    def add_debt(self, user_node, to_node, points=1):
        if points < 1:
            raise Exception("Invalid Debt")
        
        if user_node not in self.graph:
            self.add_user(user_node)
        if to_node not in self.graph:
            self.add_user(to_node)
        
        if to_node in self.graph[user_node]:
            self.graph[user_node][to_node] += points
        else:
            self.graph[user_node][to_node] = points

        if user_node not in self.graph[to_node]:
            self.graph[to_node][user_node] = 0
        

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
        total = 0
        for user in self.graph:
            if user_node in self.graph[user]:
                total += self.graph[user][user_node]
        return total
    
    def get_debt(self, user_node):
        return self.graph[user_node]
    
    def get_score(self, user_node, to_node):
        x = self.graph[user_node][to_node]
        y = self.graph[to_node][user_node]
        return (x,y)
    
        