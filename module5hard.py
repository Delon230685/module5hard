import hashlib
import time

class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = self._hash_password(password)
        self.age = age

    def _hash_password(self, password):
        return int(hashlib.sha256(password.encode()).hexdigest(), 16)

    def __eq__(self, other):
        return isinstance(other, User) and self.nickname == other.nickname

    def __repr__(self):
        return self.nickname


class Video:
    def __init__(self, title, duration, adult_mode=False, time_now=0):
        self.title = title  # заголовок, строка
        self.duration = duration  # продолжительность, секунды
        self.time_now = time_now  # секунда остановки
        self.adult_mode = adult_mode  # ограничение по возрасту

    def __eq__(self, other):
        return isinstance(other, Video) and self.title == other.title

    def __repr__(self):
        return self.title


class UrTube:
    def __init__(self):
        self.users = []
        self.videos = []  #список объектов
        self.current_user = None  #текущий пользователь

    def log_in(self, nickname, password):
        hashed_password = int(hashlib.sha256(password.encode()).hexdigest(), 16)
        for user in self.users:
            if user.nickname == nickname and user.password == hashed_password:
                self.current_user = user
                return
        print('Неверный логин или пароль')

    def register(self, nickname, password, age):
        new_user = User(nickname, password, age)
        if new_user in self.users:
            print(f'Пользователь {nickname} уже существует')
        else:
            self.users.append(new_user)
            self.current_user = new_user

    def log_out(self):
        self.current_user = None

    def add(self, *videos):
        for video in videos:
            if video not in self.videos:
                self.videos.append(video)

    def get_videos(self, search_word):
        search_word = search_word.lower()
        result = []
        for video in self.videos:
            if search_word in video.title.lower():
                result.append(video.title)
        return result

    def watch_video(self, title):
        if not self.current_user:
            print('Войдите в аккаунт, чтобы смотреть видео')
            return

        for video in self.videos:
            if video.title == title:
                if video.adult_mode and self.current_user.age < 18:
                    print('Вам нет 18 лет, пожалуйста покиньте страницу')
                    return

                for second in range(video.time_now + 1, video.duration + 1):
                    print(second, end=' ', flush=True)
                    video.time_now = second
                    time.sleep(0.5)
                print('Конец видео')
                video.time_now = 0
                return



ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)
#Добавление видео
ur.add(v1, v2)
#Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))
#Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')
#Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)
#Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')
