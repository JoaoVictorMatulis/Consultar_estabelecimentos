from selenium.webdriver.common.by import By
from functions.utils.logger import log_info, log_error
import time

def collect_data(driver, establishment_type_search, qtd_results = 10):
    search_input_xpath = "//input[contains(@class ,'searchboxinput')]"
    establishment_name_xpath = "//h1[contains(@class ,'DUwDvf lfPIob')]"
    establishment_type_xpath = "//*[@id='QA0Szd']/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/span/span/button"
    establishment_rate_xpath = "//*[@id='QA0Szd']/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]"
    establishment_avaliation_count_xpath = "//*[@id='QA0Szd']/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]/span/span"
    establishment_address_xpath = "//*[contains(@data-item-id ,'address')]/div/div[2]/div[1]"
    close_button_xpath = "//*[@id='QA0Szd']/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div/div[3]/span/button"
    search_loaded = False
    index_inicial_result = 3
    load_timeout = 5
    load_attemps = 0
    establishment_name = None
    establishment_type = None
    establishment_rate = None
    establishment_avaliation_count = None
    establishment_address = None
    result_research = {}

    log_info(f"Iniciando a coleta de dados para o estabelecimento do tipo: {establishment_type_search}")
    log_info(f"Aguardando o carregamento da página")
    driver.wait_page_load(timeout=60)

    log_info(f"Digitando o nome do estabelecimento")
    driver.type_into(by=By.XPATH, value=search_input_xpath, txt=establishment_type_search, send_enter=True)

    log_info(f"Aguardando o carregamento da página de busca")
    time.sleep(3)

    while not search_loaded or load_attemps < load_timeout:
        log_info("Coletando o URL da página")
        current_url = driver.get_current_url()
        log_info(f"URL da página: {current_url}")
        if "/data=" in current_url and "!3m1!4b1" in current_url:
            log_info(f"Página de busca carregada com sucesso")
            search_loaded = True
            break
        log_info("Tela não foi carregada")
        load_attemps += 1
        time.sleep(0.5)

    if not search_loaded:
        raise ValueError(f"Timeout ao carregar a página de busca do estabelecimento do tipo: {establishment_type_search}")

    log_info(f"Página de busca carregada com sucesso")
    log_info(f"Coletando os dados dos resultados")

    for i in range(qtd_results):
        log_info(f"Coletando o resultado {i+1}")
        window_loaded = False
        max_attempts = 3
        attempts = 0
        while not window_loaded and attempts < max_attempts:
            base_div_results_xpath = f"/html/body/div[1]/div[2]/div[9]/div[8]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[{index_inicial_result}]"
            log_info(f"Abrindo janela do estabelecimento: {i+1}")
            driver.scroll_to_element(by=By.XPATH, value=base_div_results_xpath)
            driver.click_on_element(by=By.XPATH, value=base_div_results_xpath)
            text = driver.get_text(by=By.XPATH, value=base_div_results_xpath)
            establishment_name = driver.get_text(by=By.XPATH, value=establishment_name_xpath)
            if(establishment_name in text and establishment_name != "" and establishment_name is not None):
                log_info(f"Janela carregada, nome do lugar: {establishment_name}")
                window_loaded = True
                time.sleep(1)
            else:
                log_error(f"Não foi possível encontrar o nome do estabelecimento na janela")
                log_error(f"Tentativa {attempts+1} de {max_attempts}")
                attempts += 1
                time.sleep(1)

        if not window_loaded:
            raise ValueError(f"Timeout ao carregar a janela do estabelecimento: {i+1}")
        
        log_info(f"Janela do estabelecimento carregada com sucesso")

        establishment_type = driver.get_text(by=By.XPATH, value=establishment_type_xpath)
        establishment_rate = driver.get_text(by=By.XPATH, value=establishment_rate_xpath)
        establishment_avaliation_count = driver.get_text(by=By.XPATH, value=establishment_avaliation_count_xpath)
        establishment_address = driver.get_text(by=By.XPATH, value=establishment_address_xpath)

        log_info(f"Nome do estabelecimento: {establishment_name}")
        log_info(f"Tipo do estabelecimento: {establishment_type}")
        log_info(f"Taxa do estabelecimento: {establishment_rate}")
        log_info(f"Quantidade de avaliações do estabelecimento: {establishment_avaliation_count}")
        log_info(f"Endereço do estabelecimento: {establishment_address}")

        result_research[i] = {
            "establishment_name": establishment_name,
            "establishment_type": establishment_type,
            "establishment_rate": establishment_rate,
            "establishment_avaliation_count": establishment_avaliation_count,
            "establishment_address": establishment_address
        }

        index_inicial_result += 2
        driver.click_on_element(by=By.XPATH, value=close_button_xpath)
        time.sleep(1)    

    return result_research