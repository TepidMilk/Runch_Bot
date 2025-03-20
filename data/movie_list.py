class MovieList():
    def __init__(self):
        self.movies = {}

    def add_movie(self, user_node, movie: str):
        if user_node not in self.movies:
            self.movies[user_node] = movie
        else:
            return
        
    
    def remove_movie(self, user_node):
        del self.movies[user_node]

    def reset_list(self):
        self.movies = {}
    
    def get_all_movies(self):
        return self.movies.items()
    