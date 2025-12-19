from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time


class WebAutomation:
    """
    Framework padrão para automação web com Selenium.
    """

    def __init__(self):
        self.__webDriver = None
        self.__chrome_options = webdriver.ChromeOptions()
        self.__last_config = {}
        self.__download_path = None

    # ========================
    # 1 - NAVEGAÇÃO
    # ========================

    def startWebDriver(self, anonimo=False, iniciar_maximizado=True, mostra_janela_chrome=True,
                       bloquear_popup=False, bloquear_notificacoes=False, desativar_extensoes=False,
                       desativar_infobar=False, desativar_sandbox=False, sistema_linux=False,
                       chrome_log_message=True, chrome_driver_path=os.getcwd()+"\\chromedriver.exe",page_load_strategy="normal"):
        """
        Inicia o navegador Chrome com as configurações especificadas.

        Args:
            anonimo (bool): Se True, inicia o navegador em modo anônimo.
            iniciar_maximizado (bool): Se True, inicia o navegador maximizado.
            mostra_janela_chrome (bool): Se True, mostra a janela do navegador.
            bloquear_popup (bool): Se True, bloqueia as popups.
            bloquear_notificacoes (bool): Se True, bloqueia as notificações.
            desativar_extensoes (bool): Se True, desativa as extensões.
            desativar_infobar (bool): Se True, desativa a barra de informações.
            desativar_sandbox (bool): Se True, desativa o sandbox.
            sistema_linux (bool): Se True, inicia o navegador no sistema Linux.
            chrome_log_message (bool): Se True, exibe as mensagens do Chrome.
            chrome_driver_path (str): Caminho do driver do Chrome.
            page_load_strategy (str): Estratégia de carregamento da página.
            
        Returns:
            webdriver.Chrome: O driver do Chrome.
        """

        # salva config para poder reutilizar na função restart_browser()
        self.__last_config = {
            "anonimo": anonimo,
            "iniciar_maximizado": iniciar_maximizado,
            "mostra_janela_chrome": mostra_janela_chrome,
            "bloquear_popup": bloquear_popup,
            "bloquear_notificacoes": bloquear_notificacoes,
            "desativar_extensoes": desativar_extensoes,
            "desativar_infobar": desativar_infobar,
            "desativar_sandbox": desativar_sandbox,
            "sistema_linux": sistema_linux,
            "chrome_log_message": chrome_log_message,
            "chrome_driver_path": chrome_driver_path,
            "page_load_strategy": page_load_strategy,
        }

        # configurações do Chrome
        self.__chrome_options = webdriver.ChromeOptions()
        self.__chrome_options.page_load_strategy = page_load_strategy

        if anonimo:
            self.__chrome_options.add_argument("--incognito")
        if iniciar_maximizado:
            self.__chrome_options.add_argument("--start-maximized")
        if not mostra_janela_chrome:
            self.__chrome_options.add_argument("--headless=new")
        if bloquear_popup:
            self.__chrome_options.add_argument("--disable-popup-blocking")
        if bloquear_notificacoes:
            self.__chrome_options.add_argument("--disable-notifications")
        if desativar_extensoes:
            self.__chrome_options.add_argument("--disable-extensions")
        if desativar_infobar:
            self.__chrome_options.add_argument("--disable-infobars")
        if desativar_sandbox:
            self.__chrome_options.add_argument("--no-sandbox")
        if sistema_linux:
            self.__chrome_options.add_argument("--disable-dev-shm-usage")
        if chrome_log_message:
            self.__chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            self.__chrome_options.add_argument("--log-level=3")

        if self.__download_path:
            prefs = {
                "download.default_directory": self.__download_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            self.__chrome_options.add_experimental_option("prefs", prefs)

        # inicia webdriver
        self.__webDriver = webdriver.Chrome(options=self.__chrome_options)
        return self.__webDriver

    def wait_page_load(self, timeout=30):
        """
        Aguarda o carregamento completo da página.

        Args:
            timeout (int): Tempo máximo de espera em segundos.
        """
        hora_inicio = time.time()
        while time.time() - hora_inicio < timeout:
            page_state = self.__webDriver.execute_script("return document.readyState")
            if page_state == "complete":
                return True
            time.sleep(0.5)
        return False

    def closer_chrome(self):
        """
        Fecha o navegador Chrome.
        """
        if self.__webDriver:
            self.__webDriver.quit()
            self.__webDriver = None

    def restart_browser(self):
        """
        Reinicia completamente o navegador com a última configuração usada no startWebDriver.
        """

        if not self.__last_config:
            raise RuntimeError("Nenhuma configuração encontrada. Você precisa chamar startWebDriver() primeiro.")
        self.closer_chrome()

        return self.startWebDriver(**self.__last_config)    

    def open_url(self, url, wait_load=True, timeout=30):
        """
        Abre uma URL no navegador Chrome.

        Args:
            url (str): URL a ser aberta.
            wait_load (bool): Se True, espera o carregamento da página.
            timeout (int): Tempo máximo de espera em segundos.
        """
        self.__webDriver.get(url)
        if wait_load:
            self.wait_page_load(timeout)

    def get_current_url(self):
        """
        Retorna a URL atual do navegador Chrome.
        """
        return self.__webDriver.current_url

    # ========================
    # 2 - ELEMENTOS
    # ========================

    def click_on_element(self, by=None, value=None, element=None, simulate_click=True, timeout=30):
        """
        Clica em um elemento da página.

        Args:
            by (str): Seletor CSS ou XPath.
            value (str): Valor do seletor.
            element (WebElement): Elemento da página.
            simulate_click (bool): Se True, simula o clique com o mouse.
            timeout (int): Tempo máximo de espera em segundos.
        """
        if by is not None and value is not None:
            element = self.wait_element(by, value, timeout)            
        if simulate_click and element is not None:
            element.click()
        elif simulate_click is False and element is not None:
            self.__webDriver.execute_script("arguments[0].click();", element)
        else:
            raise ValueError("É necessário fornecer 'by' e 'value' ou 'element'.")

    def type_into(self, by=None, value=None, element=None, txt=None, limpar=True, timeout=30, send_enter=False, time_sleep_enter = 0):
        """
        Digita um texto em um campo da página.

        Args:
            by (str): Seletor CSS ou XPath.
            value (str): Valor do seletor.
            element (WebElement): Elemento da página.
            txt (str): Texto a ser digitado.
            limpar (bool): Se True, limpa o campo antes de digitar.
            timeout (int): Tempo máximo de espera em segundos.
            send_enter (bool): Se True, envia um Enter após digitar.
            time_sleep_enter (int): Tempo de espera em segundos após enviar o Enter.
        """
        if txt is None:
            raise ValueError("O texto para digitar não pode ser None.")
        if by is not None and value is not None:
            campo = self.wait_element(by=by, value=value,timeout=timeout)
        elif element is not None:
            campo = element
        else:
            raise ValueError("É necessário fornecer 'by' e 'value' ou 'element'.")
        if limpar:
            # campo.clear()
            campo.send_keys(Keys.CONTROL + "a")
            campo.send_keys(Keys.DELETE)
        campo.send_keys(txt)
        if send_enter:
            if time_sleep_enter > 0:
                time.sleep(time_sleep_enter)
            campo.send_keys(Keys.ENTER)

    def scroll_to_element(self, by=None, value=None, element=None, timeout=30):
        """
        Scrolla até um elemento da página.

        Args:
            by (str): Seletor CSS ou XPath.
            value (str): Valor do seletor.
            element (WebElement): Elemento da página.
            timeout (int): Tempo máximo de espera em segundos.
        """
        if by is not None and value is not None:
            element = self.wait_element(by=by, value=value,timeout=timeout)
        self.__webDriver.execute_script("arguments[0].scrollIntoView();", element)

    def get_text(self, by=None, value=None, element=None):
        """
        Retorna o texto de um elemento da página.

        Args:
            by (str): Seletor CSS ou XPath.
            value (str): Valor do seletor.
            element (WebElement): Elemento da página.
        """
        try:
            if by is not None and value is not None:
                el = self.__webDriver.find_element(by=by, value=value)
                return el.text if el.text.strip() else ""
            elif element is not None:
                return element.text if element.text.strip() else ""
        except Exception:
            # Se não achar nada, retorna vazio também
            return ""
        return ""

    # ========================
    # 3 - ESPERAS
    # ========================

    def wait_element(self, by, value, timeout=30):
        """
        Espera por um elemento da página.

        Args:
            by (str): Seletor CSS ou XPath.
            value (str): Valor do seletor.
            timeout (int): Tempo máximo de espera em segundos.
        """
        hora_comeco = time.time()
        while (time.time() - hora_comeco) < timeout:
            try:
                return self.__webDriver.find_element(by=by, value=value)
            except:
                time.sleep(0.5)
        return None