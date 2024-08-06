import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.get('https://petfriends.skillfactory.ru/login')
    driver.maximize_window()
    yield driver

    driver.quit()


def test_show_all_pets(driver):
    driver.find_element(By.ID, 'email').send_keys('dinar0002@mail.ru')
    driver.find_element(By.ID, 'pass').send_keys('434310_ASDf')
    driver.implicitly_wait(10)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')
    for i in range(len(names)):
        image_source = images[i].get_attribute('src')
        name_text = names[i].text
        print(f"Image source: {image_source}")
        print(f"Name text: {name_text}")
        assert image_source != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def test_show_my_pets(driver):
    wait = WebDriverWait(driver, 5)
    driver.find_element(By.ID, 'email').send_keys('dinar0002@mail.ru')
    driver.find_element(By.ID, 'pass').send_keys('434310_ASDf')
    driver.implicitly_wait(10)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    wait.until(EC.element_to_be_clickable((By.XPATH, '//a[text()="Мои питомцы"]'))).click()
    assert driver.find_element(By.TAG_NAME, 'h2').text == "gen0m"

    # Определяем количество питомцев
    pets_count = int(driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1])

    # Ищем в теле таблицы все строки с полными данными питомцев (имя, порода, возраст)
    css_locator = 'tbody>tr'
    data_my_pets = driver.find_elements(By.CSS_SELECTOR, css_locator)

    # Проверка наличия всех питомцев
    assert len(data_my_pets) == pets_count

    # Находим данные о питомцах
    images = driver.find_elements(By.CSS_SELECTOR, 'img[style="max-width: 100px; max-height: 100px;"]')
    names = [name.text for name in driver.find_elements(By.XPATH, '//tbody/tr/td[1]')]
    breeds = [breed.text for breed in driver.find_elements(By.XPATH, '//tbody/tr/td[2]')]
    ages = [age.text for age in driver.find_elements(By.XPATH, '//tbody/tr/td[3]')]

    # Проверяем, что хотя бы у половины питомцев есть фотографии
    assert len([img for img in images if img.get_attribute('src')]) >= pets_count / 2

    # Проверка на наличие имени, возраста и породы у каждого питомца
    assert len(names) == pets_count and len(breeds) == pets_count and len(ages) == pets_count

    # Проверка на уникальность имен
    assert len(names) == len(set(names))

    # Проверка на уникальность питомцев (имя, порода, возраст)
    unique_pets = set(zip(names, breeds, ages))
    assert len(unique_pets) == pets_count
