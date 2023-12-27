# Automação para Extração de Notas Fiscais de Serviço Eletrônica (NFSE) - Município de Campinas

## Funcionalidades

Esta automação simplifica a extração de Notas Fiscais de Serviço Eletrônica (NFSE) do município de Campinas. O processo é dividido nas seguintes etapas:

1. Insirir um CNPJ.
2. Especificar um intervalo de datas.
3. Acessar as notas referentes ao período.
4. Extrair os dados da nota e do prestador de serviço.
5. Salvar as informações extraídas.

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

  - Pasta para armazenamento dos dados extraídos

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

### Extrair os dados

- São extraídos os dados da nota e do prestador, salvos como **extracts/nota\_{numero_da_nota}.json**
- Os dados extraídos são:
  labels_nota = ['Número da Nota', 'Data e Hora de Emissão', 'Código de Verificação']
  labels_prestador = ['Nome/Razão Social', 'CPF/CNPJ', 'Inscrição Municipal', 'Endereço', 'Município', 'UF', 'Telefone']
- Podendo ser alterados diretamente do arquivo **navigation/\_5_extract_nota_data.py**
