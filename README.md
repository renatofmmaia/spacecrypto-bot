# Spacecrypto Bot [Family JOW]
Bot desenvolvido em python, 100% do código é aberto, para aqueles que tenham conhecimento validarem que não existe nenhum código malicioso, o bot apenas trabalha com reconhecimento de imagens para poder gerenciar as interações na tela, compatível com Windows e Linux.
O bot em constante atualização, e para que ele continue 100% free, não deixei de realizar sua contribuição, isso nos motiva a continuar!

# Doações
Faça seus testes, esta usando e ele te ajuda a otimizar seus ganhos? Mostre seu agradecimento em BUSD/BNB/BCOIN, assim nossa equipe se mantem empenhada em atualizar e trazer novas funcionalidades para a comunidade :relaxed:

Smart Chain Wallet(BUSD/BNB/SPG/SPE) 

***0xb3e7A42b647A0875682249294107Db182DDFC321***


# Funcionalidades
- Farm personalizado, defina a % que suas voltam a trabalhar.
- Multi Acc, logue a metamask de todas as suas contas, de play no bot e faça coisas melhores na sua vida do que ficar acordando de madrugada. :beers:
- Multi OS, funciona em linux ou Windows!
- Integração com Telegram, receba uma print cada X minutos, o tempo é configuravel no arquivo config.yaml.
- Anti-Broken, mesmo que aconteça um erro não tratado em tela, o bot força atualização da pagina e refaz o login, reiniciando o processo de farm, no pain yes gain!
- Arquivo de configuração, para que você mesmo determine como o bot deve funcionar (./config.yaml).

# Como utilizar
###  Requisitos:
- Instalação do Python, instale pelo [site oficial](https://www.python.org/downloads/) ou pela [windows store](https://www.microsoft.com/p/python-37/9nj46sx7x90p?activetab=pivot:overviewtab) durante a instalação do python, não se esqueça de marcar a opção add Python to Path.
- ![Path Python](https://github.com/renatofmmaia/spacecrypto-bot/blob/main/assets/infos_and_tutorial/python_path.png)
- Realizar download do bot, clicando em Code -> Download Zip
- ![download do bot](https://github.com/renatofmmaia/spacecrypto-bot/blob/main/assets/infos_and_tutorial/bot_download.png)
- Descompactar o bot na pasta em que desejar
- (Linux) Instalar o pacote xdtools (responsável por retornar as janelas de navegador no linux) através do comando: sudo apt-get install xdotool
- (Linux) Instalar pacote Scrot (responsável pela printscreen no linux) através do comando: sudo apt-get install scrot

###  Rodando o bot:
- Abra um terminal, se for windows (aperte a tecla do windows + r e digite "cmd").
- Navegue até a pasta onde o bot foi extraído, exemplo: cd "C:\spacecrypto-bot".
- Instale as dependências do bot executando o comando, sem aspas: Windows: "pip install -r requirements.txt" // Linux: "pip3 install -r requirements.txt".
- **IMPORTANTE:** Seu navegador não pode estar com ZOOM, pois o bot usa reconhecimento de imagem e o tamanho e proporção dos objetos fazem diferença e deve estar sempre MAXIMOZADO, ou seja, tela cheia.
- Faça o primeiro acesso na sua metamask, pois o bot realiza o login apenas se a mesma já estiver conectada.
- Execute o bot executando o cmando, sem aspas: "python main.py"
- Enjoy the moment :D

###  Configurando o Bot
- Todas as configurações do bot são realizadas através do arquivo config.yaml
- Configs importantes que você deve se atentar:
----------------------------------
- refresh_ships = Tempo em que o bot aguarda antes de realocar as navas para um novo farmar.
- **n_ships_to_fight** = Número de naves que você quer enviar sempre que for iniciar uma nova luta com o boss.
- **ship_work_percent** = Porcentagem em que o bot vai usar como referência na hora de enviar suas naves, atualmente apenas é permitido os valores (50, 75 ou 100)%.
- **repeat** = Total de scroll(rolagem) que o bot vai fazer, para encontrar as naves para farmar, a base de referência é a cada 10 naves, incrementar 3 no valor total, exemplo: 10 spaceships: 3 // 20 spaceships: 6 // 30 spaceships: 9 // ETC


###  Configurando Telegram
- Em seu telegram, inicie uma conversa com @BotFather
- Clique em Start, e quando abrir as opções, clique em "/newbot"
- Em seguida informe um nome e depois um username para o bot, lembrando que username tem que terminar com "_bot" no final, exemplo "meubomb_bot"
- Finalizando você vai ver uma mensagem contendo os dados do bot que vc criou, copie o Token e insira no arquivo de configuração, config.yaml
- O 2º parametro a ser configurado é o chat_id, para isso, siga os passos abaixo:
- Criei um grupo no telegram, e adicione o bot que você acabou de criar, informando o username para encontra-lo.
- Com o grupo criado, acesse o link a seguir, alterando o TOKEN na url, pelo o que você acabou de criar: https://api.telegram.org/botSEUTOKEN/getUpdates
- Vai ser exibido na tela um JSON, procure por "chat":"id", geralmente esse valor começa com o sinal de menos(-) e altere no arquivo config.yaml chat_id.
- Exemplo chat_id
- ![chatid](https://github.com/renatofmmaia/spacecrypto-bot/blob/main/assets/infos_and_tutorial/chat_id.png)
- Config.yaml que você tem que configurar
- ![config trelegram](https://github.com/renatofmmaia/spacecrypto-bot/blob/main/assets/infos_and_tutorial/token_chat_id.png)

### Possíveis soluções
- Mantenha a tela do navegador maximizada e a resolução do monitor preferencialmente em 1920x1080.
- (linux) Muitos problemas se rolvem ao atualizar o OS, pois os pacotes da instalação são basicos para o sistema rodar, para atualizar seu linux execute o comando: ***sudo apt updade && sudo apt upgrade -y***
- (linux) Se apresentar o erro "No module named 'tkinter'", execute o comando para instalar a interface grafica do python: ***sudo apt install python3-tk***
- (linux) Caso seu linux não reconheca o comando pip ou pip3, será necessário instala-lo, através do comando: ***sudo apt install python3-pip***

# Contato/Sugestão/Bug
- Issues github: https://github.com/renatofmmaia/spacecrypto-bot/issues/new

