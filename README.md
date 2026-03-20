# 🛠️ MarraStack | Hub de Automações & MyFinance

O **MarraStack** é um ecossistema de ferramentas desenvolvido para centralizar automações de produtividade, gestão financeira e geração de documentos. O projeto foi construído com foco em arquitetura limpa, utilizando o padrão **MVC (Model-View-Controller)**.

---

## 🚀 Tecnologias Utilizadas

* **Backend:** Python 3.x com Flask
* **Banco de Dados:** SQLite3
* **Frontend:** HTML5, CSS3 (Modular/Geométrico) e Jinja2
* **Ferramentas de Automação:** Selenium, Pandas, Python-docx (Integração em progresso)
* **Ambiente:** Anaconda / VS Code

---

## 🏗️ Estrutura do Projeto (MVC)

O projeto segue uma estrutura organizada para facilitar a escalabilidade:

/marrastack
│
├── app.py                # Controller Principal e Configurações
├── models.py             # Camada de Dados (Lógica de Banco de Dados)
├── static/               # Arquivos Estáticos (CSS, JS, Imagens)
│   ├── css/              # Estilização "Dark Tech"
│   └── img/              # Favicon e Logotipos
├── templates/            # Views (Templates Jinja2)
│   ├── layouts/          # Estruturas base e Navbar
│   └── admin/            # Painéis restritos
└── requirements.txt      # Dependências do projeto


🛠️ Ferramentas Integradas
Lead Capture: Landing Page otimizada para captura de e-mails com feedback de sucesso/duplicidade.

Admin Panel: Painel restrito com autenticação por sessão para visualização de leads.

My Finance (Em breve): Módulo de gestão financeira pessoal.

Docs Gen (Em breve): Gerador automático de documentos .docx para licitações.

🔧 Como Executar o Projeto
1. Clone o repositório:
git clone [https://github.com/SEU_USUARIO/marrastack.git](https://github.com/SEU_USUARIO/marrastack.git)

2. Crie um ambiente virtual (opcional):
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3. Instale as dependências:
pip install -r requirements.txt

4. Inicie o servidor:
python app.py

Acesse: http://127.0.0.1:5000

🛡️ Segurança
O acesso ao painel administrativo é protegido via sessão. Para fins de desenvolvimento, utilize a chave mestra definida no controlador.

Desenvolvido por Bruno Cassio Marra

