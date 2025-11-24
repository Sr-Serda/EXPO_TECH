
# **README.md**

# 🧾 NovaDesk — Sistema de Chamados (Help Desk)

O **NovaDesk** é um sistema de abertura, gerenciamento e controle de tickets, desenvolvido em **Flask**, com interface utilizando **Bootstrap 5**, gradientes, sidebar e pesquisa em tempo real.
para equipes que precisam registrar solicitações, acompanhar status e administrar chamados de forma simples.
---

## 📌 **Funcionalidades**

### 🔐 Autenticação

* Tela de login.
* Sessões protegidas com Flask-Login.
* Diferenciação entre usuários **comuns** e **administradores**.

### 🎫 Gestão de Tickets

* Criar tickets com título e descrição.
* Administradores podem:

  * Alterar status (Pending, In Progress, Completed)
  * Excluir tickets
* Modal de visualização detalhada.

### 🎨 Interface

* **Sidebar com gradiente azul/roxo**
* **Topbar com barra de pesquisa**
* **Badges coloridas e com gradientes**
* **Cards arredondados e sombreados**

### 🔍 Pesquisa (JavaScript)

* Filtragem instantânea dos tickets, sem recarregar a página.



## 🛠️ **Tecnologias Utilizadas**

* **Python 3.10+**
* **Flask**
* **Flask-Login**
* **SQLAlchemy**
* **Bootstrap 5.3**
* **Bootstrap Icons**
* **JavaScript Vanilla**
* **SQLite** (padrão, mas pode usar PostgreSQL ou MySQL)

---

## 📁 Estrutura do Projeto

```
project/
│
├── app.py
├── requirements.txt
├── instance/
│   └── database.db
│
├── templates/
│   ├── login.html
│   └── dashboard.html
│
└── static/
    ├── css/
    │   └── custom.css
    ├── js/
    │   └── main.js
    └── img/
```

---

## 🚀 Instalação e Execução

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

### 2️⃣ Crie um ambiente virtual

```bash
python -m venv venv
```

### 3️⃣ Ative o ambiente

#### Windows:

```bash
venv\Scripts\activate
```

#### Linux / Mac:

```bash
source venv/bin/activate
```

### 4️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 5️⃣ Execute a aplicação

```bash
python app.py
```

O sistema iniciará em:

```
http://127.0.0.1:5000
```

---

## 🔑 Usuário Admin padrão

Ao rodar a primeira vez, geralmente o sistema cria um administrador:

```
Usuário: admin
Senha: admin

## 📝 Principais Rotas

| Rota                 | Método   | Função              |
| -------------------- | -------- | ------------------- |
| `/login`             | GET/POST | Tela de login       |
| `/dashboard`         | GET      | Painel de tickets   |
| `/create_order`      | POST     | Criação de ticket   |
| `/update_order/<id>` | POST     | Alteração de status |
| `/delete_order/<id>` | GET      | Excluir ticket      |
| `/logout`            | GET      | Encerrar sessão     |

