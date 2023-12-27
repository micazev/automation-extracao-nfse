# Automação para Extração de Notas Fiscais de Serviço Eletrônica (NFSE) - Município de Campinas

## Funcionalidades

Esta automação simplifica a extração de Notas Fiscais de Serviço Eletrônica (NFSE) do município de Campinas. O processo é dividido nas seguintes etapas:

1. Insira um CNPJ.
2. Especifique um intervalo de datas.
3. Acesse as notas referentes ao período.
4. Extraia os dados da nota e do prestador de serviço.
5. Salve as informações extraídas.

## Estrutura de Pastas e Arquivos

- **\_init_py**
- **gitignore**
- **main.py**
- **README.md**
- **requirements.txt**
- **setup.py**
- **utils.py**

- **config**

  - **init**
  - **input.json**
  - **recover.json**

- **extracts**

  - Onde a automação armazena as notas salvas com o nome **nota\_{numero_da_nota}**

- **logs**

  - Pasta para armazenamento de logs

- **navigation**

  - **\_init_py**
  - **1_insert_credentials.py**
  - **2_select_date_range.py**
  - **3_verifica_notas.py**
  - **4_click_each_nfse.py**
  - **5_extract_nota_data.py**

- **scripts**
  - **navegar_notas_periodo.py**
  - **navegar_pagina.py**
  - **verifica_paginacao.py**

## Input

```json
{
  "dataInicio": "2022-01",
  "dataFim": "2022-12",
  "usuario": "xx.xxx.xxx/xxxx-xx",
  "senha": "xx",
  "captchaKey": "xx"
}
```

## Especificações

### Login

- Utiliza a resolução via anti-captcha.com.
- Salva a imagem na pasta "config" antes de solucionar.

### Filtrar e Inserir Datas

- O site aceita apenas extrações de 6 em 6 meses.
- Recomenda-se a extração de 3 em 3 meses para evitar muitas paginações.
- É possível alterar o intervalo de busca com a variável **intervalo_meses** em **processar_datas** dentro de **config/config.json**.
