from http import HTTPStatus
from urllib import response
from django.test import TestCase
from django.urls import reverse

# Create your tests here.
# python manage.py test . - запуск всех тестов

# python manage.py test women - запуск тестов конкретного приложения, например women
# или
# python manage.py test women.tests.GetPageTestCase

# python manage.py test women.tests.GetPageTestCase.test_case_1 - запуск одного конкретного теста

# так же создается default - тестовая база данных для теста, которая удаляется


class GetPagesTestCase(TestCase):
    def setUp(self):
        #инициализация перед тестом
        pass
    
    def test_mainpage(self):
        path = reverse('home')
        #client - имитирует запрос url браузера
        # response = ответ на запрос
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK) # HTTPStatus.OK = 200 
        # self.assertIn('women/index.html', response.template_name)
        self.assertTemplateUsed(response, 'women/index.html')
        
        self.assertEqual(response.context_data['title'], 'Главная страница')
        
    def test_redirect_addpage(self):
        # тест http://127.0.0.1:8000/users/login/?next=/addpage/
        path = reverse('add_page')
        
        # получение пути перенаправления
        redirect_uri = reverse('users:login') + '?next=' + path
        
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)
        
    def test_case_2(self):
        pass
    
    def tearDown(self) -> None:
        # дествия после выполнения теста
        pass