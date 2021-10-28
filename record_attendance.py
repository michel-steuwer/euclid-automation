from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions


def record_attendance(students, username, password, secure_word):
    options = Options()
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, timeout=10)
    original_window = driver.current_window_handle

    driver.get("https://www.myed.ed.ac.uk/")
    login(wait, driver, username, password)
    goto_euclid(wait, driver)
    pass_second_challenge(wait, driver, secure_word)

    for student in students:
        open_student_window(wait, driver, original_window, student["name"])

        add_engagement(wait, driver, student["date"], student["description"], student["notes"])

        close_window(driver, original_window)

    driver.quit()


def click(wait, driver, by, text):
    wait.until(lambda d: d.find_element(by, text))
    driver.find_element(by, text).click()


def select(wait, driver, by, text, value):
    wait.until(lambda d: d.find_element(by, text))
    Select(driver.find_element(by, text)).select_by_visible_text(value)


def send_keys(wait, driver, by, text, value):
    wait.until(lambda d: d.find_element(by, text))
    driver.find_element(By.ID, text).send_keys(value)


def clear(wait, driver, by, text):
    wait.until(lambda d: d.find_element(by, text))
    driver.find_element(By.ID, text).clear()


def login(wait, driver, username, password):
    click(wait, driver, By.ID, "login-btn")

    send_keys(wait, driver, By.ID, "login", username)
    click(wait, driver, By.ID, "submit")

    send_keys(wait, driver, By.ID, "password", password)
    click(wait, driver, By.ID, "submit")


def goto_euclid(wait, driver):
    click(wait, driver, By.ID, "myed-nav-tab-2")
    click(wait, driver, By.LINK_TEXT, "EUCLID")


def pass_second_challenge(wait, driver, secure_word):
    def get_position_text(d, label):
        elem = d.find_element(By.ID, label)
        text = elem.get_attribute('innerText')
        return text[text.rfind(":") + 1:].strip()

    def get_pos(label):
        wait.until(lambda d: get_position_text(d, label).isnumeric())
        return int(get_position_text(driver, label))

    c1 = get_pos("c1label")
    send_keys(wait, driver, By.ID, "c1", secure_word[c1-1])
    c2 = get_pos("c2label")
    send_keys(wait, driver, By.ID, "c2", secure_word[c2-1])
    c3 = get_pos("c3label")
    send_keys(wait, driver, By.ID, "c3", secure_word[c3-1])

    click(wait, driver, By.ID, "loginsubmit")


def open_student_window(wait, driver, original_window, name):
    click(wait, driver, By.LINK_TEXT, "Students")

    click(wait, driver, By.LINK_TEXT, "My students | Student Hub")

    click(wait, driver, By.LINK_TEXT, name)

    wait.until(expected_conditions.number_of_windows_to_be(2))
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break


def close_window(driver, original_window):
    driver.close()
    driver.switch_to.window(original_window)


def add_engagement(wait, driver, date, description, notes):
    click(wait, driver, By.LINK_TEXT, "Engagement")
    click(wait, driver, By.LINK_TEXT, "Add event")

    select(wait, driver, By.ID, "ANSWER.TTQ.MENSYS.1.", "Attendance")

    clear(wait, driver, By.ID, "ANSWER.TTQ.MENSYS.3.")
    send_keys(wait, driver, By.ID, "ANSWER.TTQ.MENSYS.3.", date)

    click(wait, driver, By.ID, "ANSWER.TTQ.MENSYS.5.1")

    send_keys(wait, driver, By.ID, "ANSWER.TTQ.MENSYS.9.", description)

    send_keys(wait, driver, By.ID, "ANSWER.TTQ.MENSYS.10.", notes)

    click(wait, driver, By.ID, "ANSWER.TTQ.MENSYS.12.")
