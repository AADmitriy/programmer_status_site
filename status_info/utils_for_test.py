import selenium.common
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains


def find_element_with_waiting(driver, element_selector, time=10, by=By.CSS_SELECTOR):
    searched_element = WebDriverWait(driver, time).until(
        EC.presence_of_element_located((by, element_selector))
    )
    return searched_element


def find_all_elements_with_waiting(driver, element_selector, time=10, by=By.CSS_SELECTOR):
    searched_elements = WebDriverWait(driver, time).until(
        EC.presence_of_all_elements_located((by, element_selector))
    )
    return searched_elements


def find_element(driver, element_selector, wait=False, time=10, by=By.CSS_SELECTOR):
    if not wait:
        searched_element = driver.find_element(by, element_selector)
    else:
        searched_element = find_element_with_waiting(driver, element_selector, time=time, by=by)

    return searched_element


def is_text_in_element(driver, element_selector, text_to_find, element_part_selector='', case_sensitive=True):
    searched_element = find_element_with_waiting(driver, element_selector)
    if element_part_selector != '':
        searched_text = searched_element.find_element(By.CSS_SELECTOR, element_part_selector).text
    else:
        searched_text = searched_element.text

    if not case_sensitive:
        searched_text = searched_text.lower()

    return text_to_find in searched_text


def is_text_not_in_element(driver, element_selector, text_to_find, element_part_selector='', case_sensitive=True):
    return not is_text_in_element(driver, element_selector, text_to_find,
                                  element_part_selector=element_part_selector, case_sensitive=case_sensitive)


def find_element_and_send_keys(driver, element_selector, value, wait=False, time=10, overwrite=False):
    if wait:
        searched_element = find_element_with_waiting(driver, element_selector, time=time)
    else:
        searched_element = driver.find_element(By.CSS_SELECTOR, element_selector)
    if overwrite:
        searched_element.clear()
    searched_element.send_keys(value)


def click_button(driver, button_element, count=1):
    """
    If button redirects to another page do not click more than one time
    or you will got StaleElementExceptions
    """
    for i in range(count):
        ActionChains(driver).move_to_element(button_element).click().perform()


def find_and_click_button(driver, button_selector, count=1, search_in_element=None, wait=False, time=10):
    if search_in_element:
        button_element = find_element(search_in_element, button_selector, wait=wait, time=time)
    else:
        button_element = find_element(driver, button_selector, wait=wait, time=time)
    click_button(driver, button_element, count=count)


class WaitForAnyTextInElement(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            element_text = driver.find_element(*self.locator).text
            return element_text != ''
        except selenium.common.StaleElementReferenceException:
            return False


def wait_for_any_text_in_element(driver, element_selector, time=3):
    try:
        WebDriverWait(driver, time).until(WaitForAnyTextInElement((By.CSS_SELECTOR, element_selector)))
    except selenium.common.NoSuchElementException:
        return False
    except selenium.common.TimeoutException:
        return False
    else:
        return True
