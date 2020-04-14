from django.test import TestCase, Client
import unittest
from django.contrib.auth.models import User
from .models import TodoList, Priority
from datetime import datetime
# Create your tests here.


class TestLogin(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()


    def test_home_page_accessible_after_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

    def test_home_page_redirects_if_not_logged_in(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login?next=/')

    def test_login_true(self):
        #Mandar info posta
        response = self.client.post(
            '/login', {
            'username': 'testuser',
            'password': '12345'
            },
            follow=True
        )
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_false(self):
        response = self.client.post(
            '/login', {
            'username': 'testuser',
            'password': 'pwd_incorrecta'
            },
            follow=True
        )
        self.assertFalse(response.context['user'].is_authenticated)


class TestTodoListCRUD(TestCase):
    def setUp(self):
        self.priority = Priority(
            name='HIGH',
            order=1
        )
        self.priority.save()
        self.client = Client()
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()
        self.not_user = User.objects.create(username='not testuser')
        self.not_user.save()
        self.todo_list_user = TodoList(
            title='asd',
            Description='asd',
            assigned_user=self.user,
            done=True,
            created=datetime.now(),
            updated=datetime.now(),
            created_by=self.user,
            updated_by=self.user,
            priority=self.priority
        )
        self.todo_list_user.save()
        self.todo_list_not_user = TodoList(
            title='asd',
            Description='asd',
            assigned_user=self.not_user,
            done=True,
            created=datetime.now(),
            updated=datetime.now(),
            created_by=self.not_user,
            updated_by=self.not_user,
            priority=self.priority
        )
        self.todo_list_not_user.save()
        self.client.login(username='testuser', password='12345')

    def test_check_todolist_of_user(self):
        response = self.client.get('/')
        todo_list_of_user = response.context['todolist_list'].get()
        self.assertEqual(todo_list_of_user.id, self.todo_list_user.id)

    def test_create_todolist_correct(self):
        response = self.client.post(
            '/create/', {
                'title': 'gilada1',
                'Description': 'gilada2',
                'done': True,
                'priority': self.priority.id
            },
            follow=True
        )
        self.assertRedirects(response, '/detail/{}/'.format(response.context['object'].id))

    def test_create_todolist_incorrect(self):
        response = self.client.post(
            '/create/', {
                'invalid_param': 'cualquier gilada'
            },
            follow=True
        )
        self.assertFalse(response.context['form'].is_valid())

    def test_delete_todolist_correct(self):
        ##VER QUE ONDA, ARREGLAR DESDE ACA!
        response = self.client.delete(
            '/delete/{}/'.format(self.todo_list_user.id),
            follow=True
        )
        self.assertTrue(True)

    def test_delete_todolist_incorrect(self):
        pass
