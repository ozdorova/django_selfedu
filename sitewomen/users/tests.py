
from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Create your tests here.



class RegisterUserTestCase(TestCase):
    def setUp(self) -> None:
        self.data = {
            'username': 'user_1',
            'email': 'user1@sitewomen.ru',
            'first_name': 'Elnora',
            'last_name': 'Norris',
            'password1': '12345678Aa',
            'password2': '12345678Aa',
        }
    
    def test_from_registration_get(self):
        """
        Функция test_from_registration_get проверяет запрос GET для страницы регистрации пользователя
        """
        
        path = reverse('users:register')
        response = self.client.get(path)
        self.assertAlmostEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')
    
    def test_user_registration_success(self):
        """
        Функция проверяет успешную регистрацию пользователя, отправляя регистрационную форму через запрос
        POST, проверяя перенаправление на страницу входа и проверяя существование пользователя в базе
        данных.
        """
        
        user_model = get_user_model()
        path = reverse('users:register')
        response = self.client.post(path, self.data) # заполняем форму регистрации через post запрос
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login')) # проверяем что было перенаправление
        self.assertTrue(user_model.objects.filter(username=self.data['username']).exists()) # проверяем наличие пользователя в БД
    
    def test_user_registration_password_error(self):
        """
        Функция проверяет наличие ошибки пароля во время регистрации пользователя.
        """
        
        self.data['password2'] = '12345678Zz'
        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK) # проверяем что остаемся на этой странице
        self.assertContains(response, "Введенные пароли не совпадают.", html=True)
    
    def test_user_registration_exists_errors(self):
        """
        Функция проверяет наличие ошибок, связанных с существующей регистрацией пользователя.
        """
        user_model = get_user_model()
        user_model.objects.create(username=self.data['username'])
        
        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует')