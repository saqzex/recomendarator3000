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

# Менеджер данных
class DataManager:

    def __init__(self):
        self._movies: Dict[int, Movie] = {}
        self._users: Dict[int, User] = {}
        self._next_movie_id = 1
        self._next_user_id = 1

    def add_movie(self, movie: Movie):
        #добавление фильма
        self._movies[movie.movie_id] = movie

    def add_user(self, user: User):
        #добавление пользователя
        self._users[user.user_id] = user

    def get_movie(self, movie_id: int):
        return self._movies.get(movie_id)

    def get_user_by_name(self, name: str):
        for user in self._users.values():
            if user.name.lower() == name.lower():
                return user
        return None

    def authenticate(self, name: str, password: str):
        #проверка логина и пароля
        user = self.get_user_by_name(name)
        if user and user.check_password(password):
            return user
        return None

    def get_all_movies(self):
        return list(self._movies.values())

    def get_all_users(self):
        return list(self._users.values())

    def get_next_movie_id(self):
        current_id = self._next_movie_id
        self._next_movie_id += 1
        return current_id

    def get_next_user_id(self):
        current_id = self._next_user_id
        self._next_user_id += 1
        return current_id

    def load_test_data(self):
        #тестовый набор фильмов
        movies_data = [
            ("Матрица", [Genre.SCI_FI, Genre.ACTION], "Лана Вачовски", 1999, 8.7),
            ("Крестный отец", [Genre.DRAMA, Genre.THRILLER], "Фрэнсис Форд Коппола", 1972, 9.2),
            ("Темный рыцарь", [Genre.ACTION, Genre.DRAMA], "Кристофер Нолан", 2008, 9.0),
            ("Побег из Шоушенка", [Genre.DRAMA], "Фрэнк Дарабонт", 1994, 9.3),
            ("Форрест Гамп", [Genre.DRAMA, Genre.COMEDY], "Роберт Земекис", 1994, 8.8),
            ("Начало", [Genre.SCI_FI, Genre.THRILLER], "Кристофер Нолан", 2010, 8.8),
            ("Интерстеллар", [Genre.SCI_FI, Genre.DRAMA], "Кристофер Нолан", 2014, 8.6),
            ("Бойцовский клуб", [Genre.DRAMA, Genre.THRILLER], "Дэвид Финчер", 1999, 8.8),
            ("Зеленая миля", [Genre.DRAMA, Genre.FANTASY], "Фрэнк Дарабонт", 1999, 8.6),
            ("Властелин колец: Возвращение короля", [Genre.FANTASY, Genre.ADVENTURE], "Питер Джексон", 2003, 8.9),
            ("Пираты Карибского моря", [Genre.ADVENTURE, Genre.COMEDY], "Гор Вербински", 2003, 8.0),
            ("Гарри Поттер и философский камень", [Genre.FANTASY, Genre.ADVENTURE], "Крис Коламбус", 2001, 7.6),
            ("Титаник", [Genre.ROMANCE, Genre.DRAMA], "Джеймс Кэмерон", 1997, 7.8),
            ("Аватар", [Genre.SCI_FI, Genre.ADVENTURE], "Джеймс Кэмерон", 2009, 7.8),
            ("Король Лев", [Genre.ANIMATION, Genre.DRAMA], "Роджер Аллерс", 1994, 8.5),
            ("Сияние", [Genre.HORROR, Genre.THRILLER], "Стэнли Кубрик", 1980, 8.4),
            ("Чужой", [Genre.HORROR, Genre.SCI_FI], "Ридли Скотт", 1979, 8.4),
            ("Терминатор 2", [Genre.ACTION, Genre.SCI_FI], "Джеймс Кэмерон", 1991, 8.5),
            ("Мстители", [Genre.ACTION, Genre.SCI_FI], "Джосс Уидон", 2012, 8.0),
            ("Джокер", [Genre.DRAMA, Genre.THRILLER], "Тодд Филлипс", 2019, 8.4),
            ("Паразиты", [Genre.DRAMA, Genre.THRILLER], "Пон Джун Хо", 2019, 8.5),
            ("Однажды в Голливуде", [Genre.COMEDY, Genre.DRAMA], "Квентин Тарантино", 2019, 7.6),
            ("Дюна", [Genre.SCI_FI, Genre.ADVENTURE], "Дени Вильнёв", 2021, 8.0),
            ("Оппенгеймер", [Genre.DRAMA, Genre.THRILLER], "Кристофер Нолан", 2023, 8.3),
            ("Барби", [Genre.COMEDY, Genre.ROMANCE], "Грета Гервиг", 2023, 6.9),
        ]

        for title, genres, director, year, rating in movies_data:
            movie_id = self.get_next_movie_id()
            movie = Movie(movie_id, title, genres, director, year, rating)
            self.add_movie(movie)