import os
import json
import pandas as pd

def read_excel(filepath, header_row: int | None = None, sheet_name: str | int | None = None):
    """
    Lê um arquivo Excel e retorna um DataFrame.

    Args:
        filepath (str): Caminho do arquivo Excel.
        header_row (int): Número da linha que contém os cabeçalhos das colunas.
        sheet_name (str): Nome da planilha a ser lida.

    Returns:
        pd.DataFrame: DataFrame com os dados da planilha.
    """
    try:
        ext = os.path.splitext(filepath)[1].lower()
        # Pandas usa índice baseado em 0 para header; config usa baseado em 1
        header_idx = (header_row - 1) if header_row and header_row > 0 else 0
        if ext == '.xlsx':
            return pd.read_excel(filepath, engine='openpyxl', header=header_idx, sheet_name=sheet_name)
        elif ext == '.xls':
            return pd.read_excel(filepath, engine='xlrd', header=header_idx, sheet_name=sheet_name)
        else:
            raise ValueError("Formato de Excel não suportado")
    except Exception as e:
        raise ValueError(f"Erro ao ler a planilha: {e}")

def write_json(data, filepath):
    """
    Escreve um dicionário em um arquivo JSON.

    Args:
        data (dict): Dicionário a ser escrito.
        filepath (str): Caminho do arquivo JSON.
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        raise ValueError(f"Erro ao escrever o arquivo JSON: {e}")

def json_to_excel(data, filepath):
    """
    Converte um dicionário em um DataFrame e salva em um arquivo Excel.

    Args:
        data (dict): Dicionário a ser convertido.
        filepath (str): Caminho do arquivo Excel.
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Dicionário de mapeamento para traduzir nomes das colunas
        column_mapping = {
            'categoria': 'Categoria',
            'establishment_name': 'Nome do Estabelecimento',
            'establishment_type': 'Tipo do Estabelecimento',
            'establishment_rate': 'Avaliação',
            'establishment_avaliation_count': 'Quantidade de Avaliações',
            'establishment_address': 'Endereço'
        }
        
        # Transformar o dicionário aninhado em uma lista de dicionários planos
        rows = []
        for category, establishments in data.items():
            for idx, establishment_data in establishments.items():
                row = {
                    'categoria': category,
                    **establishment_data  # Desempacota os dados do estabelecimento (sem incluir 'indice')
                }
                rows.append(row)
        
        # Criar DataFrame
        df = pd.DataFrame(rows)
        
        # Renomear as colunas usando o mapeamento
        df = df.rename(columns=column_mapping)
        
        # Reordenar as colunas na ordem desejada (opcional)
        desired_order = ['Categoria', 'Nome do Estabelecimento', 'Tipo do Estabelecimento', 
                        'Avaliação', 'Quantidade de Avaliações', 'Endereço']
        # Filtrar apenas as colunas que existem no DataFrame
        desired_order = [col for col in desired_order if col in df.columns]
        df = df[desired_order]
        
        # Salvar no Excel
        df.to_excel(filepath, index=False, engine='openpyxl')
        return True
    except Exception as e:
        raise ValueError(f"Erro ao converter o JSON para Excel: {e}")