import logging
import os
from datetime import datetime

def setup_logging(dir_path="logs"):
    """
    Configura o logger para registrar mensagens em um arquivo e no console.
    O arquivo de log é nomeado com a data atual.
    """
    # Criar pasta de logs (se não existir)
    os.makedirs(dir_path, exist_ok=True)

    # Nome do arquivo de log com data
    log_file = os.path.join(dir_path, f"log_{datetime.now().strftime('%Y%m%d')}.log")

    # Configuração básica
    logging.basicConfig(
        level=logging.INFO,  # Nível mínimo (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),  # salva em arquivo
            logging.StreamHandler()  # mostra no console também
        ]
    )

def log_info(msg):
    get_logger().info(msg)

def log_error(msg):
    get_logger().error(msg)

# Função para obter logger em qualquer lugar
def get_logger(name="main"):
    return logging.getLogger(name)