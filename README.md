# ENOS
# 🤖 Projeto Enos: Assistente de Pagamentos Inteligente

O **Enos** é um bot de automação desenvolvido em Python para gerenciar lembretes de pagamentos. Ele monitora um arquivo de dados local e envia notificações por e-mail para os destinatários configurados exatamente **um dia antes** do vencimento de cada conta.

## 🚀 Funcionalidades
- **Monitoramento Automático:** Verifica diariamente quais contas vencem no dia seguinte.
- **Lógica de Calendário:** Identifica vencimentos por dia do mês e trata casos especiais como "último dia do mês" (ex: Receita Federal).
- **Segurança:** Utiliza variáveis de ambiente (`.env`) para proteger credenciais SMTP.
- **Deploy em Nuvem:** Configurado para rodar 24/7 via tarefas agendadas (Cron/Tasks) no PythonAnywhere.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.x
- **Bibliotecas:** `smtplib`, `email.message`, `json`, `datetime`, `python-dotenv`
- **Infraestrutura:** Linux Mint (Local) / PythonAnywhere (Nuvem)
- **Agendamento:** Crontab / PythonAnywhere Tasks

## 📂 Estrutura do Projeto
```text
Enos/
├── enos/
│   ├── bot_pagamento.py   # O "cérebro" do assistente
│   ├── pagamentos.json    # Banco de dados das contas
│   └── .env               # Credenciais (Oculto via .gitignore)
├── .gitignore             # Proteção de arquivos sensíveis
├── requirements.txt       # Dependências do projeto
└── README.md              # Documentação