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

# Класс Пользователь
class User:
    def __init__(self, user_id: int, name: str, password: str):
        self._user_id = user_id
        self._name = name
        self._password = password
        self._watched_movies: Dict[int, float] = {}
        self._preferred_genres: List[Genre] = []

    @property
    def user_id(self):
        return self._user_id

    @property
    def name(self):
        return self._name

    @property
    def watched_movies(self):
        return self._watched_movies.copy()

    @property
    def preferred_genres(self):
        return self._preferred_genres.copy()

    def check_password(self, password: str):
        #проверка пароля
        return self._password == password

    def add_rating(self, movie_id: int, rating: float):
        #оценка фильма
        if 0 <= rating <= 10:
            self._watched_movies[movie_id] = rating
        else:
            print("Оценка должна быть от 0 до 10!")

    def set_preferred_genres(self, genres: List[Genre]):
        self._preferred_genres = genres

    def has_watched(self, movie_id: int):
        return movie_id in self._watched_movies

    def __str__(self):
        return f"Пользователь: {self._name} (ID: {self._user_id})"

    def __repr__(self):
        return f"User(id={self._user_id}, name='{self._name}')"
