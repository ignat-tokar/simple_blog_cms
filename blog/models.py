# Импорт модуля для работы с моделями
from django.db import models
# Импорт функции для работы со ссылками
from django.shortcuts import reverse
# Импорт функции для создания slug
from django.utils.text import slugify
# Импорт фунции для работы со временем
from time import time


# Генерирование нового slug
def gen_slug(s):
	new_slug = slugify(s, allow_unicode=True)
	# Уникализация slug путем добавления данных, которые возвращает time()
	return new_slug + "-" + str(int(time()))


# Класс модели поста
class Post(models.Model):
	# Определение полей таблицы в базе данных и установка их атрибутов
	title = models.CharField(max_length = 150, db_index = True)
	slug = models.SlugField(max_length = 150, unique = True)
	text = models.TextField(blank = True, db_index = True)
	tags = models.ManyToManyField('Tag', blank = True, related_name = 'posts')
	date = models.DateTimeField(auto_now_add = True)

	# Функция для получения ссылки на объект модели
	def get_absolute_url(self):
		return reverse('detail_post_url', kwargs={'slug': self.slug})

	# Функция для получения ссылки на редактирование объекта модели
	def get_edit_url(self):
		return reverse('edit_post_url', kwargs={'slug': self.slug})

	# Функция для получения ссылки на удаление объекта модели
	def get_delete_url(self):
		return reverse('delete_post_url', kwargs={'slug': self.slug})

	# Коррекция процесса сохранения объекта для добавления поля slug на 
	# основе поля title
	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self.title)
		super().save(*args, **kwargs)

	# Определение способа сортировки в базе данных - по дате в обратном
	# порядке
	class Meta:
		ordering = ['-date']


# Класс модели для тэга
class Tag(models.Model):
	# Определение полей таблицы в базе данных и установка их атрибутов
	title = models.CharField(max_length = 50, db_index = True)
	slug = models.SlugField(max_length = 50, unique = True)

	# Функция для получения ссылки на объект модели
	def get_absolute_url(self):
		return reverse('detail_tag_url', kwargs={'slug': self.slug })

	# Функция для получения ссылки на редактирование объекта модели
	def get_edit_url(self):
		return reverse('edit_tag_url', kwargs={'slug': self.slug })

	# Функиця для получения ссылки на удаление объекта модели
	def get_delete_url(self):
		return reverse('delete_tag_url', kwargs={'slug': self.slug })

	# Коррекция процесса сохранения объекта для добавления поля slug на 
	# основе поля title	
	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self.title)
		super().save(*args, **kwargs)

	# Вместа вывода индекса объекта в памяти - выводиться его поле title
	def __str__(self):
		return self.title
		
	# Определение способа сортировки объектов в базе данных - 
	# по названию в алфавитном порядке
	class Meta:
		ordering = ['title']
