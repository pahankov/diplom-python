from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from posts.models import Post, Comment, Like
from django.utils import timezone
import random
from datetime import timedelta
from PIL import Image
import os
from django.conf import settings
import uuid
from faker import Faker
from django.db import connection

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Заполняет базу данных уникальными тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            help='Number of test users to create',
            default=30,
        )
        parser.add_argument(
            '--posts',
            type=int,
            help='Number of test posts to create',
            default=150,
        )
        parser.add_argument(
            '--likes',
            type=int,
            help='Number of test likes to create',
            default=500,
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )

    def create_test_image(self, width=800, height=600, idx=0):
        media_dir = os.path.join(settings.MEDIA_ROOT, 'posts')
        os.makedirs(media_dir, exist_ok=True)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        filename = f'test_image_{idx}_{uuid.uuid4()}.jpg'
        filepath = os.path.join(media_dir, filename)
        image = Image.new('RGB', (width, height), color)
        image.save(filepath, 'JPEG')
        return f'posts/{filename}'

    def handle(self, *args, **kwargs):
        clear_data = kwargs['clear'] # Получаем значение аргумента --clear

        # Удаляем старые данные, только если указан флаг --clear
        if clear_data:
            self.stdout.write('Удаление существующих данных...')
            Like.objects.all().delete()
            Comment.objects.all().delete()
            Post.objects.all().delete()
            User.objects.exclude(is_superuser=True).delete() # Осторожно с удалением пользователей!

            # Сброс последовательности ID для модели Post в PostgreSQL
            with connection.cursor() as cursor:
                # Имя последовательности обычно apps_modelname_id_seq
                cursor.execute("ALTER SEQUENCE posts_post_id_seq RESTART WITH 1;")
            self.stdout.write('Последовательность ID для Post сброшена.')

        male_first_names = ['Александр', 'Алексей', 'Андрей', 'Артем', 'Владимир', 'Дмитрий', 'Евгений', 'Иван', 'Максим', 'Михаил', 'Николай', 'Сергей', 'Павел', 'Роман', 'Степан']
        female_first_names = ['Анна', 'Елена', 'Мария', 'Наталья', 'Ольга', 'Татьяна', 'Юлия', 'Ирина', 'Екатерина', 'Анастасия', 'Дарья', 'Ксения', 'Алиса', 'Полина', 'София']
        male_last_names = ['Иванов', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев', 'Петров', 'Соколов', 'Михайлов', 'Новиков', 'Федоров', 'Морозов', 'Волков', 'Алексеев', 'Лебедев', 'Семенов']
        female_last_names = ['Иванова', 'Смирнова', 'Кузнецова', 'Попова', 'Васильева', 'Петрова', 'Соколова', 'Михайлова', 'Новикова', 'Федорова', 'Морозова', 'Волкова', 'Алексеева', 'Лебедева', 'Семенова']

        # Создаем уникальных пользователей
        users = []
        for i in range(15):
            username = f"{male_first_names[i].lower()}_{male_last_names[i].lower()}"
            user = User.objects.create_user(
                username=username,
                password=f'password{i+1}',
                email=f'{username}@example.com',
                first_name=male_first_names[i],
                last_name=male_last_names[i]
            )
            users.append(user)
            self.stdout.write(f'Создан пользователь {user.username}')
        for i in range(15):
            username = f"{female_first_names[i].lower()}_{female_last_names[i].lower()}"
            user = User.objects.create_user(
                username=username,
                password=f'password{i+16}',
                email=f'{username}@example.com',
                first_name=female_first_names[i],
                last_name=female_last_names[i]
            )
            users.append(user)
            self.stdout.write(f'Создан пользователь {user.username}')

        # Уникальные тексты для постов
        post_texts = [
            f"Уникальный пост номер {i+1}: {txt}" for i, txt in enumerate([
                "Отличный день для прогулки! ☀️",
                "Мой новый проект наконец-то запущен! 🚀",
                "Красивый закат сегодня... 🌅",
                "Вкусный ужин в любимом ресторане 🍽️",
                "Удачная тренировка сегодня 💪",
                "Новая книга оказалась очень интересной 📚",
                "Путешествие начинается! ✈️",
                "Мой любимый город выглядит особенно красиво сегодня 🌆",
                "Удалось поймать отличный кадр 📸",
                "Встреча с друзьями после долгой разлуки 👥",
                "Новый рецепт оказался просто отличным! 👨‍🍳",
                "Утренняя пробежка заряжает энергией на весь день 🏃‍♂️",
                "Мой сад в полном цвету 🌸",
                "Новый альбом любимой группы просто огонь! 🎵",
                "Удачный день для шопинга 🛍️",
                "Пробую новый стиль фотографии.",
                "Сегодня был насыщенный день!",
                "Люблю такие вечера у костра.",
                "Поймал момент счастья!",
                "Вдохновляюсь природой каждый день.",
                "Маленькие радости делают жизнь ярче.",
                "Экспериментирую с новыми рецептами.",
                "Побывал в новом месте — впечатления незабываемые!",
                "Делюсь хорошим настроением!",
                "Сегодня был день открытий!",
                "Поймал закат на берегу моря.",
                "Вдохновляюсь музыкой и творчеством.",
                "Провел день с семьей — это бесценно.",
                "Пробую себя в новом хобби.",
                "Сегодня был день для себя!",
                "Удивительный рассвет сегодня! 🌅",
                "Новый рецепт пасты — просто объедение! 🍝",
                "Утренняя йога заряжает энергией! 🧘‍♀️",
                "Поймал редкий момент в природе! 🦋",
                "Встреча с друзьями в любимом кафе! ☕",
                "Новый проект в разработке! 💻",
                "Вечерняя прогулка по городу 🌆",
                "Пробую себя в макросъемке 📸",
                "Вдохновляющий закат над морем 🌊",
                "Новый рецепт десерта — пальчики оближешь! 🍰",
                "Утренний кофе с книгой — лучший старт дня! 📚",
                "Поймал редкий кадр с птицами! 🦅",
                "Вечерняя пробежка по парку 🏃‍♂️",
                "Новый альбом в плейлисте 🎵",
                "Встреча рассвета на пляже 🌅"
            ])
        ]
        # Если нужно больше постов, добавим уникальные
        while len(post_texts) < 75:
            post_texts.append(f"Уникальный автосгенерированный пост #{len(post_texts)+1}")

        # Создаем посты с уникальным текстом и изображением
        posts = []
        for i in range(150):
            created_at = timezone.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23), minutes=random.randint(0, 59))
            image_path = self.create_test_image(idx=i)
            post = Post.objects.create(
                author=users[i % len(users)],
                text=fake.paragraph(nb_sentences=random.randint(3, 10)),
                image=image_path,
                created_at=created_at
            )
            posts.append(post)
            self.stdout.write(f'Создана публикация {post.id}')

        # Уникальные тексты для комментариев
        comment_texts = [
            f"Комментарий #{i+1}: {txt}" for i, txt in enumerate([
                "Отличная публикация! 👍",
                "Согласен с тобой полностью!",
                "Красивые фотографии! 📸",
                "Спасибо за интересный пост!",
                "Очень вдохновляюще! ✨",
                "Поделись подробностями?",
                "Где это было сделано?",
                "Как тебе удалось это сфотографировать?",
                "Поздравляю с успехом! 🎉",
                "Жду продолжения!",
                "Отличная идея! 💡",
                "Спасибо за рекомендацию!",
                "Очень интересно! 🤔",
                "Классный кадр! 📷",
                "Поделись рецептом? 👨‍🍳",
                "Вдохновляющий пример!",
                "Супер!",
                "Это просто вау!",
                "Очень круто!",
                "Здорово придумано!",
                "Беру на заметку!",
                "Спасибо за мотивацию!",
                "Потрясающе!",
                "Очень понравилось!",
                "Супер идея!",
                "Классный пост! 🌟",
                "Отличное фото! 📸",
                "Спасибо за вдохновение! ✨",
                "Очень интересная мысль! 💭",
                "Поделись опытом? 🤔",
                "Красивый момент! 🌅",
                "Отличная идея! 💡",
                "Спасибо за рекомендацию! 👍",
                "Очень полезно! 📚",
                "Классный кадр! 📷",
                "Великолепный снимок! 📸",
                "Как тебе удалось поймать этот момент? 🤔",
                "Поделись настройками камеры? 📷",
                "Очень атмосферно! ✨",
                "Спасибо за позитив! 😊",
                "Вдохновляющий пост! 💫",
                "Красивые цвета! 🎨",
                "Отличная композиция! 📐",
                "Поделись секретом успеха? 🤫",
                "Очень душевно! 💖",
                "Классная идея для фото! 📸",
                "Спасибо за эмоции! 😍",
                "Великолепный ракурс! 📷",
                "Очень стильно! 👌",
                "Поделись планами? 📝"
            ])
        ]
        while len(comment_texts) < 100:
            comment_texts.append(f"Уникальный автосгенерированный комментарий #{len(comment_texts)+1}")

        # Создаем уникальные комментарии к разным постам
        used_post_comment_pairs = set()
        for i in range(300):
            # Гарантируем уникальность пары (пост, автор)
            while True:
                post = random.choice(posts)
                author = random.choice(users)
                pair = (post.id, author.id)
                if pair not in used_post_comment_pairs:
                    used_post_comment_pairs.add(pair)
                    break
            comment_time = post.created_at + timedelta(hours=random.randint(1, 24), minutes=random.randint(0, 59))
            Comment.objects.create(
                post=post,
                author=author,
                text=fake.text(max_nb_chars=random.randint(30, 200)),
                created_at=fake.date_time_between(start_date=post.created_at, end_date='now')
            )
            self.stdout.write(f'Создан комментарий {i+1}')

        # Лайки (оставим случайными, но без дублей)
        used_likes = set()
        for i in range(500):
            post = random.choice(posts)
            user = random.choice(users)
            like_time = post.created_at + timedelta(minutes=random.randint(1, 60))
            key = (post.id, user.id)
            if key not in used_likes:
                Like.objects.create(
                    post=post,
                    user=user,
                    created_at=like_time
                )
                used_likes.add(key)
                self.stdout.write(f'Создан лайк {i+1}')

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена уникальными данными!')) 