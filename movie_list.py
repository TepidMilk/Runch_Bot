class MovieList():
    def __init__(self):
        self.movies = {}

    def add_user(self, user_node):
        if user_node not in self.graph:
            self.movies[user_node] = set()

    def add_movie(self, user_node, movie: str):
        if user_node not in self.movies:
            self.add_user(user_node)
        self.movies[user_node].add(movie.upper())