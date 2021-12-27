# Импорт функции для отображения веб-страницы
from django.shortcuts import render
# Импорт функции для извлечения объектов их базы данных
from django.shortcuts import get_object_or_404
# Импорт функции для работы с редиректом
from django.shortcuts import redirect
# Импорт класса для работы с видами
from django.views.generic import View
# Импорт класса для упрощения добавления пагинации
from django.core.paginator import Paginator
# Импорт класса для упрощения процесса поиска по сайту
from django.db.models import Q

# Импортирование моделей и форм текущего проекта
from .models import Post, Tag
from .forms import PostForm, TagForm


# Функция для вывода всех постов
def all_post (request):
	# Обработка запроса строки поиска
	search_query = request.GET.get('search', '')
	# Если в запросе есть данные
	if search_query:
		# Производиться поиск по полях title или text
		posts = Post.objects.filter(Q(title__icontains=search_query) | Q(text__icontains=search_query))
	else:
		# Если совпадения не обнаружены возвращаються все посты
		posts = Post.objects.all()
	# Установка данных для пагинации (по три поста на странице)
	paginator = Paginator(posts, 3)
	# Проверяеться GET-запрос и наличие в нем данных о странице
	# (по умолчанию - 1)
	page_number = request.GET.get('page', 1)
	# Получение текущей страницы из пагинатора
	page = paginator.get_page(page_number)
	# Проверка есть ли посты на других страницах для отображени (или нет)
	# строки с номерами страниц
	is_paginated = page.has_other_pages()
	prev_url = None
	next_url = None
	# Проверка - есть ли предыдущая страницы
	if page.has_previous():
		# Установка номера для ссылки на предыдущую страницу
		prev_url = "?page={}".format(page.previous_page_number())
	# Проверка - есть ли следующая страница
	if page.has_next():
		# Установка номера для ссылки на следующую страницу
		next_url = "?page={}".format(page.next_page_number())
	# Формирования словаря для отправки на веб-страницу которая будет
	# отображаться
	context = {
		'page': page,
		'is_paginated': is_paginated,
		'prev_url': prev_url,
		'next_url': next_url
	}
	# Отображение страницы
	return render(request, 'all_post.html', context)


# Класс для обработки запроса на вывод данных конкретного поста
class PostDetail(View):
	def get(self, request, slug):
		# Получение поста из базы данных по полю slug
		post = get_object_or_404(Post, slug__iexact=slug)
		# Отображение страницы
		return render(request, 'detail_post.html', context={'post': post})


# Класс для обработки get- и post-запросов страницы создания поста
class PostCreate(View):

	def get(self, request):
		# Создание формы для модели поста
		form = PostForm()
		# Отображение страницы и передача созданной формы
		return render(request, 'create_post.html', context={'form': form})

	def post(self, request):
		# Получение связанной формы
		bound_form = PostForm(request.POST)
		# Проверка связанной формы на валидность
		if bound_form.is_valid():
			# Сохранение нового поста
			new_post = bound_form.save()
			# Редирект на страницу только что созданного поста
			return redirect(new_post)
		# Если форма не валидна перенаправляем пользователя обратно
		# на страницу создания поста и отправляем связанную форму
		return render(request, 'create_post.html', context={'form': bound_form})


# Класс для обработки get- и post-запросов страницы редактирования поста
class PostEdit(View):

	def get(self, request, slug):
		# Извлечение из базы данных объекта поста по полю slug
		post = Post.objects.get(slug__iexact = slug)
		# Создание формы с заполненными данными на основе извлеченного поста
		form = PostForm(instance=post)
		# Отображение страницы с заполненной формой
		return render(request, 'edit_post.html', context={'form': form, 'post': post})

	def post(self, request, slug):
		# Извлечение из базы данных объекта поста по полю slug
		post = Post.objects.get(slug__iexact = slug)
		# Создание формы с заполненными данными на основе извлеченного поста
		# + данные post-запроса
		form = PostForm(request.POST, instance = post)
		# Проверка формы на валидность
		if form.is_valid():
			# Сохранение отредактированного поста
			edited_post = form.save()
			# Редирект на страницу обновленного поста
			return redirect(edited_post)
		# Если форма не валидна - возвращение пользователя на страницу
		# редактирование и повторная отправка некоректной формы
		return render(request, 'edit_post.html', context={'form': form, 'post': post})


# Класс для обработки get- и post-запросов страницы удаления поста
class PostDelete(View):

	def get(self, request, slug):
		# Извлечение из базы данных объекта поста по полю slug
		post = Post.objects.get(slug__iexact=slug)
		# Отображение страницы с выбранным постом
		return render(request, 'delete_post.html', context={'post': post})

	def post(self, request, slug):
		# Извлечение из базы данных объекта поста по полю slug
		post = Post.objects.get(slug__iexact=slug)
		# Удаление поста
		post.delete()
		# Получение обновленного списка постов
		posts = Post.objects.all()
		# Отображение главной страницы и передача обновленного списка постов
		return render(request, 'all_post.html', context={'posts': posts})


# Функция для вывода страницы с отображением всех созданных тэгов
def all_tag(request):
	# Получение всех объектов модели тэга из базы данных
	tags = Tag.objects.all()
	# Отображение страницы
	return render(request, 'all_tag.html', context={'tags': tags})


# Класс для вывода страницы тэга
class TagDetail(View):

	def get(self, request, slug):
		# Получение тэга по полю slug
		tag = get_object_or_404(Tag, slug__iexact=slug)
		# Отображение страницы
		return render(request, 'detail_tag.html', context={'tag': tag})


# Класс для обработки get- и post-запросов страницы создания нового тэга
class TagCreate(View):
	
	def get(self, request):
		# Получение формы для модели тэга
		form = TagForm()
		# Отображение страницы
		return render(request, 'create_tag.html', context={'form': form})

	def post(self, request):
		# Получение заполненной формы
		form = TagForm(request.POST)
		# Проверка формы на валидность
		if form.is_valid():
			# Сохранение нового объекта модели тэг
			new_tag = form.save()
			# Редирект на страницу только-что созданного тэга
			return redirect(new_tag)
		# Если форма не валидна повторная отправка на страницу создания тэга
		return render(request, 'create_tag.html', context={'form': form})


# Класс для обработки get- и post-запросов страницы редактирования тэга
class TagEdit(View):
	
	def get(self, request, slug):
		# Получение объекта тэга из базы данных по полю slug
		tag = Tag.objects.get(slug__iexact=slug)
		# Заполнение формы данными из полученного тэга
		form = TagForm(instance=tag)
		# Отображение страницы с заполненной формой
		return render(request, 'edit_tag.html', context={'form': form, 'tag': tag})

	def post(self, request, slug):
		# Получение объекта тэга из базы данных по полю slug
		tag = Tag.objects.get(slug__iexact=slug)
		# Заполнение формы данными из полученного тэга
		# + данные post-запроса
		form = TagForm(request.POST, instance=tag)
		# Проверка валидности формы
		if form.is_valid():
			# Сохранение отредактированного тэга
			edit_tag = form.save()
			# Редирект на страницу обновленного тэга
			return redirect(edit_tag)
		# Если форма не валидна - отображаеться страница редактирования
		# тэга с полученной формой
		return render(request, 'edit_tag.html', context={'form': form, 'tag': tag})


# Класс для обработки get- и post-запросов страницы удаления тэга
class TagDelete(View):
	
	def get(self, request, slug):
		# Получение объекта тэга из базы данных по полю slug
		tag = Tag.objects.get(slug__iexact=slug)
		# Отображение страницы удаления выбранного тэга
		return render(request, 'delete_tag.html', context={'tag': tag})

	def post(self, request, slug):
		# Получение объекта тэга из базы данных по полю slug
		tag = Tag.objects.get(slug__iexact=slug)
		# Удаление тэга
		tag.delete()
		# Получение обновленного списка тэгов
		tags = Tag.objects.all()
		# Отображение страницы с обновленным списком тэгов
		return render(request, 'all_tag.html', context={'tags': tags})