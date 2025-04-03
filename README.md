# 🌻 Sunflower Tracker – Dashboard de Preços do Sunflower Land

Esse projeto coleta dados de preços dos itens do jogo **Sunflower Land**, armazena em um banco de dados MySQL (na nuvem) e exibe os dados em um painel com gráficos interativos.

---

## 🚀 O que esse projeto faz

- 🔁 Atualiza automaticamente os preços dos itens a cada 15 minutos
- 🔧 Armazena os dados em um banco MySQL (Clever Cloud)
- 🌐 Expõe uma API em Flask para acessar os dados
- 📊 Exibe os dados em tempo real em um painel com gráficos dinâmicos
- 💻 Frontend hospedado via GitHub Pages

---

## 📦 Tecnologias usadas

| Camada         | Tecnologia                  |
|----------------|-----------------------------|
| API            | Python + Flask + Flask-CORS |
| Script         | Python + Requests + MySQL   |
| Banco de Dados | Clever Cloud (MySQL)        |
| Automação      | Replit                      |
| Frontend       | HTML + JS + Chart.js        |
| Hospedagem     | Render (API) + GitHub Pages (painel) |

---

## 📂 Estrutura do projeto
sunflower/
├── app.py                     # API Flask com rotas /api/items e /api/price_history
├── sunflower_price_tracker.py # Script de atualização automática dos preços
├── requirements.txt           # Lista de dependências
├── templates/
│   └── index.html             # Frontend (painel)
├── images/                    # Ícones do frontend
├── .env.example               # Exemplo do arquivo de variáveis (sem dados reais)
└── .gitignore                 # Ignora o .env real


## 🔐 Variáveis de ambiente

As variáveis estão no arquivo `.env` (NÃO deve ser versionado). Exemplo:

```env
DB_HOST=seuhost.clever-cloud.com
DB_PORT=3306
DB_USER=usuario
DB_PASSWORD=senha
DB_NAME=nome_do_banco

📡 Endpoints da API
GET /api/items
Retorna a lista de nomes dos itens únicos.

GET /api/price_history?item=Banana&days=7
Retorna o histórico de preço do item informado nos últimos 7 dias.

🧪 Como rodar localmente
Clone o projeto:

bash
Copiar
Editar
git clone https://github.com/SEU_USUARIO/sunflower.git
cd sunflower
Instale as dependências:

bash
Copiar
Editar
pip install -r requirements.txt
Crie um arquivo .env com as credenciais do banco (como mostrado acima).

Para iniciar a API:

bash
Copiar
Editar
python app.py
Para rodar o script que coleta e atualiza os dados:

bash
Copiar
Editar
python sunflower_price_tracker.py
🌍 Deploys utilizados
Plataforma	Função
🟢 Render	Hospeda a API Flask
🔁 Replit	Executa o script automático
☁️ Clever	Banco de dados MySQL
🖼️ GitHub Pages	Exibe o painel com os gráficos
🧠 Feito por
Elivelton Castilho
🔧 Python | Flask | MySQL | Frontend

⭐ Licença
MIT – Livre para uso, cópia e modificação.

yaml
Copiar
Editar

---

Se quiser, posso gerar ele automaticamente como um arquivo `.md` e até te mandar um pull request se
