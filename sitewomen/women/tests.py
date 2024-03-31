from http import HTTPStatus
from urllib import response
from django.db.models import QuerySet
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from .models import Women

# Create your tests here.
# python manage.py test . - запуск всех тестов

# python manage.py test women - запуск тестов конкретного приложения, например women
# или
# python manage.py test women.tests.GetPageTestCase

# python manage.py test women.tests.GetPageTestCase.test_case_1 - запуск одного конкретного теста

# так же создается default - тестовая база данных для теста, которая удаляется

# python -Xutf8 manage.py dumpdata women.women -o women/fixtures/women_women.json - загрузка данных БД в json


class GetPagesTestCase(TestCase):
    # загружает фикстуры из папки fixtures и загружает во временную БД данные из рабочей БД
    fixtures =['women_women.json', 'women_category.json', 'women_husband.json', 'women_tagpost.json']
    
    def setUp(self):
        #инициализация перед тестом
        pass
    
    def test_mainpage(self):
        # формируем машрут на главную страницу через имя маршрута из urls.py
        path = reverse('home')
        #client - имитирует запрос url браузера
        # response = ответ на запрос
        response: HttpResponse = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK) # HTTPStatus.OK = 200 
        # self.assertIn('women/index.html', response.template_name)
        self.assertTemplateUsed(response, 'women/index.html')
        
        self.assertEqual(response.context_data['title'], 'Главная страница')
        
    def test_redirect_addpage(self):
        # тест http://127.0.0.1:8000/users/login/?next=/addpage/
        path = reverse('add_page')
        
        # получение пути перенаправления
        redirect_uri = reverse('users:login') + '?next=' + path
        
        response: HttpResponse = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)
        
    def test_data_mainpage(self):
        w: QuerySet = Women.published.all().select_related('cat') # обращение к временной БД default, а не к рабочей БД
        path = reverse('home')
        response = self.client.get(path)
        # print(w)
        self.assertQuerysetEqual(response.context_data['posts'],  w[:5]) # сравнивается 5 статей, тк на странице отображается 5 статей
        
    def test_paginate_mainpage(self):
        path = reverse('home')
        page = 2
        paginate_by = 5
        response = self.client.get(path + f"?page={page}") # имитация запроса перехода на страницу с номером page
        w: QuerySet = Women.published.all().select_related('cat')
        self.assertQuerysetEqual(response.context_data['posts'], w[(page-1) * paginate_by:page * paginate_by])
        
    def test_content_post(self):
        w = Women.published.get(pk=1)
        path = reverse('post', args=[w.slug])
        response = self.client.get(path)
        self.assertEqual(w.content, response.context_data['post'].content)
        
        
        
    def tearDown(self) -> None:
        # дествия после выполнения теста
        pass