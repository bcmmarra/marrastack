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

```text
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
