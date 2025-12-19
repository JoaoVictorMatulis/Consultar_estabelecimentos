# Consultar Estabelecimentos - RPA Google Maps

Bot de automação (RPA) desenvolvido em Python que realiza consultas automatizadas no Google Maps para coletar informações sobre estabelecimentos comerciais.

## 📋 Descrição

Este projeto automatiza a busca de estabelecimentos no Google Maps, coletando informações detalhadas como:

- Nome do estabelecimento
- Tipo/Categoria do estabelecimento
- Nota do estabelecimento
- Quantidade de avaliações
- Endereço completo

Os dados são coletados a partir de uma planilha Excel de entrada e salvos em formato JSON e Excel para análise posterior.

## ✨ Funcionalidades

- ✅ Automação completa do navegador Chrome usando Selenium
- ✅ Leitura de planilha Excel com estabelecimentos e quantidades de resultados
- ✅ Busca automatizada no Google Maps
- ✅ Coleta de dados estruturados dos estabelecimentos
- ✅ Sistema de retry automático em caso de falhas
- ✅ Logging completo de todas as operações
- ✅ Exportação dos resultados em JSON e Excel
- ✅ Configuração flexível via arquivo TOML

## 🛠️ Requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- ChromeDriver (incluído no projeto)
- Dependências Python (ver seção de instalação)

## 📦 Instalação

1. **Clone ou baixe o repositório:**

```bash
git clone <url-do-repositorio>
cd Consultar_estabelecimentos
```

2. **Crie um ambiente virtual (recomendado):**

```bash
python -m venv venv
```

3. **Ative o ambiente virtual:**

   - **Windows (PowerShell):**

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   - **Windows (CMD):**

   ```cmd
   venv\Scripts\activate.bat
   ```

   - **Linux/Mac:**

   ```bash
   source venv/bin/activate
   ```
4. **Instale as dependências:**

```bash
pip install selenium pandas openpyxl xlrd
```

## ⚙️ Configuração

O projeto utiliza o arquivo `config.toml` para configurações. Edite este arquivo conforme suas necessidades:

```toml
[base]
tentativas_maximas = 3

[arquivos]
resultados_json = "|Diretorio_atual|/data/results/resultados.json"
resultados_excel = "|Diretorio_atual|/data/results/resultados.xlsx"

[planilha_atuacao]
caminho_planilha = "|Diretorio_atual|/data/data.xlsx"
nome_aba = "Plan1"
coluna_estabeleciomento = "Estabelecimento"
coluna_qtd = "Quantidade"
```

### Parâmetros de Configuração

- **tentativas_maximas**: Número máximo de tentativas em caso de erro durante a coleta
- **resultados_json**: Caminho onde será salvo o arquivo JSON com os resultados
- **resultados_excel**: Caminho onde será salvo o arquivo Excel com os resultados
- **caminho_planilha**: Caminho da planilha Excel de entrada
- **nome_aba**: Nome da aba da planilha que contém os dados para execução
- **coluna_estabeleciomento**: Nome da coluna que contém os nomes dos estabelecimentos
- **coluna_qtd**: Nome da coluna que contém a quantidade de resultados a coletar

## 📊 Formato da Planilha de Entrada

A planilha Excel de entrada deve conter as seguintes colunas:

| Estabelecimento | Quantidade |
| --------------- | ---------- |
| Restaurantes    | 5          |
| Farmácias      | 10         |
| Supermercados   | 3          |

**Observação**: Os nomes das colunas devem corresponder aos valores configurados em `config.toml`.

## 🚀 Como Usar

1. **Prepare sua planilha de entrada:**

   - Crie um arquivo Excel em `data/data.xlsx`
   - Preencha com os estabelecimentos que deseja buscar
   - Configure as colunas conforme especificado acima
2. **Execute o programa:**

```bash
python main.py
```

3. **Acompanhe o progresso:**

   - O programa exibirá logs no console
   - Arquivos de log são salvos na pasta `logs/`
   - Os resultados são salvos automaticamente durante a execução
4. **Resultados:**

   - Arquivo JSON: `data/results/resultados.json`
   - Arquivo Excel: `data/results/resultados.xlsx`

## 📁 Estrutura do Projeto

```
Consultar_estabelecimentos/
│
├── main.py                      # Arquivo principal de execução
├── config.toml                  # Arquivo de configuração
├── chromedriver.exe             # Driver do Chrome para Selenium
│
├── functions/
│   ├── src/
│   │   └── google_map.py        # Módulo de coleta de dados do Google Maps
│   │
│   └── utils/
│       ├── selenium_web.py      # Classe de automação web com Selenium
│       ├── file_manager.py      # Funções para leitura/escrita de arquivos
│       └── logger.py            # Sistema de logging
│
├── data/
│   ├── data.xlsx                # Planilha de entrada (você precisa criar)
│   └── results/
│       ├── resultados.json      # Resultados em JSON (gerado)
│       └── resultados.xlsx      # Resultados em Excel (gerado)
│
└── logs/
    └── log_YYYYMMDD.log         # Arquivos de log (gerados)
```

## 🔍 Funcionalidades Técnicas

### Sistema de Retry

O programa possui um sistema automático de retry que reinicia o navegador em caso de falha durante a coleta de dados, garantindo maior robustez na execução.

### Logging

Todos os eventos são registrados em arquivos de log diários na pasta `logs/`, facilitando o debug e monitoramento da execução.

### Tratamento de Erros

O código possui tratamento de erros robusto que permite continuar a execução mesmo em caso de falhas pontuais, registrando todas as ocorrências nos logs.

## ⚠️ Observações Importantes

- Certifique-se de que o ChromeDriver está compatível com a versão do Google Chrome instalada
- O programa abre uma janela do navegador Chrome durante a execução
- É recomendado não interagir com o navegador enquanto o programa está em execução
- A velocidade de coleta depende da conexão com a internet e do tempo de resposta do Google Maps
- Respeite os termos de uso do Google Maps ao utilizar este script
