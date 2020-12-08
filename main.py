import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Сценарий:
# Входим под учетной записью пользователя, затем создаем пост, проверяем
# его с записи создателя, гостя и другого пользователя. Заходим в редактор
# делаем запись личной и проверяем видна ли она кому то кроме создаетля.
# Затем заходим в аккаунт создателя и находим в списке его записей нашу созданную ранее
# после чего ее удаляем.
class WebTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_create_record(self):
        driver = self.driver
        driver.implicitly_wait(100)

        # Так как мы часто логинемся создаем метод
        def login(name, password):
            driver.get("https://ruswizard.site/test/wp-login.php")
            for i in range(20):
                driver.find_elements_by_id(id_="user_login")[0].send_keys(Keys.BACK_SPACE)
            WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.ID, "user_login"))) \
                .send_keys(name)
            driver.find_elements_by_id(id_="user_pass")[0].send_keys(password)
            driver.find_elements_by_id(id_="wp-submit")[0].click()
            WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1:nth-child(1)")))

        # Логинемся и создаем запись
        login("aglushko", "bpNcZtU)YrvM!O6o")
        driver.get(url="https://ruswizard.site/test/wp-admin/post-new.php")
        post = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "post-title-0"))
        )
        self.text = "Safari is shit"
        post.send_keys(self.text)
        driver.find_element_by_xpath('//*[@id="editor"]/div/div/div[1]/div/div[1]/div/div[2]/button[2]').click()
        driver.find_element_by_xpath('//*[@id="editor"]/div/div/div[1]' +
                                     '/div/div[2]/div[3]/div/div/div/div[1]/div[1]/button').click()
        self.link = driver.find_elements_by_id("inspector-text-control-0")[0].get_attribute("value")
        self.edit = driver.current_url

        # Проверяем запись с разны аккаунтов
        driver.get(self.link)
        assert self.text == driver.find_element_by_css_selector(".entry-title").text
        driver.get("https://ruswizard.site/test/wp-login.php?action=logout&_wpnonce=6ad8284a71")
        driver.find_element_by_link_text("выйти").click()
        WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".message")))
        driver.get(self.link)
        assert self.text == driver.find_element_by_css_selector(".entry-title").text
        login("aglushko_1", "lvgU&(wQ@TLseB^n")
        driver.get(self.link)
        assert self.text == driver.find_element_by_css_selector(".entry-title").text
        driver.get("https://ruswizard.site/test/wp-login.php?action=logout&_wpnonce=6ad8284a71")
        driver.find_element_by_link_text("выйти").click()
        WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".message")))

        # Логинемся с аккаунта пользователя и делаем запись личной
        login("aglushko", "bpNcZtU)YrvM!O6o")
        driver.get(self.edit)
        driver.find_element_by_css_selector(".edit-post-post-visibility__toggle").click()
        driver.find_elements_by_id("editor-post-private-0")[0].click()
        driver.switch_to.alert.accept()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                                                          ".editor-post-publish-button"), "Обновить"))
        # Проверяем доступность записи с разных аккаунтов
        driver.get(self.link)
        assert "Личное: " + self.text == driver.find_element_by_css_selector(".entry-title").text
        driver.get("https://ruswizard.site/test/wp-login.php?action=logout&_wpnonce=6ad8284a71")
        driver.find_element_by_link_text("выйти").click()
        WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".message")))
        driver.get(self.link)
        assert "Страница не найдена" == driver.find_element_by_css_selector(".entry-title").text
        login("aglushko_1", "lvgU&(wQ@TLseB^n")
        driver.get(self.link)
        assert "Страница не найдена" == driver.find_element_by_css_selector(".entry-title").text
        driver.get("https://ruswizard.site/test/wp-login.php?action=logout&_wpnonce=6ad8284a71")
        driver.find_element_by_link_text("выйти").click()
        WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".message")))

        # Находим запись в списе
        login("aglushko", "bpNcZtU)YrvM!O6o")
        driver.get("https://ruswizard.site/test/wp-admin/edit.php")
        driver.find_element_by_link_text("Safari is shit").click()
        assert self.text == driver.find_elements_by_id("post-title-0")[0].text

        # Удаляем запись и проверяем что она больше недоступна
        driver.find_element_by_css_selector(".editor-post-trash").click()
        WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".wp-heading-inline")))
        driver.get(self.link)
        assert "Страница не найдена" == driver.find_element_by_css_selector(".entry-title").text

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()



