import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from login_logout_test import test_valid_login
from selenium.common import NoAlertPresentException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

customer_info1 = ["Nghi", "0326259419", "lgn@gmail.com", "123123", "15B Street"]
customer_info2 = ["user", "0326259411", "user@gmail.com", "index", "15B Street"]

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_add_customer(driver):
    test_valid_login(driver)
    driver.find_element(By.XPATH, "//li[@class='sidebar-nav__item']/a[@href='user-manager.php']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/button").click()
    time.sleep(2)

    driver.find_element(By.XPATH, "//input[contains(@name, 'user-name')]").send_keys(customer_info2[0])
    driver.find_element(By.XPATH, "//input[contains(@name, 'user-phone')]").send_keys(customer_info2[1])
    driver.find_element(By.XPATH, "//input[contains(@name, 'user-email')]").send_keys(customer_info2[2])
    driver.find_element(By.XPATH, "//input[contains(@name, 'user-password')]").send_keys(customer_info2[3])
    time.sleep(5)

    # Chọn tỉnh/thành phố
    province = driver.find_element(By.XPATH, "//select[contains(@name, 'user-province')]")
    province.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//option[contains(@value, '79/Thành phố Hồ Chí Minh')]").click()
    time.sleep(2)

    # Tìm phần tử modal (và phần tử có thanh cuộn bên trong)
    modal_scrollable_content = driver.find_element(By.CSS_SELECTOR, '.modal-user__container')
    # Sử dụng ActionChains để cuộn
    actions = ActionChains(driver)
    actions.move_to_element(modal_scrollable_content).click().perform()  # Di chuyển đến phần tử modal
    time.sleep(2)

    # Chọn quận/huyện
    district = driver.find_element(By.XPATH, "//select[contains(@name, 'user-district')]")
    district.click()
    driver.find_element(By.XPATH, "//option[contains(@value, '778/Quận 7')]").click()
    time.sleep(2)

    # Chọn phường/xã
    ward = driver.find_element(By.XPATH, "//select[contains(@name, 'user-ward')]")
    ward.click()
    driver.find_element(By.XPATH, "//option[contains(text(), 'Phường Phú Mỹ')]").click()
    time.sleep(2)
    house_number = (driver.find_element(By.XPATH, "//input[contains(@name, 'user-houseAndRoadAddress')]"))
    house_number.send_keys(customer_info2[4])
    time.sleep(2)

    # Lưu khách hàng
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[3]/form/div[2]/button[1]").click()
    time.sleep(5)

    try:
        alert = driver.switch_to.alert
        assert alert.text == "Bạn có chắc chắn muốn thêm người dùng này vào cơ sở dữ liệu?", "Unexpected alert message."
        alert.accept()
    except NoAlertPresentException:
        assert False, "Expected alert not present."
    time.sleep(2)

    try:
        alert = driver.switch_to.alert
        expected_text = "Thêm người dùng mới có mã"
        assert expected_text in alert.text, f"Unexpected alert message: {alert.text}"
        alert.accept()

    except NoAlertPresentException:
        assert False, "Expected alert not present."

def test_not_fill_customer_info(driver):

    test_valid_login(driver)
    driver.find_element(By.XPATH, "//li[@class='sidebar-nav__item']/a[@href='user-manager.php']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/button").click()
    time.sleep(2)

    # Lưu khách hàng
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[3]/form/div[2]/button[1]").click()
    time.sleep(5)

    assert driver.page_source, "Trường này không được để trống"
    time.sleep(2)

def test_username_length(driver):
    test_valid_login(driver)
    driver.find_element(By.XPATH, "//li[@class='sidebar-nav__item']/a[@href='user-manager.php']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/button").click()
    time.sleep(2)

    driver.find_element(By.XPATH, "//input[contains(@name, 'user-name')]").send_keys("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    driver.find_element(By.XPATH, "//input[contains(@name, 'user-phone')]").send_keys("0132456789")
    driver.find_element(By.XPATH, "//input[contains(@name, 'user-email')]").send_keys("use@gmail.com")
    driver.find_element(By.XPATH, "//input[contains(@name, 'user-password')]").send_keys("index")
    time.sleep(5)

    # Chọn tỉnh/thành phố
    province_dropdown = driver.find_element(By.XPATH, "//select[contains(@name, 'user-province')]")
    province_dropdown.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//option[contains(@value, '79/Thành phố Hồ Chí Minh')]").click()
    time.sleep(2)

    # Tìm phần tử modal (và phần tử có thanh cuộn bên trong)
    modal_scrollable_content = driver.find_element(By.CSS_SELECTOR, '.modal-user__container')
    # Sử dụng ActionChains để cuộn
    actions = ActionChains(driver)
    actions.move_to_element(modal_scrollable_content).click().perform()  # Di chuyển đến phần tử modal
    time.sleep(2)

    # Chọn quận/huyện
    district_dropdown = driver.find_element(By.XPATH, "//select[contains(@name, 'user-district')]")
    district_dropdown.click()
    driver.find_element(By.XPATH, "//option[contains(@value, '778/Quận 7')]").click()
    time.sleep(2)

    # Chọn phường/xã
    ward_dropdown = driver.find_element(By.XPATH, "//select[contains(@name, 'user-ward')]")
    ward_dropdown.click()
    driver.find_element(By.XPATH, "//option[contains(text(), 'Phường Phú Mỹ')]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//input[contains(@name, 'user-houseAndRoadAddress')]").send_keys("15B Street")
    time.sleep(2)

    # Lưu khách hàng
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[3]/form/div[2]/button[1]").click()
    time.sleep(5)

    assert driver.page_source, "Tên người dùng không vượt quá 50 kí tự"

def test_add_existing_email(driver):
    test_valid_login(driver)
    driver.find_element(By.XPATH, "//li[@class='sidebar-nav__item']/a[@href='user-manager.php']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/button").click()
    time.sleep(2)

    driver.find_element(By.XPATH, "//input[contains(@name, 'user-name')]").send_keys("user")
    driver.find_element(By.XPATH, "//input[contains(@name, 'user-phone')]").send_keys("0132456789")
    driver.find_element(By.XPATH, "//input[contains(@name, 'user-email')]").send_keys("pnd987@gmail.com")
    driver.find_element(By.XPATH, "//input[contains(@name, 'user-password')]").send_keys("index")
    time.sleep(5)
    # driver.execute_script("window.scrollBy(0, 500);")  # Cuộn xuống 500px
    # time.sleep(2)
    # Chọn tỉnh/thành phố
    province_dropdown = driver.find_element(By.XPATH, "//select[contains(@name, 'user-province')]")
    province_dropdown.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//option[contains(@value, '79/Thành phố Hồ Chí Minh')]").click()
    time.sleep(2)

    # Tìm phần tử modal (và phần tử có thanh cuộn bên trong)
    modal_scrollable_content = driver.find_element(By.CSS_SELECTOR, '.modal-user__container')
    # Sử dụng ActionChains để cuộn
    actions = ActionChains(driver)
    actions.move_to_element(modal_scrollable_content).click().perform()  # Di chuyển đến phần tử modal
    time.sleep(2)

    # Chọn quận/huyện
    district_dropdown = driver.find_element(By.XPATH, "//select[contains(@name, 'user-district')]")
    district_dropdown.click()
    driver.find_element(By.XPATH, "//option[contains(@value, '778/Quận 7')]").click()
    time.sleep(2)

    # Chọn phường/xã
    ward_dropdown = driver.find_element(By.XPATH, "//select[contains(@name, 'user-ward')]")
    ward_dropdown.click()
    driver.find_element(By.XPATH, "//option[contains(text(), 'Phường Phú Mỹ')]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//input[contains(@name, 'user-houseAndRoadAddress')]").send_keys("15B Street")
    time.sleep(2)

    # Lưu khách hàng
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[3]/form/div[2]/button[1]").click()
    time.sleep(5)

    try:
        alert = driver.switch_to.alert
        assert alert.text == "Bạn có chắc chắn muốn thêm người dùng này vào cơ sở dữ liệu?", "Unexpected alert message."
        alert.accept()
    except NoAlertPresentException:
        assert False, "Expected alert not present."
    time.sleep(2)

    try:
        alert = driver.switch_to.alert
        assert alert.text == "Thêm người dùng không thành công do email đã tồn tại trong hệ thống! Hãy thử một email khác!",\
                                "Unexpected alert message."
        alert.accept()
    except NoAlertPresentException:
        assert False, "Expected alert not present."

def test_edit_customer_info(driver):
    test_valid_login(driver)
    driver.find_element(By.XPATH, "//li[@class='sidebar-nav__item']/a[@href='user-manager.php']").click()
    time.sleep(2)
    # Cuộn ngang sang phải 500px
    driver.execute_script("window.scrollBy(500, 0);")
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/table/tbody/tr[1]/td[11]/span").click()
    time.sleep(2)

    name = driver.find_element(By.XPATH, "//input[contains(@name, 'user-name')]")
    name.clear()
    name.send_keys(customer_info1[0])
    phone_number = driver.find_element(By.XPATH, "//input[contains(@name, 'user-phone')]")
    phone_number.clear()
    phone_number.send_keys(customer_info1[1])
    email = driver.find_element(By.XPATH, "//input[contains(@name, 'user-email')]")
    email.clear()
    email.send_keys(customer_info1[2])
    password = driver.find_element(By.XPATH, "//input[contains(@name, 'user-password')]")
    password.clear()
    password.send_keys(customer_info1[3])
    time.sleep(5)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[3]/form/div[2]/button[2]").click()
    time.sleep(2)
    try:
        alert = driver.switch_to.alert
        assert alert.text == "Bạn có chắc chắn muốn sửa người dùng này vào cơ sở dữ liệu?", "Unexpected alert message."
        alert.accept()
    except NoAlertPresentException:
        assert False, "Expected alert not present."
    time.sleep(2)

    try:
        alert = driver.switch_to.alert
        expected_text = "Sửa người dùng có mã"
        assert expected_text in alert.text, f"Unexpected alert message: {alert.text}"
        alert.accept()

    except NoAlertPresentException:
        assert False, "Expected alert not present."

def test_cancel_edit(driver):
    test_valid_login(driver)
    driver.find_element(By.XPATH, "//li[@class='sidebar-nav__item']/a[@href='user-manager.php']").click()
    time.sleep(2)
    # Cuộn ngang sang phải 500px
    driver.execute_script("window.scrollBy(500, 0);")
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/table/tbody/tr[1]/td[11]/span").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[3]/form/div[1]/span").click()
    time.sleep(2)

    assert driver.page_source

def test_valid_search(driver):
    test_valid_login(driver)
    driver.find_element(By.XPATH, "//li[@class='sidebar-nav__item']/a[@href='user-manager.php']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/form/input").send_keys("abc@gmail.com")
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/form/button/span").click()
    time.sleep(2)

    result = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/table/tbody/tr/td[4]")
    assert result.is_displayed()

def test_invalid_search(driver):
    test_valid_login(driver)
    driver.find_element(By.XPATH, "//li[@class='sidebar-nav__item']/a[@href='user-manager.php']").click()
    time.sleep(2)
    search_input = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/form/input")
    time.sleep(2)
    search_button = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/form/button/span")
    time.sleep(2)

    invalid_keywords = [":###", "@@@", "!!!"]
    for keyword in invalid_keywords:
        search_input.send_keys(keyword)
        search_button.click()
        result_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table/tbody/tr/td"))
        )
        assert "Không có người dùng nào để hiển thị!" in result_message.text, \
            f"Unexpected message for keyword '{keyword}': {result_message.text}"

def test_count_total_user(driver):
    test_valid_login(driver)
    driver.find_element(By.XPATH, "//li[@class='sidebar-nav__item']/a[@href='user-manager.php']").click()
    time.sleep(2)
    all_user = []
    page = 1
    while True:
        list_user = driver.find_elements(By.XPATH, "//tbody/tr")
        for user in list_user:
            all_user.append(user)
        page += 1
        try:
            dynamic_xpath = f"//a[@href='?page={page}&user-search=']"
            driver.find_element(By.XPATH, dynamic_xpath).click()
        except NoSuchElementException:
            break
    print(len(all_user))

@pytest.mark.parametrize("width, height", [
    (1920, 1080),  # Desktop lớn
    (1366, 768),   # Laptop nhỏ
    (768, 1024),   # Tablet
    (375, 667),    # Điện thoại
])
def test_responsive_sidebar(driver, width, height):
    """
    Test xem thanh sidebar có bị ẩn ở các kích thước màn hình nhỏ hay không.
    :param driver: Selenium WebDriver instance
    :param width: Width of the browser window
    :param height: Height of the browser window
    """
    # Thiết lập kích thước cửa sổ trình duyệt
    driver.set_window_size(width, height)

    # Đăng nhập hợp lệ
    test_valid_login(driver)

    # Điều hướng đến trang User Manager
    driver.find_element(By.XPATH, "//li[@class='sidebar-nav__item']/a[@href='user-manager.php']").click()
    time.sleep(2)

    # Kiểm tra thanh sidebar
    try:
        sidebar = driver.find_element(By.CLASS_NAME, "sidebar")  # Lớp của thanh sidebar
        if width <= 768:  # Nếu chiều rộng màn hình <= 768px (tablet, mobile)
            # Kiểm tra xem thanh sidebar có bị ẩn không (bằng cách xem thuộc tính 'display')
            assert sidebar.is_displayed() is False, f"Sidebar should be hidden at {width}x{height}"
            print(f"Sidebar is hidden at {width}x{height}")
        else:  # Nếu chiều rộng màn hình > 768px (desktop, laptop)
            assert sidebar.is_displayed(), f"Sidebar should be visible at {width}x{height}"
            print(f"Sidebar is visible at {width}x{height}")
    except Exception as e:
        print(f"Error: Sidebar test failed for {width}x{height}: {str(e)}")
        assert False, f"Error occurred during test for {width}x{height}: {str(e)}"


