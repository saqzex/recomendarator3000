from enum import Enum
from abc import ABC, abstractclassmethod
from typing import List, Dict, Optional
import json
import os


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
        self._watched_movies: Dict[int, float] = {} #словарь из id фильма и оценки
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

    def __init__(self, filename="data.json"):
        self.filename = filename
        self._movies: Dict[int, Movie] = {}
        self._users: Dict[int, User] = {}
        self._next_movie_id = 1
        self._next_user_id = 1

    #загружаем данные если файл существует
        if os.path.exists(self.filename):
            self.load_from_file()
        else:
            self.load_test_data()
            self.save_to_file()

    #сохранение пользователя
    def save_to_file(self):
        data = {
            "users": {},
        }

        for user_id, user in self._users.items():
            data["users"][user_id] = {
                "name": user.name,
                "password": user._password,
                "watched": user.watched_movies,
                "preferred_genres": [g.value for g in user.preferred_genres],
            }

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    #загрузка
    def load_from_file(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.load_test_data()  # фильмы всегда загружаем одинаково

        for user_id, u in data["users"].items():
            user = User(int(user_id), u["name"], u["password"])
            # восстановление оценок
            for movie_id, rating in u["watched"].items():
                user.add_rating(int(movie_id), rating)
            # восстановление жанров
            genres = []
            for g in u["preferred_genres"]:
                for genre in Genre:
                    if genre.value == g:
                        genres.append(genre)
            user.set_preferred_genres(genres)

            self._users[user.user_id] = user

        #изменяем следующий ID
        self._next_user_id = max(self._users.keys()) + 1 if self._users else 1


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


#- Создать абстрактный базовый класс для стратегий рекомендаций
class RecommendationStrategy(ABC):
    def __init__(self, data_manager: DataManager):
        self._data_manager = data_manager

    #@abstractclassmethod
    @classmethod
    def get_reccomendations(self, user:User, min_rating: float = 0.0, min_year: int = 0, max_results:int = 10):
        pass


# На основе жанров - рекомендует фильмы любимых жанров пользователя
class GenreBasedStrategy(RecommendationStrategy):
    def get_recommendations(self, user: User, min_rating: float = 0.0,min_year: int = 0, max_results: int = 10):
        
        reccomendations = []
        watched_ids = set(user.watched_movies.keys())

        preffered_genres = user.preferred_genres
        if not preffered_genres: #угадывает любимые жанры пользователя по уже просмотренным фильмам
            genre_counts = {} #создаётся словарь: жанр - сколько раз он встретился.
            
            for movie_id in watched_ids:
                movie = self._data_manager.get_movie(movie_id)
                if not movie:
                    continue

                for genre in genre_counts:
                    if genre in genre_counts:
                        genre_counts[genre] += 1
                    else:
                        genre_counts = 1 #тоесть если фильм с таким жанром еще не встречался он становится 1

            if genre_counts: #берем 3 самых частых жанра
                sorted_genres = sorted(genre_counts.items(), key = lambda item: item[1], reverse= True) #reverse = True сортировка по убыванию
                preffered_genres = [genre for genre, count in sorted_genres[:3]]

        for movie in self._data_manager.get_all_movies():
            if movie.movie_id not in watched_ids:
                if movie.rating >= min_rating and movie.year > min_year:
                    for genre in preffered_genres:
                        if genre in movie.genres:
                            reccomendations.append(movie)
                            break

        reccomendations.sort(key = lambda x: x.rating)
        return reccomendations[:max_results]
    

class RatingBasedStrategy(RecommendationStrategy):
    
    def get_recommendations(self, user: User, min_rating: float = 0.0, min_year: int = 0, max_results: int = 10) :
        watched_ids = set(user.watched_movies.keys())
        recommendations = []

        for movie in self._data_manager.get_all_movies():
            if movie.movie_id not in watched_ids:
                if movie.rating >= min_rating and movie.year >= min_year:
                    recommendations.append(movie)

        recommendations.sort(key = lambda x: x.rating)
        return recommendations[:max_results]
    
class SimilarUserStrategy(RecommendationStrategy):
    def _calculate_similarity(self, user1: User, user2:User):
        watched1 = set(user1.watched_movies.keys()) # получаем id
        watched2 = set(user2.watched_movies.keys())
        common = watched1 & watched2 

        if not common:
            return 0.0
        
        total_diff = 0.0 #сумма разниц
        for movie_id in common:
            diff = abs(user1.watched_movies[movie_id] - user2.watched_movies[movie_id]) #разница в оценке фильма
            total_diff += diff

        avg_diff = total_diff/ len(common) #если вкусы почти совпадают то число близко к 0, если сильно расходятся то ближе к 10
        #чтобы из макс 10 сделать 0 или 1. делим на 10. (avg_diff/10) - насколько они разные, нам надо наоборот, поэтому вычитаем из 1
        return max(0.0, 1.0 - (avg_diff/10)) #чем ближе к 1 тем более похожи
    
    def get_recommendations(self, user: User, min_rating: float = 0.0, min_year: int = 0, max_results : int = 10):

        watched_ids = set(user.watched_movies.keys())
        movie_scores: Dict[int, float] = {}

        for other_user in self._data_manager.get_all_users():
            if other_user.user_id == user.user_id:
                continue

            similarity = self._calculate_similarity(user, other_user)
            if similarity <  0.3:
                continue # слишком не похожий пользователь

            for movie_id, rating in other_user.watched_movies.items():
                if movie_id not in watched_ids:
                    score = similarity * rating
                    #складываются все score для каждого фильма от разных пользователе
                    movie_scores[movie_id] = movie_scores.get(movie_id, 0.0) + score

        sorted_movies = sorted(movie_scores.items(), key = lambda x: x[1], reverse = True)  

        recommendations = []                  
        for movie_id, score in sorted_movies:
            movie = self._data_manager.get_movie(movie_id)
            if movie and movie.rating >= min_rating and movie.year >= min_year:
                recommendations.append(movie)
                if len(recommendations) >= max_results:
                    break

        return recommendations


        
    
        
        
# Блок 3: Расширение системы и интерфейс
class MovieRecommendationApp:

    def __init__(self):
        self.data_manager = DataManager()
        self.data_manager.load_test_data()
        self.current_user: Optional[User] = None

        self.strategies = {
            1: GenreBasedStrategy(self.data_manager),
            2: RatingBasedStrategy(self.data_manager),
            3: SimilarUserStrategy(self.data_manager)
        }

# Главное меню
    def show_main_menu(self):                                               
        print("\n" + "="*50)
        print("РЕКОМЕНДАТЕЛЬНАЯ СИСТЕМА ФИЛЬМОВ")
        print("="*50)
        if self.current_user:
            print(f"Текущий пользователь: {self.current_user.name}")
        print("\n1. Регистрация")
        print("2. Вход")
        print("3. Просмотр фильмов")
        print("4. Оценить фильм")
        print("5. Получить рекомендации")
        print("6. Настроить предпочтения")
        print("7. Выход")
        print("="*50)

# Регистрация
    def register_user(self):
        print("\n" + "="*50)
        print("РЕГИСТРАЦИЯ")
        print("="*50)

        name = input("Введите имя: ").strip()
        if not name:
            print("Имя не может быть пустым!")
            return

        if self.data_manager.get_user_by_name(name):
            print("Пользователь с таким именем уже существует!")
            return

        password = input("Введите пароль: ").strip()
        if not password:
            print("Пароль не может быть пустым!")
            return

        user_id = self.data_manager.get_next_user_id()
        user = User(user_id, name, password)
        self.data_manager.add_user(user)
        self.current_user = user

        print(f"\nПользователь '{name}' успешно зарегистрирован!")

# Вход
    def login_user(self):
        print("\n" + "="*50)
        print("ВХОД")
        print("="*50)

        name = input("Введите имя: ").strip()
        password = input("Введите пароль: ").strip()

        user = self.data_manager.authenticate(name, password)
        if user:
            self.current_user = user
            print(f"\nДобро пожаловать, {user.name}!")
        else:
            print("\nОшибка: неправильное имя или пароль!")

 # Просмотр фильмов           
    def show_movies(self):
        movies = self.data_manager.get_all_movies()
        print(f"\nВсего фильмов: {len(movies)}")
        print("-"*50)
        for movie in movies:
            print(f"{movie.movie_id}. {movie}")

# Оценка фильма
    def rate_movie(self):
        if not self.current_user:
            print("Сначала войдите в систему!")
            return

        self.show_movies()

        try:
            movie_id = int(input("\nВведите ID фильма: "))
            movie = self.data_manager.get_movie(movie_id)
            if not movie:
                print("Фильм не найден!")
                return

            rating = float(input("Введите оценку (0-10): "))
            self.current_user.add_rating(movie_id, rating)
            print(f"Вы оценили фильм '{movie.title}' на {rating} баллов!")
        except ValueError:
            print("Ошибка ввода!")

# Получение рекомендаций
    def get_recommendations(self):
        if not self.current_user:
            print("Сначала войдите!")
            return

        print("\nВыберите стратегию:")
        print("1. По жанрам")
        print("2. По рейтингу")
        print("3. По похожим пользователям")

        try:
            strategy_num = int(input("Ваш выбор: "))
            if strategy_num not in self.strategies:
                print("Неверный выбор!")
                return

            min_rating = float(input("Мин. рейтинг (по умолч. 0): ") or 0)
            min_year = int(input("Мин. год (по умолч. 0): ") or 0)
            max_results = int(input("Макс. результатов (по умолч. 10): ") or 10)

            strategy = self.strategies[strategy_num]
            recommendations = strategy.get_recommendations(
                self.current_user, min_rating, min_year, max_results
            )

            print("\nРекомендации:")
            print("-"*50)
            if not recommendations:
                print("Нет подходящих фильмов!")
            else:
                for i, movie in enumerate(recommendations, 1):
                    print(f"{i}. {movie}")

        except ValueError:
            print("Ошибка ввода!")


# Фильтр, препочитаемые жанры
    def set_preferences(self):
        if not self.current_user:
            print("Сначала войдите!")
            return

        print("\nНастройка предпочтений")
        print("-"*50)

        for i, genre in enumerate(Genre, 1):
            print(f"{i}. {genre.value}")

        try:
            genre_nums = input("\nВведите номера через запятую: ").split(",")
            selected_genres = []

            for num_str in genre_nums:
                num = int(num_str.strip())
                if 1 <= num <= len(Genre):
                    selected_genres.append(list(Genre)[num - 1])

            if selected_genres:
                self.current_user.set_preferred_genres(selected_genres)
                print("Предпочтения обновлены!")
            else:
                print("Вы не выбрали жанры!")

        except ValueError:
            print("Ошибка ввода!")


    def run(self):
        while True:
            self.show_main_menu()
            choice = input("\nВыберите действие: ").strip()

            if choice == "1":
                self.register_user()
            elif choice == "2":
                self.login_user()
            elif choice == "3":
                self.show_movies()
            elif choice == "4":
                self.rate_movie()
            elif choice == "5":
                self.get_recommendations()
            elif choice == "6":
                self.set_preferences()
            elif choice == "7":
                print("До свидания!")
                break
            else:
                print("Неверный выбор!")


if __name__ == "__main__":
    app = MovieRecommendationApp()
    app.run()         