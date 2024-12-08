import pytest
from selenium import webdriver
from selenium.common import NoAlertPresentException
from selenium.webdriver.common.by import By
import time

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# Kiểm tra chức năng "Hiển thị mật khẩu" -- bên Egde hiển thị được, Chrome không???

def test_valid_login(driver): #đăng nhập hợp lệ
    driver.get("http://watchplace.great-site.net/admin-login.php")
    driver.find_element(By.ID, "username").send_keys("admin@gmail.com")
    driver.find_element(By.ID, "password").send_keys("123123")
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "login__btn").click()
    time.sleep(5)
    assert "http://watchplace.great-site.net/brand-manager.php" in driver.current_url

def test_leave_fields_blank_login(driver): #đăng nhập mà để trống các trường
    driver.get("http://watchplace.great-site.net/admin-login.php")
    # driver.find_element(By.ID, "username").send_keys("")
    # driver.find_element(By.ID, "password").send_keys("")
    # time.sleep(2)
    driver.find_element(By.CLASS_NAME, "login__btn").click()
    time.sleep(5)

    email_err = driver.find_element(By.CSS_SELECTOR, ".err.username")
    pass_err = driver.find_element(By.CSS_SELECTOR, ".err.password")
    # Assertions to verify error messages are displayed
    assert email_err.is_displayed() and pass_err.is_displayed()

def test_wrong_email_or_password_login(driver): # đăng nhập sai mật khẩu
    driver.get("http://watchplace.great-site.net/admin-login.php")
    driver.find_element(By.ID, "username").send_keys("lgn@gmail.com")
    driver.find_element(By.ID, "password").send_keys("123456")
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "login__btn").click()
    time.sleep(5)

    # Handle the JavaScript alert
    try:
        alert = driver.switch_to.alert
    # Khi một thông báo JavaScript xuất hiện, Selenium cần chuyển sang thông báo này để có thể tương tác.
    # driver.switch_to.alert được sử dụng để truy cập vào thông báo đó.
        assert alert.text == "Email hoặc mật khẩu không hợp lệ!", "Unexpected alert message."
    # Dòng này kiểm tra xem nội dung của thông báo có khớp với
    # nội dung mong đợi là "Email hoặc mật khẩu không hợp lệ!"
    # hay không. Nếu nội dung không khớp, bài kiểm tra sẽ thất bại và
    # hiển thị thông báo "Unexpected alert message."
        alert.accept()
    # Dòng này sẽ đóng thông báo bằng cách nhấp vào nút "OK". alert.accept() mô phỏng thao tác nhấp "OK"
    # để loại bỏ thông báo và cho phép bài kiểm tra tiếp tục.
    except NoAlertPresentException:
        assert False, "Expected alert not present."
    # Khối này bắt lỗi NoAlertPresentException, xảy ra khi không có thông báo nào trên trang khi đáng lẽ phải có.
    # Nếu trường hợp này xảy ra, bài kiểm tra sẽ thất bại với thông báo "Expected alert not present."
    # Điều này đảm bảo rằng bài kiểm tra sẽ báo lỗi hợp lý nếu thông báo không xuất hiện như mong đợi.

def test_invalid_email_character_login(driver): # đăng nhập sai mật khẩu
    driver.get("http://watchplace.great-site.net/admin-login.php")
    driver.find_element(By.ID, "username").send_keys("admin@@gmail.com")
    driver.find_element(By.ID, "password").send_keys("123")
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "login__btn").click()
    time.sleep(5)
    try:
        alert = driver.switch_to.alert
        assert alert.text == "Email hoặc mật khẩu không hợp lệ!", "Unexpected alert message."
        alert.accept()
    except NoAlertPresentException:
        assert False, "Expected alert not present."

def test_logout_by_admin(driver): #đăng xuất
    driver.get("http://watchplace.great-site.net/admin-login.php")
    driver.find_element(By.ID, "username").send_keys("admin@gmail.com")
    driver.find_element(By.ID, "password").send_keys("123123")
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "login__btn").click()
    time.sleep(2)

    driver.find_element(By.CLASS_NAME, "container-header__admin-account").click()
    driver.find_element(By.XPATH, "//a[contains(@href, 'admin-logout.php')]").click()
    time.sleep(2)

    try:
        alert = driver.switch_to.alert
        assert alert.text == "Bạn có chắc chắn muốn đăng xuất?", "Unexpected alert message."
        alert.accept()
    except NoAlertPresentException:
        assert False, "Expected alert not present."

    adminpage = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/p[1]")
    assert "Chào Mừng Bạn Đến Với Trang Quản Trị Viên!" in adminpage.text
    time.sleep(2)

# def test_logout(driver): #đăng xuất
#     driver.get("http://watchplace.great-site.net/admin-login.php")
#     driver.find_element(By.ID, "username").send_keys("admin@gmail.com")
#     driver.find_element(By.ID, "password").send_keys("123123")
#     time.sleep(2)
#     driver.find_element(By.CLASS_NAME, "login__btn").click()
#     time.sleep(2)
#
#     driver.find_element(By.XPATH, "//li[@class='sidebar-nav__item']/a[@href='admin-logout.php']").click()
#     time.sleep(2)
#
#     try:
#         alert = driver.switch_to.alert
#         assert alert.text == "Bạn có chắc chắn muốn đăng xuất?", "Unexpected alert message."
#         alert.accept()
#     except NoAlertPresentException:
#         assert False, "Expected alert not present."



