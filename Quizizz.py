from selenium import webdriver # pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from multiprocessing import Pool
import string, random, requests

class quizizzBot:
    def __init__(self, join_code, join_url='https://quizizz.com/join?ref=header_tab&lng=en'):
        self.__version__ = '23.9.4'
        self.join_code = join_code
        self.join_url = join_url
        self.checkStatus(self.join_url)

    def checkStatus(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.status_code
        except requests.ConnectionError as conError:
            raise RuntimeError("Failed to establish a connection. Please check the URL and your network connection.") from conError
        except requests.HTTPError as httpError:
            raise RuntimeError(f"HTTP Error: {httpError}") from httpError

    def generateBotName(self, min_chr, max_chr):
        length = random.randint(min_chr, max_chr)
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    def listPlayer(self, show_listPlayer=True, max_waitTime=30):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--log-level=3')  # Set log level to suppress console output

        name = 'id is not defined'
        options.headless = True

        driver = webdriver.Edge(options=options)
        driver.get(self.join_url)

        # -------------- Join Code Page --------------
        code_input = WebDriverWait(driver, max_waitTime).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-cy="gamecode-field"]'))
            )
        join_button = driver.find_element(By.CSS_SELECTOR, 'button[data-cy="joinGame-button"]')

        code_input.send_keys(str(self.join_code))
        join_button.click()
        
        # -------------- Input Name Page --------------
        try:
            name_input = WebDriverWait(driver, max_waitTime).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-cy="enter-name-field"]'))
                )
            start_button = driver.find_element(By.CSS_SELECTOR, 'button[data-cy="start-game-button"]')
        except TimeoutException:
            print("Check if the join code is correct or The website might have updated its structure.")
            return

        name_input.send_keys(str(name))
        start_button.click()
        
        # -------------- Alert Confirm Check Popup --------------
        retries_count = 0
        while retries_count < 3:
            try:
                player_field = WebDriverWait(driver, max_waitTime).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'name'))
                    )
                break
            except (TimeoutException,UnboundLocalError):
                try:
                    alertConfirm_button = WebDriverWait(driver, max_waitTime).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-cy="confirm"]'))
                        )
                    alertConfirm_button.click()
                except (TimeoutException,UnboundLocalError):
                    retries_count += 1
                    if retries_count >= 3:
                        print(f"The request was Unsuccessful.")
                        return

        # -------------- Waiting Room Page --------------
        waiting_rome_page = BeautifulSoup(driver.page_source, "html.parser")
        player_field = waiting_rome_page.find('div' ,{'class':"players-grid"})
        player_names = player_field.find_all('span')

        playerNames_list = []

        for order, player_name_tag in enumerate(player_names):
            name_text = player_name_tag.get_text()
            if show_listPlayer:
                print(f"{order+1}) {name_text}")
            playerNames_list.append(name_text)

        if not playerNames_list:
            print("No players in this room yet.")

        driver.quit()
        return playerNames_list


    def dummy(self, name, makeAutoExam=False, max_waitTime=30):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--log-level=3')  # Set log level to suppress console output

        options.headless = True
        id_status = 'No access'

        driver = webdriver.Edge(options=options)
        driver.get(self.join_url)

        # -------------- Join Code Page --------------
        code_input = WebDriverWait(driver, max_waitTime).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-cy="gamecode-field"]'))
            )
        join_button = driver.find_element(By.CSS_SELECTOR, 'button[data-cy="joinGame-button"]')

        code_input.send_keys(str(self.join_code))
        join_button.click()
        
        # -------------- Input Name Page --------------
        try:
            name_input = WebDriverWait(driver, max_waitTime).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-cy="enter-name-field"]'))
                )
            start_button = driver.find_element(By.CSS_SELECTOR, 'button[data-cy="start-game-button"]')
        except TimeoutException:
            print("Check if the join code is correct or The website might have updated its structure.")
            print(f"{id_status}: {name}")
            return

        name_input.send_keys(str(name))
        start_button.click()
        
        # -------------- Alert Confirm Check Popup --------------
        retries_count = 0
        while retries_count < 3:
            try:
                player_field = WebDriverWait(driver, max_waitTime).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'name'))
                    )
                if id_status != 'Dupicate access':
                    id_status = 'Access'
                break
            except (TimeoutException,UnboundLocalError):
                try:
                    alertConfirm_button = WebDriverWait(driver, max_waitTime).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-cy="confirm"]'))
                        )
                    alertConfirm_button.click()
                    id_status = 'Duplicate access'
                except (TimeoutException,UnboundLocalError):
                    retries_count += 1
                    if retries_count >= 3:
                        print(f"{id_status}: {name}")
                        return                    

        # -------------- Waiting Room Page --------------
        player_name = player_field.text

        print(f"{id_status}: {player_name}")

        if makeAutoExam:
            pass

        driver.quit()


    def mutiDummy(self, num_processes, NameList=[], makeAutoExam=False, max_waitTime=30):
        if __name__ == '__main__':
            # Use the pool to run the dummy function concurrently
            if len(NameList) == 0 :
                botvirus_names = [self.generateBotName(8, 11) for _ in range(num_processes)]
                args_list = [(name, makeAutoExam, max_waitTime) for name in botvirus_names]
                with Pool(processes=num_processes) as pool:
                    pool.starmap(self.dummy, args_list)
            else:
                args_list = [(name, makeAutoExam, max_waitTime) for name in NameList]
                with Pool(processes=num_processes) as pool:
                    pool.starmap(self.dummy, args_list)
                # pool.map(self.dummy, [name+str(id) for id in range(1, 1+num_processes)])

            # Close the pool of worker processes
            # pool.close()
            # pool.join()