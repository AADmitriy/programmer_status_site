from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.urls import reverse
import time
from .models import UserStats, Quest
from django.contrib.auth.models import User
from .utils_for_test import *


class TestQuests(StaticLiveServerTestCase):
    def setUp(self):
        self.quests_page_url = reverse('quests_page')
        self.quest_form_url = reverse('create_quest')
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

    def test_same_quest_in_db_error(self):
        quest_name = "quest 1"
        Quest.objects.create(user=self.user, name=quest_name, description="description", completed=False)

        self.driver.get(f'{self.live_server_url}{self.quest_form_url}')

        find_element_and_send_keys(self.driver, 'input[name="name"]', quest_name, wait=True)
        find_element_and_send_keys(self.driver, 'textarea[name="description"]', quest_name)
        find_and_click_button(self.driver, 'input[type="submit"]')

        self.assertTrue(wait_for_any_text_in_element(self.driver, "div.errors"))

    def test_quest_create(self):
        self.driver.get(f'{self.live_server_url}{self.quest_form_url}')

        quest_name = "quest 1"
        find_element_and_send_keys(self.driver, 'input[name="name"]', quest_name, wait=True)
        find_element_and_send_keys(self.driver, 'textarea[name="description"]', quest_name)
        find_and_click_button(self.driver, 'input[type="submit"]')

        self.assertTrue(is_text_in_element(self.driver, "div.current_quest", quest_name,
                                           element_part_selector="h6"))
        created_quest = Quest.objects.filter(user=self.user, name=quest_name)
        self.assertTrue(created_quest.exists())

    def test_quest_complete(self):
        quest_name = "quest to complete"
        Quest.objects.create(user=self.user, name=quest_name, description="description", completed=False)

        self.driver.get(f'{self.live_server_url}{self.quests_page_url}')
        quest = find_element_with_waiting(
            self.driver,
            f"//div[@class='current_quest']/h6[contains(text(), '{quest_name}')]",
            by=By.XPATH).parent

        find_and_click_button(self.driver, 'input[type="submit"]', search_in_element=quest)
        #input()
        quest_completed_element = find_element_with_waiting(
            self.driver,
            f"//div[@class='old_quest']/h6[contains(text(), '{quest_name}')]",
            by=By.XPATH)

        self.assertTrue(quest_completed_element is not None)
        quest_completed = Quest.objects.get(user=self.user, name=quest_name)
        self.assertTrue(quest_completed.completed)

    def test_quest_uncomplete(self):
        quest_name = "quest to uncomplete"
        Quest.objects.create(user=self.user, name=quest_name, description="description", completed=True)

        self.driver.get(f'{self.live_server_url}{self.quests_page_url}')
        quest = find_element_with_waiting(
            self.driver,
            f"//div[@class='old_quest']/h6[contains(text(), '{quest_name}')]",
            by=By.XPATH).parent

        find_and_click_button(self.driver, 'input[type="submit"]', search_in_element=quest)
        # input()
        quest_uncompleted_element = find_element_with_waiting(
            self.driver,
            f"//div[@class='current_quest']/h6[contains(text(), '{quest_name}')]",
            by=By.XPATH)

        self.assertTrue(quest_uncompleted_element is not None)
        quest_uncompleted = Quest.objects.get(user=self.user, name=quest_name)
        self.assertFalse(quest_uncompleted.completed)

    def test_quests_order(self):
        quest_names = ['quest 1', 'quest 2', 'quest 3', 'quest 4']
        for num, name in enumerate(quest_names):
            Quest.objects.create(user=self.user, name=name, description="description", completed=(num > 1))

        self.driver.get(f'{self.live_server_url}{self.quests_page_url}')
        completed_quests = find_all_elements_with_waiting(self.driver, 'div.current_quest')
        uncompleted_quests = find_all_elements_with_waiting(self.driver, 'div.old_quest')
        for quest in completed_quests:
            self.assertTrue(quest.find_element(By.TAG_NAME, 'h6').text in quest_names[:2])
        for quest in uncompleted_quests:
            self.assertTrue(quest.find_element(By.TAG_NAME, 'h6').text in quest_names[2:])

    def tearDown(self):
        self.driver.quit()
