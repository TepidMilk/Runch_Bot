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
    
    def remove_movie(self, user_node, movie: str):
        self.movies[user_node].remove(movie.upper())

    def remove_winner(self, movie: str):
        for user in self.movies:
            if movie.upper() in self.movies[user]:
                self.movies[user].remove(movie.upper())

    def get_movie_list(self, user_node):
        return self.movies[user_node]
    
    def get_all_movies(self):
        all_movies = []
        for user in self.movies:
            all_movies.extend(self.movies[user])
        return all_movies
    
