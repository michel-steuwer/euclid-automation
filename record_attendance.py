from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions

from password import username, password, secure_word

from datetime import datetime

students = [
    {
        "name": "First Last",
        "description": "Description",
        "notes": "Notes"
    }
]

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, timeout=5)
original_window = driver.current_window_handle


def click(by, text):
    wait.until(lambda d: d.find_element(by, text))
    driver.find_element(by, text).click()


def select(by, text, value):
    wait.until(lambda d: d.find_element(by, text))
    Select(driver.find_element(by, text)).select_by_visible_text(value)


def send_keys(by, text, value):
    wait.until(lambda d: d.find_element(by, text))
    driver.find_element(By.ID, text).send_keys(value)


def clear(by, text):
    wait.until(lambda d: d.find_element(by, text))
    driver.find_element(By.ID, text).clear()


def login():
    click(By.ID, "login-btn")

    send_keys(By.ID, "login", username)
    click(By.ID, "submit")

    send_keys(By.ID, "password", password)
    click(By.ID, "submit")


def goto_euclid():
    click(By.ID, "myed-nav-tab-2")
    click(By.LINK_TEXT, "EUCLID")


def pass_second_challenge():
    def get_position_text(d, label):
        elem = d.find_element(By.ID, label)
        text = elem.get_attribute('innerText')
        return text[text.rfind(":") + 1:].strip()

    def get_pos(label):
        wait.until(lambda d: get_position_text(d, label).isnumeric())
        return int(get_position_text(driver, label))

    c1 = get_pos("c1label")
    send_keys(By.ID, "c1", secure_word[c1-1])
    c2 = get_pos("c2label")
    send_keys(By.ID, "c2", secure_word[c2-1])
    c3 = get_pos("c3label")
    send_keys(By.ID, "c3", secure_word[c3-1])

    click(By.ID, "loginsubmit")


def open_student_window(name):
    click(By.LINK_TEXT, "Students")

    click(By.LINK_TEXT, "My students | Student Hub")

    click(By.LINK_TEXT, name)

    wait.until(expected_conditions.number_of_windows_to_be(2))
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break


def close_window():
    driver.close()
    driver.switch_to.window(original_window)


def add_engagement(date, description, notes):
    click(By.LINK_TEXT, "Engagement")
    click(By.LINK_TEXT, "Add event")

    select(By.ID, "ANSWER.TTQ.MENSYS.1.", "Attendance")

    clear(By.ID, "ANSWER.TTQ.MENSYS.3.")
    send_keys(By.ID, "ANSWER.TTQ.MENSYS.3.", date)

    click(By.ID, "ANSWER.TTQ.MENSYS.5.1")

    send_keys(By.ID, "ANSWER.TTQ.MENSYS.9.", description)

    send_keys(By.ID, "ANSWER.TTQ.MENSYS.10.", notes)

    click(By.ID, "ANSWER.TTQ.MENSYS.12.")


driver.get("https://www.myed.ed.ac.uk/")
login()
goto_euclid()
pass_second_challenge()

for student in students:
    open_student_window(student["name"])

    date = student.get("date", default=datetime.today().strftime("%d/%b/%Y"))
    description = student.get("description", default="")
    notes = student.get("notes", default="")

    add_engagement(date, description, notes)

    close_window()

driver.quit()
