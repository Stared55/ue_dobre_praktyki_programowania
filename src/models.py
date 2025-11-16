class Movie:
    def __init__(self, movieId: int, title: str, genres: str):
        self.movieId = int(movieId)
        self.title = title
        self.genres = genres

class Link:
    def __init__(self, movieId: int, imdbId: int, tmdbId: int):
        self.movieId = int(movieId)
        self.imdbId = int(imdbId)
        self.tmdbId = int(tmdbId) if tmdbId else None 

class Rating:
    def __init__(self, userId: int, movieId: int, rating: float, timestamp: int):
        self.userId = int(userId)
        self.movieId = int(movieId)
        self.rating = float(rating)
        self.timestamp = int(timestamp)

class Tag:
    def __init__(self, userId: int, movieId: int, tag: str, timestamp: int):
        self.userId = int(userId)
        self.movieId = int(movieId)
        self.tag = tag
        self.timestamp = int(timestamp)