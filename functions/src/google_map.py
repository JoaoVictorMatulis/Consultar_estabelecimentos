from selenium.webdriver.common.by import By
from functions.utils.logger import log_info, log_error
import time

def collect_data(driver, establishment_type_search, qtd_results = 10):
    """
        Recebe um tipo de estabelecimento e faz a consulta dele no google maps, 
        depois coleta os dados de cada estabelecimento encontrado conforme a quantidade informada.

        Args:
            driver: driver do navegador
            establishment_type_search: tipo de estabelecimento a ser buscado
            qtd_results: quantidade de resultados a serem coletados
        Returns:
            dicionário com os dados coletados
        Raises:
            ValueError: caso ocorra um erro ao coletar os dados
            Exception: caso ocorra um erro ao coletar os dados
            TimeoutError: caso ocorra um timeout ao coletar os dados
            TimeoutException: caso ocorra um timeout ao coletar os dados
            WebDriverException: caso ocorra um erro ao coletar os dados
            WebDriverWaitException: caso ocorra um erro ao coletar os dados
            WebDriverWaitTimeoutException: caso ocorra um timeout ao coletar os dados
            WebDriverWaitTimeoutException: caso ocorra um timeout ao coletar os dados
    """
    # XPaths dos elementos da página
    search_input_xpath = "//input[contains(@class ,'searchboxinput')]"
    establishment_name_xpath = "//h1[contains(@class ,'DUwDvf lfPIob')]"
    establishment_type_xpath = "//*[@id='QA0Szd']/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/span/span/button"
    establishment_rate_xpath = "//*[@id='QA0Szd']/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]"
    establishment_avaliation_count_xpath = "//*[@id='QA0Szd']/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]/span/span"
    establishment_address_xpath = "//*[contains(@data-item-id ,'address')]/div/div[2]/div[1]"
    close_button_xpath = "//*[@id='QA0Szd']/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div/div[3]/span/button"

    # Variáveis de controle
    search_loaded = False # Variável para verificar se a página de busca foi carregada
    index_inicial_result = 3 # Índice inicial dos resultados na página de busca
    max_load_attemps = 5 # Número máximo de tentativas de carregamento da página de busca
    load_attemps = 0 # Variável para o número de tentativas de carregamento da página de busca
    establishment_name = None # Variável para o nome do estabelecimento
    establishment_type = None # Variável para o tipo do estabelecimento
    establishment_rate = None # Variável para a taxa do estabelecimento
    establishment_avaliation_count = None # Variável para a quantidade de avaliações do estabelecimento
    establishment_address = None # Variável para o endereço do estabelecimento
    result_research = {} # Variável para armazenar os resultados da busca

    # A automação espera a página do google maps ser totalmente carregada antes de iniciar as buscas
    log_info(f"Iniciando a coleta de dados para o estabelecimento do tipo: {establishment_type_search}")
    log_info(f"Aguardando o carregamento da página")
    driver.wait_page_load(timeout=60)

    # Após a página ser carregada, a automação digita o texto passado como parâmetro na busca do estabelecimento
    # Exemplo: caso tenha sido colado na planilha a palavra "restaurante", a automação irá digitar "restaurante" na busca do estabelecimento
    log_info(f"Digitando o nome do estabelecimento")
    driver.type_into(by=By.XPATH, value=search_input_xpath, txt=establishment_type_search, send_enter=True)
    # Aqui espera três segundo só para dar um tempo para a página processar a solicitação de busca
    time.sleep(3)

    # Aqui a automação garante que a página fez a requisição da busca e retornou algum resultado
    log_info(f"Aguardando o carregamento da página de busca")
    while not search_loaded or load_attemps < max_load_attemps:
        log_info("Coletando o URL da página")
        current_url = driver.get_current_url()
        log_info(f"URL da página: {current_url}")
        # Por algum motivo a página do google maps não recarrega ou atualiza para mostrar esses resultados da busca, 
        # ela só atualiza a url e adiciona um campo de "/data=!3m1!4b1", não necessáriamente a data vem assim, ela pode ocorrer de vir como "/data=!4d1!3m1!4b1"
        # essa foi a unica maneira que achei para validar se a página realmente processou a busca e retornou algum resultado
        if "/data=" in current_url and "!3m1!4b1" in current_url:
            # Caso na url tenha sido encontrado o campo "/data=" e o campo "!3m1!4b1", significa que a página realmente processou a busca e retornou algum resultado
            log_info(f"Página de busca carregada com sucesso")
            search_loaded = True
            break
        # Caso não tenha sido encontrado o campo "/data=" e o campo "!3m1!4b1", significa que a página não processou a busca e não retornou nenhum resultado
        # Ou ela ainda está carregando os resultadas da busca
        log_info("Tela não foi carregada")
        load_attemps += 1
        time.sleep(0.5) # Aqui espera meio segundo para dar um tempo para a página processar a solicitação de busca

    # Caso a página não tenha sido carregada, a automação levanta um erro de timeout
    if not search_loaded:
        raise ValueError(f"Timeout ao carregar a página de busca do estabelecimento do tipo: {establishment_type_search}")

    # Caso a página tenha sido carregada, a automação coleta os dados de cada estabelecimento encontrado conforme a quantidade informada
    for i in range(qtd_results):
        log_info(f"Coletando o resultado {i+1}")
        # Variável para verificar se a janela do estabelecimento foi carregada
        window_loaded = False
        # Número máximo de tentativas de abrir a janela do estabelecimento
        max_attempts = 3
        attempts = 0

        # Nessa eu faço um loop para garantir que a janela do estabelecimento foi carregada
        while not window_loaded and attempts < max_attempts:
            # Esse xpath serve para clicar nos resultados da busca, onde cada estavelecimento tem um cartão e um index, que começa no número 3 e vai aumentando de 2 em 2
            base_div_results_xpath = f"/html/body/div[1]/div[2]/div[9]/div[8]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[{index_inicial_result}]"
            log_info(f"Abrindo janela do estabelecimento: {i+1}")
            driver.scroll_to_element(by=By.XPATH, value=base_div_results_xpath)
            driver.click_on_element(by=By.XPATH, value=base_div_results_xpath)
            text = driver.get_text(by=By.XPATH, value=base_div_results_xpath)
            establishment_name = driver.get_text(by=By.XPATH, value=establishment_name_xpath)
            # Aqui para entender se a Janela foi carregada ou não, eu estou usando o nome do estabelecimento que vem do base_div_results_xpath e do establishment_name_xpath, onde no base_div_results_xpath ele já vem com a maioria das informações do estabelecimento, porém não todas, então eu abro o cartão do estabelecimento e coleto o nome do estabelecimento que abriu no cartão, caso esse nome estaja dentro da lista do base_div_results_xpath, significa que a janela foi carregada com sucesso, caso contrário ele tentará abrir novamente o cartão.
            if(establishment_name in text and establishment_name != "" and establishment_name is not None):
                log_info(f"Janela carregada, nome do lugar: {establishment_name}")
                window_loaded = True
                time.sleep(1)
            else:
                log_error(f"Não foi possível encontrar o nome do estabelecimento na janela")
                log_error(f"Tentativa {attempts+1} de {max_attempts}")
                attempts += 1
                time.sleep(1)

        # Caso a janela não tenha sido carregada, a automação levanta um erro de timeout
        if not window_loaded:
            raise ValueError(f"Timeout ao carregar a janela do estabelecimento: {i+1}")
        
        log_info(f"Janela do estabelecimento carregada com sucesso")

        # Aqui eu coleto o resto das informações que estão faltando, como o tipo do estabelecimento, a nota da avaliação, a quantidade de avaliações e o endereço completo do estabelecimento.
        establishment_type = driver.get_text(by=By.XPATH, value=establishment_type_xpath)
        establishment_rate = driver.get_text(by=By.XPATH, value=establishment_rate_xpath)
        establishment_avaliation_count = driver.get_text(by=By.XPATH, value=establishment_avaliation_count_xpath)
        establishment_address = driver.get_text(by=By.XPATH, value=establishment_address_xpath)

        # Aqui eu imprimo as informações coletadas
        log_info(f"Nome do estabelecimento: {establishment_name}")
        log_info(f"Tipo do estabelecimento: {establishment_type}")
        log_info(f"Taxa do estabelecimento: {establishment_rate}")
        log_info(f"Quantidade de avaliações do estabelecimento: {establishment_avaliation_count}")
        log_info(f"Endereço do estabelecimento: {establishment_address}")

        # Aqui eu armazeno as informações coletadas em um dicionário
        result_research[i] = {
            "establishment_name": establishment_name,
            "establishment_type": establishment_type,
            "establishment_rate": establishment_rate,
            "establishment_avaliation_count": establishment_avaliation_count,
            "establishment_address": establishment_address
        }

        # Aqui eu incremento o índice inicial dos resultados para a próxima iteração
        index_inicial_result += 2
        # Aqui eu fecho a janela do estabelecimento, para garantir que a automação não confuda o cartão do proximo estabelecimento com do cartão que acabei de coletar os dados.
        driver.click_on_element(by=By.XPATH, value=close_button_xpath)
        time.sleep(1)    

    # Após todas as iterações, a automação retorna o dicionário com os dados coletados
    return result_research