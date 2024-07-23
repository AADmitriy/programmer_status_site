from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.urls import reverse
import time
from .models import UserStats, Title, Job, Skill
from django.contrib.auth.models import User
from .utils_for_test import *

# Create your tests here.


class TestSignUp(StaticLiveServerTestCase):
    def test_isUserCreated(self):
        signup_form_url = reverse('signup')
        username = "testuser"
        password = "qwe567rty432"

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(f'{self.live_server_url}{signup_form_url}')

        find_element_and_send_keys(self.driver, 'input[name="username"]', username, wait=True)
        find_element_and_send_keys(self.driver, 'input[name="password1"]', password)
        find_element_and_send_keys(self.driver, 'input[name="password2"]', password)
        find_and_click_button(self.driver, 'button[type="submit"]')

        self.assertTrue(User.objects.filter(username=username).exists())

    def tearDown(self):
        self.driver.quit()


class TestDetailsUpdate(StaticLiveServerTestCase):
    def setUp(self):
        stats_page_url = reverse('stats_page')
        self.stats_page_full_link = f'{self.live_server_url}{stats_page_url}'
        login_url = reverse('login')
        username = "testuser"
        password = "qwe567rty432"
        self.user = User.objects.create_user(username=username, password=password)
        UserStats.objects.create(user=self.user)

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)

        # Log In
        self.driver.get(f'{self.live_server_url}{login_url}')
        find_element_and_send_keys(self.driver, 'input[type="text"]', username, wait=True)
        find_element_and_send_keys(self.driver, 'input[type="password"]', password)
        find_and_click_button(self.driver, 'button[type="submit"]')

    def is_update_page_working(self, obj_class, link_selector, data_dict=None):
        if data_dict:
            name = data_dict['name']
            obj_class.objects.create(user=self.user, **data_dict)
        else:
            name = 'name'
            obj_class.objects.create(user=self.user, name='name', description='description')

        self.driver.get(self.stats_page_full_link)

        find_and_click_button(self.driver, link_selector, wait=True)
        find_and_click_button(self.driver, '#update_link', wait=True)
        update_value = ' Updated!'
        find_element_and_send_keys(self.driver, 'textarea[name="description"]', update_value, wait=True, time=3)
        find_and_click_button(self.driver, 'input[type="submit"]')

        updated_description = find_element_with_waiting(self.driver, '#description_id').text
        is_updated_on_site = update_value in updated_description
        changed_object = obj_class.objects.get(user=self.user, name=name)
        is_updated_in_db = update_value in changed_object.description

        return is_updated_on_site and is_updated_in_db

    def test_title_update(self):
        self.assertTrue(self.is_update_page_working(Title, '#titles a'))

    def test_job_update(self):
        data_dict = {
            'name': 'name',
            'description': 'description',
            'current': False,
        }
        self.assertTrue(self.is_update_page_working(Job, '#jobs a', data_dict=data_dict))

    def test_passive_skill_update(self):
        data_dict = {
            'name': 'name',
            'description': 'description',
            'active': False,
        }
        self.assertTrue(self.is_update_page_working(Skill, '#passive_skills a', data_dict=data_dict))

    def test_active_skill_update(self):
        data_dict = {
            'name': 'name',
            'description': 'description',
            'active': True,
        }
        self.assertTrue(self.is_update_page_working(Skill, '#active_skills a', data_dict=data_dict))

    def tearDown(self):
        self.driver.quit()
