# Vaguinhas

Este projeto é uma ferramenta para automatizar a busca por vagas de emprego no LinkedIn, notificando o usuário sobre novas oportunidades através de um bot no Telegram (ainda planejo adicionar outras formas de notificações).

> [!WARNING]
> **Risco de Bloqueio:** O uso de automação para interagir com o LinkedIn pode violar os termos de serviço da plataforma e resultar no bloqueio da sua conta. **É altamente recomendável que você utilize uma conta secundária, não a sua principal.**

## Funcionalidades

- **Crawler de Vagas:** Realiza buscas automáticas no LinkedIn Jobs com base em filtros definidos pelo usuário.
- **Notificações via Telegram:** Envia as vagas encontradas para um chat do Telegram em tempo real.
- **Persistência:** Armazena as vagas já notificadas para evitar duplicatas.

## Pré-requisitos

- Python 3.10+
- Uma conta no Telegram
- Uma conta no LinkedIn

## Instalação

1.  **Clone o repositório:**
    ```sh
    git clone https://github.com/seu-usuario/job_search.git
    cd vaguinha
    ```

2.  **Crie e ative um ambiente virtual:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Instale os drivers do Playwright:**
    ```sh
    playwright install
    ```

## Configuração

### 1. Bot do Telegram

Você precisará de um token de bot e um ID de chat para que as notificações funcionem.

1.  **Crie um Bot:**
    - No Telegram, procure por `BotFather`.
    - Envie o comando `/newbot` e siga as instruções para criar seu bot.
    - O `BotFather` fornecerá um **token**.

2.  **Obtenha o Chat ID:**
    - Envie qualquer mensagem para o seu novo bot no Telegram.
    - Execute o seguinte comando no seu terminal, substituindo `<TOKEN>` pelo token que você recebeu:
      ```sh
      curl https://api.telegram.org/bot<TOKEN>/getUpdates
      ```
    - Na resposta JSON, localize o objeto `chat` e copie o valor do campo `id`.

### 2. Variáveis de Ambiente

1.  **Crie o arquivo `.env`:**
    - Renomeie ou copie o arquivo `exemple.env` para `.env`.

2.  **Adicione as credenciais:**
    - Abra o arquivo `.env` e adicione o token do bot e o ID do chat que você obteve:
      ```env
      TELEGRAM_TOKEN="SEU_TOKEN_AQUI"
      TELEGRAM_CHAT_ID="SEU_CHAT_ID_AQUI"
      ```

## Como Usar

1.  **Configure o Filtro de Busca:**
    - Abra o arquivo `main.py`.
    - Na função `main`, localize as Variáveis `job_titles`, `locations` e `seniority_levels`.
    - Altere os parâmetros (como `job_titles` e `locations`) para definir o tipo de vaga que você deseja buscar.

2.  **Execute o Script:**
    ```sh
    python3 main.py
    ```

### Primeiro Acesso

Na primeira vez que o script for executado, uma janela do navegador será aberta para que você faça o login no LinkedIn. Esta etapa é necessária para salvar os cookies de sessão, permitindo que o bot se autentique em execuções futuras sem a necessidade de login manual.

Após o login, o script começará a buscar as vagas e, se encontrar alguma que corresponda ao seu filtro, enviará uma notificação para o seu bot no Telegram.

Caso o cookie expire, você pode executar o `scripts/create_cookies.py` para que o cookie seja renovado.

## Roadmap de Melhorias

Esta é uma prova de conceito e melhorias contínuas estão sendo planejadas:

- [ ] Implementar a busca e notificação de forma assíncrona para melhor performance.
- [x] Transformar o script em um serviço de loop contínuo, com intervalos de busca configuráveis.
- [ ] Adicionar suporte a outras plataformas de vagas além do LinkedIn.
- [ ] Criar uma interface mais amigável para gerenciar os filtros de busca.
