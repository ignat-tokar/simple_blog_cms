# Импортирование модуля для работы с формами
from django import forms
# Импортирование моделей проекта
from .models import Post, Tag


# Класс формы для модели поста
class PostForm(forms.ModelForm):
	class Meta:
		# Установление модели для формы
		model = Post
		# Обозначение полей
		fields = ['title', 'tags', 'text']
		# Добавление виджетов и установка дополнительных атрибутов для них
		widgets = {
			'title' : forms.TextInput(attrs={'class': 'form-control'}),
			'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
			'text' : forms.Textarea(attrs={'class': 'form-control'})
		}


# Класс формы для модели тэга
class TagForm(forms.ModelForm):
	class Meta:
		# Установка модели для текущей формы
		model = Tag
		# Обозначение полей
		fields = ['title']
		# Добавление виджетов и установка дополнительных атрибутов
		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			# 'slug': forms.TextInput(attrs={'class': 'form-control'})
		}