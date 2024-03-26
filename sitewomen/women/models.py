from tabnanny import verbose
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class PublishedManager(models.Manager):
    
    # Менеджер моделей
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


# Create your models here.
# ORM
class Women(models.Model):
    class Status(models.IntegerChoices):
        # Перечисление
        # Выбор статуса значения is_published
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'
        # Women.Status.choices [(0, 'Черновик'), (1, 'Опубликовано')]
        # Women.Status.labels ['Черновик', 'Опубликовано']
        # Women.Status.values [0, 1]
    
    title = models.CharField(
        max_length=255, 
        verbose_name='Заголовок',
    )
    slug = models.SlugField(
        max_length=255, 
        unique=True, 
        db_index=True,
        verbose_name='Slug', 
        validators=[
            MinLengthValidator(5, message='Минимум 5 символов'),
            MaxLengthValidator(100, message='Максимум 100 символов'),
        ],
    )
    # фото 
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        default=None,
        blank=True,
        null=True,
        verbose_name='Фото'
    )
    content = models.TextField(
        blank=True, 
        verbose_name='Текст статьи',
    )
    time_create = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Время создания',
    )
    time_update = models.DateTimeField(
        auto_now=True, 
        verbose_name="Время изменения",
    )
    # choices=tuple(map(lambda x: (bool(x[0]), x[1]) костыль для преобразования из choices 0, 1 в булевое значение
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.PUBLISHED, 
        verbose_name="Статус",
    )
    
    # связь таблицы с таблицей category Many_to_one
    cat = models.ForeignKey(
        'Category', 
        on_delete=models.PROTECT, 
        related_name='posts', 
        verbose_name="Категория",
    ) 
    # In [3]: Category.objects.get(pk=1).posts.all()
    
    # теги постов Many_to_Many
    tags = models.ManyToManyField(
        'TagPost', 
        blank=True, 
        related_name='tags', 
        verbose_name="Теги",
    )
    
    # связь с таблицей husband One_to_One
    husband = models.OneToOneField(
        'Husband',
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='wuman', 
        verbose_name="Муж",
    )
    
    # поле автора
    author = models.ForeignKey(
        get_user_model(), 
        on_delete=models.SET_NULL, 
        related_name='posts',
        null=True,
        default=None,
    )
    
    
    #экземпляр менеджера моделей
    published = PublishedManager()
    #нужно переопределить менеджер objects, 
    # так как при создании собственного менеджера objects перестает работать
    objects = models.Manager()
    
    
    def __str__(self):
        return self.title

    # Класс Meta определяет порядок и индексы модели в Python.
    class Meta:
        verbose_name = 'Женщины'
        verbose_name_plural = 'Жещины'
        # Сортировка
        ordering =[
            '-time_create'
        ]
        indexes = [
            models.Index(fields=['-time_create'])
        ]
    
    def get_absolute_url(self):
        #возращает url адрес со слагом
        return reverse("post", kwargs={"post_slug": self.slug})
    
    # def save(self, *args, **kwargs):
    #     # автоматическое создание слага
    #     self.slug = slugify(unidecode(str(self.title)))
    #     super().save(*args, **kwargs)



class Category(models.Model):
    # модель связной таблицы для категорий
    name = models.CharField(
        max_length=100,
        db_index=True, 
        verbose_name='Категория',
    )
    slug = models.SlugField(
        max_length=255, 
        unique=True, 
        db_index=True,
    )
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("category", kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    # таблица с тегами постов
    tag = models.CharField(
        max_length=100, 
        db_index=True,
    )
    slug = models.SlugField(
        max_length=255, 
        unique=True, 
        db_index=True,
    )
    
    def __str__(self):
        return self.tag
    
    def get_absolute_url(self):
        return reverse("tag", kwargs={"tag_slug": self.slug})


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    
    def __str__(self):
        return self.name


class UploadFiles(models.Model):
    # модель для загрузки файлов
    file = models.FileField(upload_to='uploads_model')


# класс Q 
# from django.db.models import Q

# Women.objects.filter(pk__lt=5, cat_id=2) # SQL AND
#  WHERE ("women_women"."cat_id" = 2 AND "women_women"."id" < 5)
# Women.objects.filter(Q(pk__lt=5) | Q(cat_id=2)) # SQL OR
#  WHERE ("women_women"."id" < 5 OR "women_women"."cat_id" = 2)
#  Women.objects.filter(Q(pk__lt=5) & Q(cat_id=2)) # SQL AND
#   WHERE ("women_women"."id" < 5 AND "women_women"."cat_id" = 2)
# Women.objects.filter(~Q(pk__lt=5) & Q(cat_id=2)) # SQL NOT=~
#  WHERE (NOT ("women_women"."id" < 5) AND "women_women"."cat_id" = 2)
# Women.objects.filter(~Q(pk__in=[1, 2, 5]) | Q(cat_id=2), title__contains='ра')
#  WHERE ((NOT ("women_women"."id" IN (1, 2, 5)) OR "women_women"."cat_id" = 2) AND "women_women"."title" LIKE '%ра%' ESCAPE '\')


#Создание файла миграции в women.migrations
# python manage.py makemigrations

# python manage.py shell - консоль джанго, похоже на консоль pycharm

# >>> from women.models import Women
# >>> Women(title='Анджелина Джоли', content='Биография Анджелины Джоли')
# <Women: Women object (None)>
# >>> w1 = _
# >>> w1
# <Women: Women object (None)>
# >>> w1.save()
# >>> w1
# <Women: Women object (1)>
# >>> w1.id
# >>> w1.pk - primary key


# >>> from django.db import connection
# >>> connection.queries
# [{'sql': 'INSERT INTO "women_women" ("title", "content", "time_create", "time_update", "is_published") VALUES (\'Анджелина Джоли\', \'Биография Анджелины Джоли\', \'2024-03-15 07:04:02.770419\', \'2024-03-15 07:04:02.771330\', 1) RETURNING "women_women"."id"', 'time': '0.003'}]
# >>> 

# >>> w2 = Women(title='Энн Хэтэуей', content='Биография Энн Хэтэуей')
# >>> w2.save
# <bound method Model.save of <Women: Women object (None)>>
# >>> w2.save()

# >>> w3 = Women()
# >>> w3.title = 'Джулия Робертся'
# >>> w3.content = 'Биография Джулии Робертс'
# >>> w3.save()


# pip install ipython

# pip install django-extensions

# INSTALLED_APPS = (
# ...
# django_extensions',
# )
# python manage.py shell_plus --print-sql  


# In [3]: Women.objects
# Out[3]: <django.db.models.manager.Manager at 0x104606550>

# In [4]: Women.objects.create(title='Ума Турман', content='Биография Умы Турман')
# Women.objects.create(title='Кира Найтли', content='Биография Киры Найтли')

# In [1]: Women.objects.all()
# Execution time: 0.000889s [Database: default]
# <QuerySet [<Women: Анджелина Джоли>, <Women: Энн Хэтэуей>, <Women: Джулия Робертся>, <Women: Екатерина Гусева>, <Women: Ума Турман>, <Women: Кира Найтли>]>


# In [2]: w = Women.objects.all()[0]
# SELECT "women_women"."id",
#        "women_women"."title",
#        "women_women"."content",
#        "women_women"."time_create",
#        "women_women"."time_update",
#        "women_women"."is_published"
#   FROM "women_women"
#  LIMIT 1

# Execution time: 0.000347s [Database: default]

# In [3]: w
# Out[3]: <Women: Анджелина Джоли>

# In [4]: w.title
# Out[4]: 'Анджелина Джоли'

# In [5]: w.content
# Out[5]: 'Биография Анджелины Джоли'

# In [6]: w.pk
# Out[6]: 1

# In [7]: w = Women.objects.all()[:3]
# SQL запрос не добавляется, только после взаимодействий с экземпляром w
# In [8]: w
# Out[8]: SELECT "women_women"."id",
#        "women_women"."title",
#        "women_women"."content",
#        "women_women"."time_create",
#        "women_women"."time_update",
#        "women_women"."is_published"
#   FROM "women_women"
#  LIMIT 3

# Execution time: 0.000309s [Database: default]
# <QuerySet [<Women: Анджелина Джоли>, <Women: Энн Хэтэуей>, <Women: Джулия Робертся>]>

# In [9]: 

# In [9]: ws = Women.objects.all()

# In [10]: for w in ws:
#     ...:     print(w)
#     ...: 
# SELECT "women_women"."id",
#        "women_women"."title",
#        "women_women"."content",
#        "women_women"."time_create",
#        "women_women"."time_update",
#        "women_women"."is_published"
#   FROM "women_women"

# Execution time: 0.002037s [Database: default]
# Анджелина Джоли
# Энн Хэтэуей
# Джулия Робертся
# Екатерина Гусева
# Ума Турман
# Кира Найтли

# Execution time: 0.000155s [Database: default]
# <QuerySet [<Women: Энн Хэтэуей>]>


# Сравение

# In [12]: Women.objects.filter(pk__gt=2)
# Out[12]: SELECT "women_women"."id",
#        "women_women"."title",
#        "women_women"."content",
#        "women_women"."time_create",
#        "women_women"."time_update",
#        "women_women"."is_published"
#   FROM "women_women"
#  WHERE "women_women"."id" > 2
#  LIMIT 21

# Execution time: 0.000122s [Database: default]
# <QuerySet [<Women: Джулия Робертся>, <Women: Екатерина Гусева>, <Women: Ума Турман>, <Women: Кира Найтли>]>


# Включает ли строка LIKE

# In [14]: Women.objects.filter(title__contains='ли')
# Out[14]: SELECT "women_women"."id",
#        "women_women"."title",
#        "women_women"."content",
#        "women_women"."time_create",
#        "women_women"."time_update",
#        "women_women"."is_published"
#   FROM "women_women"
#  WHERE "women_women"."title" LIKE '%ли%' ESCAPE '\'
#  LIMIT 21

# Execution time: 0.000143s [Database: default]
# <QuerySet [<Women: Анджелина Джоли>, <Women: Джулия Робертся>, <Women: Кира Найтли>]>

# In [15]: 
# In [16]: Women.objects.filter(title__icontains='Дж')

# In [19]: Women.objects.filter(pk__in=[2, 5, 11, 12])
# Out[19]: SELECT "women_women"."id",
#        "women_women"."title",
#        "women_women"."content",
#        "women_women"."time_create",
#        "women_women"."time_update",
#        "women_women"."is_published"
#   FROM "women_women"
#  WHERE "women_women"."id" IN (2, 5, 11, 12)
#  LIMIT 21

# Execution time: 0.000205s [Database: default]
# <QuerySet [<Women: Энн Хэтэуей>, <Women: Ума Турман>]>


# In [20]: Women.objects.filter(pk__in=[2, 5, 11, 12], is_published=1)


# NOT
# In [21]: Women.objects.exclude(pk=2)
# Out[21]: SELECT "women_women"."id",
#        "women_women"."title",
#        "women_women"."content",
#        "women_women"."time_create",
#        "women_women"."time_update",
#        "women_women"."is_published"
#   FROM "women_women"
#  WHERE NOT ("women_women"."id" = 2)
#  LIMIT 21

# Execution time: 0.000171s [Database: default]
# <QuerySet [<Women: Анджелина Джоли>, <Women: Джулия Робертся>, <Women: Екатерина Гусева>, <Women: Ума Турман>, <Women: Кира Найтли>]>


# Возвращает только 1 запись
# In [22]: Women.objects.get(pk=2)
# SELECT "women_women"."id",
#        "women_women"."title",
#        "women_women"."content",
#        "women_women"."time_create",
#        "women_women"."time_update",
#        "women_women"."is_published"
#   FROM "women_women"
#  WHERE "women_women"."id" = 2
#  LIMIT 21

# Execution time: 0.000156s [Database: default]
# Out[22]: <Women: Энн Хэтэуей>

# Сортировка

# ORDER BY
# In [1]: Women.objects.all().order_by("title")
# Women.objects.order_by("title")
# Out[1]: SELECT "women_women"."id",
#        "women_women"."title",
#        "women_women"."content",
#        "women_women"."time_create",
#        "women_women"."time_update",
#        "women_women"."is_published"
#   FROM "women_women"
#  ORDER BY "women_women"."title" ASC
#  LIMIT 21

# Execution time: 0.000542s [Database: default]
# <QuerySet [<Women: Анджелина Джоли>, <Women: Джулия Робертся>, <Women: Екатерина Гусева>, <Women: Кира Найтли>, <Women: Ума Турман>, <Women: Энн Хэтэуей>]>




# In [3]: Women.objects.filter(pk__lte=4).order_by('title')
# Out[3]: SELECT "women_women"."id",
#        "women_women"."title",
#        "women_women"."content",
#        "women_women"."time_create",
#        "women_women"."time_update",
#        "women_women"."is_published"
#   FROM "women_women"
#  WHERE "women_women"."id" <= 4
#  ORDER BY "women_women"."title" ASC
#  LIMIT 21

# Execution time: 0.000233s [Database: default]
# <QuerySet [<Women: Анджелина Джоли>, <Women: Джулия Робертся>, <Women: Екатерина Гусева>, <Women: Энн Хэтэуей>]>



# In [4]: Women.objects.filter(pk__lte=4).order_by('-title')
# Out[4]: SELECT "women_women"."id",
#        "women_women"."title",
#        "women_women"."content",
#        "women_women"."time_create",
#        "women_women"."time_update",
#        "women_women"."is_published"
#   FROM "women_women"
#  WHERE "women_women"."id" <= 4
#  ORDER BY "women_women"."title" DESC
#  LIMIT 21

# Execution time: 0.000128s [Database: default]
# <QuerySet [<Women: Энн Хэтэуей>, <Women: Екатерина Гусева>, <Women: Джулия Робертся>, <Women: Анджелина Джоли>]>


# Обновление записей 

# In [2]: wu = Women.objects.get(pk=2)
# SELECT "women_women"."id",
#        "women_women"."title",
#        "women_women"."content",
#        "women_women"."time_create",
#        "women_women"."time_update",
#        "women_women"."is_published"
#   FROM "women_women"
#  WHERE "women_women"."id" = 2
#  LIMIT 21

# Execution time: 0.000152s [Database: default]

# In [3]: wu
# Out[3]: <Women: Энн Хэтэуей>

# In [4]: wu.title = 'Марго Робби'

# In [5]: wu.content = 'Биография Марго Робби'

# In [6]: wu.save()
# UPDATE "women_women"
#    SET "title" = 'Марго Робби',
#        "content" = 'Биография Марго Робби',
#        "time_create" = '2024-03-15 07:09:52.589678',
#        "time_update" = '2024-03-15 10:41:11.514216',
#        "is_published" = 1
#  WHERE "women_women"."id" = 2

#  In [7]: Women.objects.update(is_published=0)
# UPDATE "women_women"
#    SET "is_published" = 0

# Execution time: 0.001353s [Database: default]
# Out[7]: 6

# In [8]: Women.objects.all().filter(pk__lte=4).update(is_published=1)
# UPDATE "women_women"
#    SET "is_published" = 1
#  WHERE "women_women"."id" <= 4

# Execution time: 0.001271s [Database: default]
# Out[8]: 4

#  In [9]: Women.objects.filter(pk__gte=5)
# Out[9]: SELECT "women_women"."id",
#        "women_women"."title",
#        "women_women"."content",
#        "women_women"."time_create",
#        "women_women"."time_update",
#        "women_women"."is_published"
#   FROM "women_women"
#  WHERE "women_women"."id" >= 5
#  ORDER BY "women_women"."time_create" DESC
#  LIMIT 21

# Execution time: 0.000174s [Database: default]
# <QuerySet [<Women: Кира Найтли>, <Women: Ума Турман>]>

# In [10]: wu = _

# In [11]: wu.delete()
# BEGIN

# Execution time: 0.000045s [Database: default]
# DELETE
#   FROM "women_women"
#  WHERE "women_women"."id" >= 5

# Execution time: 0.000406s [Database: default]
# Out[11]: (2, {'women.Women': 2})

# Заполнение поля slug
# In [2]: for w in Women.objects.all():
#    ...:     w.slug = 'slug-'+str(w.pk)
#    ...:     w.save()


# In [15]: c.women_set
# Out[15]: <django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager.<locals>.RelatedManager at 0x110426d90>


# Менеджер записей
# In [16]: c.women_set.all()
# Out[16]: SELECT "women_women"."id",
#        "women_women"."title",
#        "women_women"."slug",
#        "women_women"."content",
#        "women_women"."time_create",
#        "women_women"."time_update",
#        "women_women"."is_published",
#        "women_women"."cat_id"
#   FROM "women_women"
#  WHERE ("women_women"."is_published" AND "women_women"."cat_id" = 1)
#  ORDER BY "women_women"."time_create" DESC
#  LIMIT 21

# Execution time: 0.001400s [Database: default]
# <QuerySet [<Women: Дженифер Лоуренс>, <Women: Джулия Робертся>, <Women: Марго Робби>, <Women: Анджелина Джоли>]>


# In [8]: Women.objects.filter(cat_id__in=[1, 2])
# Out[8]: SELECT "women_women"."id",
#        "women_women"."title",
#        "women_women"."slug",
#        "women_women"."content",
#        "women_women"."time_create",
#        "women_women"."time_update",
#        "women_women"."is_published",
#        "women_women"."cat_id"
#   FROM "women_women"
#  WHERE "women_women"."cat_id" IN (1, 2)
#  ORDER BY "women_women"."time_create" DESC
#  LIMIT 21

# Execution time: 0.000222s [Database: default]
# <QuerySet [<Women: Дженифер Лоуренс>, <Women: Джулия Робертся>, <Women: Марго Робби>, <Women: Анджелина Джоли>]>


# In [9]: cats = Category.objects.all()

# In [10]: Women.objects.filter(cat__in=cats)

# In [11]: Women.objects.filter(cat__slug='aktrisy')
# Out[11]: SELECT "women_women"."id",
#        "women_women"."title",
#        "women_women"."slug",
#        "women_women"."content",
#        "women_women"."time_create",
#        "women_women"."time_update",
#        "women_women"."is_published",
#        "women_women"."cat_id"
#   FROM "women_women"
#  INNER JOIN "women_category"
#     ON ("women_women"."cat_id" = "women_category"."id")
#  WHERE "women_category"."slug" = 'aktrisy'
#  ORDER BY "women_women"."time_create" DESC
#  LIMIT 21


# In [14]: Category.objects.filter(posts__title__contains='ли')
# Out[14]: SELECT "women_category"."id",
#        "women_category"."name",
#        "women_category"."slug"
#   FROM "women_category"
#  INNER JOIN "women_women"
#     ON ("women_category"."id" = "women_women"."cat_id")
#  WHERE "women_women"."title" LIKE '%ли%' ESCAPE '\'
#  LIMIT 21

# Execution time: 0.000224s [Database: default]
# <QuerySet [<Category: Актрисы>, <Category: Актрисы>]>



# Добавление и присваивание тегов в связи таблиц Many_to_Many
# In [6]: TagPost.objects.create(tag='Оскар', slug='oskar')
# Out[6]: <TagPost: Оскар>

# In [7]: TagPost.objects.create(tag='Олимпиада', slug='olimpiada')
# Out[7]: <TagPost: Олимпиада>

# In [8]: TagPost.objects.create(tag='Высокие', slug='visokie')
# Out[8]: <TagPost: Высокие>

# In [9]: TagPost.objects.create(tag='Средние', slug='srednie')
# Out[9]: <TagPost: Средние>

# In [10]: TagPost.objects.create(tag='Низкие', slug='niskie')
# Out[10]: <TagPost: Низкие>

# In [11]: a = Women.objects.get(pk=1)

# In [12]: a
# Out[12]: <Women: Анджелина Джоли>

# In [13]: tag_br = TagPost.objects.all()[1]

# In [14]: tag_br
# Out[14]: <TagPost: Брюнетки>

# In [15]: tag_o, tag_v = TagPost.objects.filter(id__in=[3, 5])

# In [16]: tag_o
# Out[16]: <TagPost: Оскар>

# In [17]: tag_v
# Out[17]: <TagPost: Высокие>

# In [18]: a.tags
# Out[18]: <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager at 0x11418e190>

# In [19]: a.tags.set([tag_br, tag_o, tag_v])

# In [20]: a.tags.remove(tag_o)

# In [21]: a.tags.add(tag_br)

# In [22]: a.tags.all()
# Out[22]: <QuerySet [<TagPost: Брюнетки>, <TagPost: Высокие>]>

# In [23]: tag_br.tags.all()
# Out[23]: <QuerySet [<Women: Анджелина Джоли>]>



# Связь таблиц One_to_One на примере Husband
# In [1]: h1 = Husband.objects.create(name='Брэд Питт', age=59)

# In [2]: h2 = Husband.objects.create(name='Том Акерли', age=31)

# In [3]: h3 = Husband.objects.create(name='Дэниэл Модер')

# In [4]: h4 = Husband.objects.create(name='Кук Марони')

# In [5]: w1 = Women.objects.get(pk=1)

# In [6]: w1
# Out[6]: <Women: Анджелина Джоли>

# In [7]: w1.husband

# In [8]: w1.husband = h1

# In [9]: w1.save()

# In [10]: w1.husband
# Out[10]: <Husband: Брэд Питт>

# In [11]: h1.wuman
# Out[11]: <Women: Анджелина Джоли>

# Обратное присваивание
# In [12]: w2 = Women.objects.get(pk=2)

# In [13]: h2
# Out[13]: <Husband: Том Акерли>

# In [14]: h2.wuman = w2

# In [15]: w2.husband
# Out[15]: <Husband: Том Акерли>

# In [16]: w2.save()

# In [17]: h2.wuman
# Out[17]: <Women: Марго Робби>


# In [18]: w1.husband.name
# Out[18]: 'Брэд Питт'

# In [19]: w1.husband.age
# Out[19]: 59

# In [20]: w1.husband.age = 30

# In [21]: w1.husband.save()
