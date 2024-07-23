from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from django.urls import reverse
import time
from .models import Title, Job, UserStats, Reflection, Skill, Language, Quest
from django.contrib.auth.models import User
from .utils_for_test import *


class TestReflectionCreation(StaticLiveServerTestCase):
    def setUp(self):
        reflection_form_url = reverse('create_reflection')
        self.reflection_page = reverse('reflection_page')
        self.reflection_title_text = "title"
        self.reflection_description_text = "text"
        username = "testuser"
        password = "qwe567rty432"
        self.user = User.objects.create_user(username=username, password=password)
        UserStats.objects.create(user=self.user)

        chrome_options = Options()
        chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(f'{self.live_server_url}{reflection_form_url}')

        # Log In
        find_element_and_send_keys(self.driver, 'input[type="text"]', username, wait=True)
        find_element_and_send_keys(self.driver, 'input[type="password"]', password)
        find_and_click_button(self.driver, 'button[type="submit"]')

        # Populate required fields and find submit button
        self.submit_button = find_element_with_waiting(self.driver, 'input[type="submit"]')
        find_element_and_send_keys(self.driver, '#id_reflection-title', self.reflection_title_text)
        find_element_and_send_keys(self.driver, '#id_reflection-description', self.reflection_description_text)

    def test_reflection_creation(self):
        click_button(self.driver, self.submit_button)
        # After redirect check for entered data
        self.assertTrue(is_text_in_element(self.driver, "div.reflection", self.reflection_title_text,
                                        element_part_selector=".reflection_title"))
        self.assertTrue(is_text_in_element(self.driver, "div.reflection", self.reflection_description_text,
                                        element_part_selector=".reflection_description"))
        self.assertTrue(Reflection.objects.filter(user=self.user, title=self.reflection_title_text).exists())


    def test_same_jobs_error(self):
        #Test if error message is displayed when user enters two same jobs
        find_and_click_button(self.driver, '#add_job_button', count=2)

        # Find and populate job input fields
        job_input_forms = self.driver.find_elements(By.CSS_SELECTOR, '#job_form_list .data_input')
        self.assertTrue(len(job_input_forms) == 2)
        for input_form in job_input_forms:
            find_element_and_send_keys(input_form, 'input', 'job 1')
            find_element_and_send_keys(input_form, 'textarea', 'description')

        click_button(self.driver, self.submit_button)
        self.assertTrue(wait_for_any_text_in_element(self.driver, '#jobs_error_list'))

    def test_jobs_repeat_db_error(self):
        #Test if errors message is displayed when user enters job name that already exists in database
        Job.objects.create(user=self.user, name="job 1234", description="another description", current=False)

        find_and_click_button(self.driver, "#add_job_button")

        job_input_form = self.driver.find_element(By.CSS_SELECTOR, '#job_form_list .data_input')
        find_element_and_send_keys(job_input_form, 'input', 'job 1234')
        find_element_and_send_keys(job_input_form, 'textarea', 'description')

        click_button(self.driver, self.submit_button)
        self.assertTrue(wait_for_any_text_in_element(self.driver, '#jobs_error_list'))

    def test_title_forms(self):
        title_text = 'title selenium test'

        find_and_click_button(self.driver, "#add_title_button")
        title_input_form = self.driver.find_element(By.CSS_SELECTOR, '#title_form_list .data_input')
        find_element_and_send_keys(title_input_form, 'input', title_text)
        find_element_and_send_keys(title_input_form, 'textarea', 'description')

        click_button(self.driver, self.submit_button)
        # After redirect check for entered data
        self.assertTrue(is_text_in_element(self.driver, "div.reflection", title_text,
                                        element_part_selector="div.reflection_gains"))
        created_title = Title.objects.filter(user=self.user, name=title_text)
        self.assertTrue(created_title.exists())

    def test_job_forms(self):
        job_text = 'job selenium test'

        find_and_click_button(self.driver, "#add_job_button")
        job_input_form = self.driver.find_element(By.CSS_SELECTOR, '#job_form_list .data_input')
        find_element_and_send_keys(job_input_form, 'input', job_text)
        find_element_and_send_keys(job_input_form, 'textarea', 'description')

        click_button(self.driver, self.submit_button)
        # After redirect check for entered data
        self.assertTrue(is_text_in_element(self.driver, "div.reflection", job_text,
                                        element_part_selector="div.reflection_gains"))
        created_job = Job.objects.filter(user=self.user, name=job_text)
        self.assertTrue(created_job.exists())

    def test_skill_forms(self):
        skill_text = 'skill selenium test'

        find_and_click_button(self.driver, "#add_skill_button")
        skill_input_form = self.driver.find_element(By.CSS_SELECTOR, '#skill_form_list .data_input')
        find_element_and_send_keys(skill_input_form, 'input[type="text"]', skill_text)
        find_element_and_send_keys(skill_input_form, 'textarea', 'description')
        find_and_click_button(self.driver, 'input[type="checkbox"]', search_in_element=skill_input_form)

        click_button(self.driver, self.submit_button)
        # After redirect check for entered data
        self.assertTrue(is_text_in_element(self.driver, "div.reflection", skill_text,
                                        element_part_selector="div.reflection_gains"))
        created_skill = Skill.objects.filter(user=self.user, name=skill_text)
        self.assertTrue(created_skill.exists())

    def test_level_forms(self):
        level_increase = 5
        # Set up database
        skill_names = ["skill 1", "skill 2", "skill 3"]
        for name in skill_names:
            Skill.objects.create(user=self.user, name=name, description="description", active=True)
        another_user = User.objects.create_user(username="username", password="password")
        another_skill_name = "another skill"
        Skill.objects.create(user=another_user, name=another_skill_name, description="description", active=True)

        self.driver.refresh()
        self.submit_button = find_element_with_waiting(self.driver, 'input[type="submit"]')
        find_element_and_send_keys(self.driver, '#id_reflection-title', self.reflection_title_text)
        find_element_and_send_keys(self.driver, '#id_reflection-description', self.reflection_description_text)

        find_and_click_button(self.driver, "#add_level_button")
        level_input_form = self.driver.find_element(By.CSS_SELECTOR, '#level_form_list .level_input')
        find_element_and_send_keys(level_input_form, 'input[type="number"]', level_increase)
        select_input = Select(level_input_form.find_element(By.CSS_SELECTOR, 'select'))
        skill_name_options = [option.get_attribute("value") for option in select_input.options]

        self.assertTrue(another_skill_name not in skill_name_options)
        self.assertTrue(skill_names == skill_name_options)
        select_input.select_by_value(skill_names[0])

        click_button(self.driver, self.submit_button)
        # After redirect check for entered data
        self.assertTrue(is_text_in_element(self.driver, "div.reflection", skill_names[0],
                                        element_part_selector="div.reflection_gains"))
        increased_skill = Skill.objects.get(user=self.user, name=skill_names[0])
        self.assertTrue(increased_skill.level == level_increase + 1)

    def test_stats_form(self):
        frontend_stat = 40
        backend_stat = 50
        data_science_stat = 20
        data_base_stat = 0

        find_element_and_send_keys(self.driver, 'input[name="stats_incr-frontend_incr"]', frontend_stat, overwrite=True)
        find_element_and_send_keys(self.driver, 'input[name="stats_incr-backend_incr"]', backend_stat, overwrite=True)
        find_element_and_send_keys(self.driver, 'input[name="stats_incr-data_science_incr"]', data_science_stat, overwrite=True)
        find_element_and_send_keys(self.driver, 'input[name="stats_incr-data_base_incr"]', data_base_stat, overwrite=True)

        click_button(self.driver, self.submit_button)
        # After redirect check for entered data
        stat_names = ['frontend', 'backend', 'data science']
        for stat_name in stat_names:
            self.assertTrue(is_text_in_element(self.driver, "div.reflection", stat_name,
                                            element_part_selector="div.reflection_gains", case_sensitive=False))
        self.assertTrue(is_text_not_in_element(self.driver, "div.reflection", 'data base',
                                           element_part_selector="div.reflection_gains", case_sensitive=False))

        user_stats = UserStats.objects.get(user=self.user)
        self.assertTrue(user_stats.frontend_stat == frontend_stat)
        self.assertTrue(user_stats.backend_stat == backend_stat)
        self.assertTrue(user_stats.data_science_stat == data_science_stat)
        self.assertTrue(user_stats.data_base_stat == data_base_stat)

    def test_lang_forms(self):
        lang_text = 'lang selenium test'
        lang_comprehension = 30

        find_and_click_button(self.driver, "#add_lang_button")
        lang_input_form = self.driver.find_element(By.CSS_SELECTOR, '#lang_form_list .lang_form')
        find_element_and_send_keys(lang_input_form, 'input[type="text"]', lang_text)
        find_element_and_send_keys(lang_input_form, 'input[type="number"]', lang_comprehension)

        click_button(self.driver, self.submit_button)
        # After redirect check for entered data
        self.assertTrue(is_text_in_element(self.driver, "div.reflection", lang_text,
                                        element_part_selector="div.reflection_gains"))
        created_lang = Language.objects.filter(user=self.user, name=lang_text)
        self.assertTrue(created_lang.exists())
        self.assertTrue(created_lang[0].comprehension == lang_comprehension)

    def test_comprehension_forms(self):
        comprehension_increase = 50
        # Set up database
        lang_names = ["lang 1", "lang 2", "lang 3"]
        for name in lang_names:
            Language.objects.create(user=self.user, name=name, comprehension=0)
        another_user = User.objects.create_user(username="username", password="password")
        another_lang_name = "another lang"
        Language.objects.create(user=another_user, name=another_lang_name, comprehension=0)

        self.driver.refresh()
        self.submit_button = find_element_with_waiting(self.driver, 'input[type="submit"]')
        find_element_and_send_keys(self.driver, '#id_reflection-title', self.reflection_title_text)
        find_element_and_send_keys(self.driver, '#id_reflection-description', self.reflection_description_text)

        find_and_click_button(self.driver, "#add_comprehension_form_button")
        lang_compr_input_form = self.driver.find_element(By.CSS_SELECTOR, '#lang_compr_form_list .lang_increase_form')
        find_element_and_send_keys(lang_compr_input_form, 'input[type="number"]', comprehension_increase)
        select_input = Select(lang_compr_input_form.find_element(By.CSS_SELECTOR, 'select'))
        lang_name_options = [option.get_attribute("value") for option in select_input.options]

        self.assertTrue(another_lang_name not in lang_name_options)
        self.assertTrue(lang_names == lang_name_options)
        select_input.select_by_value(lang_names[0])

        click_button(self.driver, self.submit_button)
        # After redirect check for entered data
        self.assertTrue(is_text_in_element(self.driver, "div.reflection", lang_names[0],
                                        element_part_selector="div.reflection_gains"))
        increased_lang = Language.objects.get(user=self.user, name=lang_names[0])
        self.assertTrue(increased_lang.comprehension == comprehension_increase)

    def tearDown(self):
        # input()
        # time.sleep(2)
        self.driver.quit()
