# 🚀 GUIA DE APRESENTAÇÃO - CHECKMATE

Olá Samuel e dupla! Este arquivo é o "Painel de Controle" de vocês para a apresentação. 
Siga este passo a passo para não ter erro na hora de mostrar o projeto para o professor.

---

## PASSO 1: Preparando o Terreno (Rodando o Projeto)
Antes de começar a falar, certifique-se de que o Docker Desktop está aberto no seu Windows.
Depois, abra o Terminal aqui no VS Code (`Ctrl + '`) e rode o comando mágico:

```bash
docker-compose up -d
```
*(Isso vai ligar o Banco de Dados, o Servidor Python e o Adminer de uma vez só!)*

---

## PASSO 2: A Interface (Frontend)
Mostre ao professor o aplicativo funcionando na prática.

🔗 **[Clique aqui para abrir o código do HTML no VS Code](./frontend/index.html)**
🔗 **[Clique aqui para abrir a lógica Javascript no VS Code](./frontend/app.js)**

👉 **Como abrir no navegador:**
No arquivo `index.html` aberto, clique com o botão direito e selecione "Reveal in File Explorer" (ou "Abrir no Explorador de Arquivos"), depois dê dois cliques para ele abrir no Google Chrome.

---

## PASSO 3: O Cérebro (Backend)
Quando o professor quiser ver o código e a arquitetura profissional que vocês montaram, clique nos links abaixo. Eles vão abrir direto no seu VS Code! Não se esqueça de ler os **comentários em português** que deixei neles.

🔗 **1. [O Motor do Servidor (`main.py`)](./app/main.py)** - Mostre como a porta de entrada é limpa e sem bagunça.
🔗 **2. [As Rotas de Login (`auth.py`)](./app/api/auth.py)** - Mostre o "Balcão de Atendimento" recebendo a requisição.
🔗 **3. [Os Validadores (`user.py`)](./app/schemas/user.py)** - Mostre o Pydantic agindo como o "Avaliador de Qualidade".

---

## PASSO 4: A Documentação Viva (Swagger UI)
Esta é a parte para impressionar. O FastAPI gera a documentação automaticamente.

🌐 **[Clique aqui para abrir o Swagger no Navegador](http://localhost:8000/docs)**

> **Dica:** Mostre a rota `/auth/register` e fale sobre o cadeado verde (Autenticação JWT).

---

## PASSO 5: O Banco de Dados (PostgreSQL)
Para provar que os dados estão sendo salvos e as senhas criptografadas, usem o Adminer.

🌐 **[Clique aqui para abrir o Banco de Dados no Navegador](http://localhost:8080)**

**Suas credenciais para logar na frente dele:**
- **Sistema:** PostgreSQL
- **Servidor:** `db`
- **Usuário:** `checkmate_user`
- **Senha:** `checkmate_pass`
- **Base de dados:** `checkmate_db`

> **Dica:** Clique em "select" na tabela `users` para mostrar as senhas bagunçadas (criptografadas pelo Bcrypt).

---
Boa sorte, vocês vão arrasar! 🥇
