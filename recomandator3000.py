from enum import Enum
from typing import List, Dict, Optional


# Перечисление жанров
class Genre(Enum):
    ACTION = "Боевик"
    COMEDY = "Комедия"
    DRAMA = "Драма"
    HORROR = "Ужасы"
    SCI_FI = "Фантастика"
    ROMANCE = "Романтика"
    THRILLER = "Триллер"
    FANTASY = "Фэнтези"
    ADVENTURE = "Приключения"
    ANIMATION = "Мультфильм"

class Movie:

    def __init__(self, movie_id: int, title: str, genres: List[Genre],
                 director: str, year: int, rating: float):
        self._movie_id = movie_id
        self._title = title
        self._genres = genres
        self._director = director
        self._year = year
        self._rating = rating

    @property
    def movie_id(self):
        return self._movie_id

    @property
    def title(self):
        return self._title

    @property
    def genres(self):
        return self._genres

    @property
    def director(self):
        return self._director

    @property
    def year(self):
        return self._year

    @property
    def rating(self):
        return self._rating

    def __str__(self):
        genres_str = ", ".join([g.value for g in self._genres])
        return f"{self._title} ({self._year}) - {genres_str}, режиссер: {self._director}, рейтинг: {self._rating}"

    def __repr__(self):
        return f"Movie(id={self._movie_id}, title='{self._title}')"