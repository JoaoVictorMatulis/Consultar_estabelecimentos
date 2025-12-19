from functions.utils import selenium_web
from functions.src.google_map import collect_data
from functions.utils.logger import log_info, log_error, setup_logging
from functions.utils.file_manager import read_excel, write_json, json_to_excel
import time
import os
import tomllib

def _substituir_diretorios(obj, base_dir: str):
    """
    Substitui os diretórios na configuração
    @param obj: objeto a ser substituído
    @param base_dir: diretório base
    @return: objeto substituído
    """
    if isinstance(obj, str):
        return obj.replace("|Diretorio_atual|", base_dir).replace("{base_dir}", base_dir)
    if isinstance(obj, list):
        return [_substituir_diretorios(x, base_dir) for x in obj]
    if isinstance(obj, dict):
        return {k: _substituir_diretorios(v, base_dir) for k, v in obj.items()}
    return obj

def carregar_config():
    """
    Carrega a configuração do programa
    @return: config
    """
    base_dir = os.getcwd()
    if os.path.exists("config.toml") and tomllib is not None:
        with open("config.toml", "rb") as f:
            return _substituir_diretorios(tomllib.load(f), base_dir)
    else:
        raise FileNotFoundError("Arquivo config.toml não encontrado")

def main():
    config = carregar_config()
    url_google_maps = "https://www.google.com/maps"

    # Aqui é configurado o logger e criado o arquivo de log
    setup_logging()

    log_info("=============== Iniciando o programa ===============")
    log_info("Iniciando a leitura da planilha")

    # Faz leitura da planilha de casos
    planilha = read_excel(filepath = config["planilha_atuacao"]["caminho_planilha"], header_row = 1, sheet_name = config["planilha_atuacao"]["nome_aba"])    
    log_info(f"Planilha lida com sucesso")

    log_info(f"Inicinado o driver")
    driver = selenium_web.WebAutomation()
    driver.startWebDriver()

    log_info(f"Abrindo o Google Maps")
    driver.open_url(url_google_maps)    
    log_info(f"Google Maps aberto")
    
    # Variaveis de controle
    tentativas = 0 # Essa variável é usada para contar as tentativas de coleta de dados
    tentativas_maximas = config["base"]["tentativas_maximas"] # Essa variável é usada para definir o número máximo de tentativas de coleta de dados
    full_result_research = {} # Essa variável é usada para armazenar os resultados da coleta de dados

    # Loop principal
    for index, row in planilha.iterrows():
        # Resetando as variáveis de controle
        tentativas = 0
        while tentativas < tentativas_maximas:
            try:
                establishment_name = row[config["planilha_atuacao"]["coluna_estabeleciomento"]]
                qtd_results = row[config["planilha_atuacao"]["coluna_qtd"]]
                result_research = collect_data(driver, establishment_name, qtd_results)
                full_result_research[establishment_name] = result_research
                log_info(f"Dados coletados para o estabelecimento: {establishment_name}")
                log_info(f"Dados coletados: {result_research}")
                break
            except Exception as e:
                    log_error(f"Erro ao coletar dados: {e}")
                    tentativas += 1
                    log_info("Reiniciando o navegador")
                    driver.restart_browser()
                    driver.open_url(url_google_maps)
                    time.sleep(1)
    log_info(f"Todos os dados coletados: {full_result_research}")
    write_json(full_result_research, config["arquivos"]["resultados_json"])
    log_info(f"Arquivo JSON escrito com sucesso")
    json_to_excel(full_result_research, config["arquivos"]["resultados_excel"])
    log_info(f"Arquivo Excel escrito com sucesso")

    log_info(f"Fechando o driver")
    driver.closer_chrome()
    log_info(f"=============== Fim do programa ===============")

if __name__ == "__main__":
    main()