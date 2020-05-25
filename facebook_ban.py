from selenium import webdriver
from bs4 import BeautifulSoup
import selenium
import time


def click_btns(x_path, i, cnt_error):
    if cnt_error == 20: return False

    try:
        driver.find_element_by_xpath(x_path[i]).click()
        return True
    except selenium.common.exceptions.NoSuchElementException:
        return click_btns(x_path, (i + 1) % len(x_path), cnt_error + 1)
    except selenium.common.exceptions.ElementNotInteractableException:
        return click_btns(x_path, (i + 1) % len(x_path), cnt_error + 1)


def click_btn(x_path, cnt_error):
    if cnt_error == 20: return False

    try:
        driver.find_element_by_xpath(x_path).click()
        return True
    except selenium.common.exceptions.NoSuchElementException:
        return click_btn(x_path, cnt_error + 1)
    except selenium.common.exceptions.ElementNotInteractableException:
        return click_btn(x_path, cnt_error + 1)


# 버튼
btns_login = ["//*[@id=\"u_0_b\"]", '//*[@id="u_0_e"]']
btns_plus = [
    "//*[@id=\"mount_0_0\"]/div/div/div[3]/div/div/div[1]/div/div/div/div[3]/div[1]/div/div/div/div[2]/div/div/div[4]/div/div[1]/div"
    ,
    "//*[@id=\"mount_0_0\"]/div/div/div[3]/div/div/div[1]/div/div/div/div[3]/div[1]/div/div/div/div[2]/div/div/div[3]/div/div[1]/div"
    ,
    "//*[@id=\"mount_0_0\"]/div/div/div[3]/div/div/div[1]/div/div/div/div[3]/div[1]/div/div/div/div[2]/div/div/div[2]/div/div[1]/div"]
btns_ban = [
    "//*[@id=\"mount_0_0\"]/div/div/div[3]/div/div/div[1]/div/div/div/div[3]/div[2]/div/div/div[1]/div[1]/div/div/div/div[1]/div/div[1]/div[3]/div[2]"
    ,
    "//*[@id=\"mount_0_0\"]/div/div/div[3]/div/div/div[1]/div/div/div/div[3]/div[2]/div/div/div[1]/div[1]/div/div/div/div[1]/div/div[1]/div[2]/div[2]"]
btn_banban = "//*[@id=\"mount_0_0\"]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[7]/div/div/div[1]/div/span"

# 웹 드라이버 실행
driver = webdriver.Chrome('c:/chromedriver.exe')
driver.get('https://facebook.com')

# 로그인
userid = input("아이디 : ")
userpw = input("비밀번호 : ")

driver.find_element_by_name('email').send_keys(userid)
driver.find_element_by_name('pass').send_keys(userpw)
click_btns(btns_login, 0, 0)
time.sleep(0.5)

# 친구목록 차단할 페이지
main_page = input("차단할 페이지 : ")
driver.get(main_page)

# 스크롤 내리기
SCROLL_PAUSE_TIME = 2

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(SCROLL_PAUSE_TIME)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
    time.sleep(SCROLL_PAUSE_TIME)

    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        break

    last_height = new_height

# 친구 페이지 목록 크롤링
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
sources = soup.select('html>body>div>div>div>div>div>div>div>div>div>div>div>div>div>div>div>div>div>div>div>a')

pages = []
for source in sources:
    page = str(source)[414:]
    if page[:4] != "http": continue

    idx = 0
    for c in page:
        if c == "\"": break
        idx += 1

    pages.append(page[:idx])

# 실행 탭 추가
driver.execute_script('window.open("about:blank", "_blank");')
tabs = driver.window_handles
driver.switch_to_window(tabs[1])


def ban(page):
    driver.get(page)
    time.sleep(1)

    if click_btns(btns_plus, 0, 0) == False: return
    time.sleep(0.5)

    if click_btns(btns_ban, 0, 0) == False: return
    time.sleep(0.5)

    if click_btn(btn_banban, 0) == False: return


# 페이지 실행 & 차단
for page in pages:
    ban(page)
