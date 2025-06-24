## Vaguinhas

Esse projeto tem como intuíto facilitar a busca de vagas de emprego.
Ele consiste de um crawler do linkedin jobs (que será extendido para outros divulgadores de vagas),
que notifica através de um bot do telegram novas vagas específicadas pelo filtro criado pelo usuário.

> Essa solução tem o risco de bloquear a sua conta do Linkedin, então é recomendado que não 
> use a sua conta principal.

#### Instruções de uso:

##### Passo 1:
Como vamos usar o telegram para nos notificar, então precisamos primeiramente criar um bot.
Para fazer isso é só pesquisar Botfather na busca do telegram e as demais instruções serão dadas
por ele.

Depois de concluir esta etapa, você terá o token necessário para o envio de mensagens ao telegram.
Adicione esse token ao `.env`, como no exemplo demonstrado no `exemple.env`. Agora será necessário o `id`
do chat, para isso mande uma mensagem para o bot, e em seguida use o seguinte comando:
```sh
curl https://api.telegram.org/bot<TOKEN>/getUpdates
```
(substitua o \<TOKEN\> pelo token usado no `.env`) com isso será exibido os chats abertos, pegue o id
do chat com você. Adicione esse `id` ao `.env`.

##### Passo 2:
Criação do envioronment e instalação das dependências:

```sh
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

##### Passo 3:
substitua o filtro na `main.py` para a vaga que pretende ser notificado, na função `linkedin.search_jobs()` e em seguida
rode o programa com `python3 main.py`.

Nesse primeiro momento, será aberto a linkedin para ser feito o login. Essa abordagem evita o bot de cair em algum captcha.
Faça login em uma conta secundária, o que ele vai fazer é salvar o cookie de sessão, e nas próximas interações esse cookie será
usado e não precisará de login novamente, somente quando o cookie expirar.

Se tudo der certo, as vagas aparecerão no chatbot.

##### AVISOS:

Essa primeira implementação está muito manual ainda (foi somente uma prova de conceito), mas melhorias estão sendo feitas.
Na estratégia atual, foi pensado o uso do crontab para a execução periódica dessa solução, mas está longe de ser a ideal.
- Será implementado um banco de dados, para que as vagas que já foram notificadas não se repitam.
- A busca e notificação de vagas será implementada de forma assíncrona
```
