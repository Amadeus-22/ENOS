import os
import json
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage
from dotenv import load_dotenv

# Configurações de diretório e segurança
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(diretorio_atual, '.env'))

def enviar_aviso(contas):
    EMAIL_REMETENTE = os.getenv('EMAIL_USER')
    SENHA_APP = os.getenv('EMAIL_PASS')
    DESTINATARIOS = ["barbosamaverickv8@gmail.com", "pamelabarbosa.m@gmail.com"]

    msg = EmailMessage()
    msg['Subject'] = "⚠️ ENOS: Lembrete de Pagamento para AMANHÃ"
    msg['From'] = f"Enos <{EMAIL_REMETENTE}>"
    msg['To'] = ", ".join(DESTINATARIOS)

    corpo = "Olá,\n\nIdentifiquei contas que vencem AMANHÃ. Segue a lista:\n\n"
    for item in contas:
        corpo += f"📌 {item['Nome']} - Vencimento dia {item['Dia']}\n"
    corpo += "\nAtenciosamente,\nEnos - Seu Assistente."

    msg.set_content(corpo)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_REMETENTE, SENHA_APP.replace(" ", "").strip())
        smtp.send_message(msg)

def verificar_calendario():
    with open(os.path.join(diretorio_atual, 'pagamentos.json'), 'r', encoding='utf-8') as f:
        dados = json.load(f)

    hoje = datetime.now()
    amanha = hoje + timedelta(days=1)
    dia_amanha = amanha.day
    
    # Lógica para o último dia do mês (Receita Federal)
    proximo_dia_depois_de_amanha = amanha + timedelta(days=1)
    e_ultimo_dia = proximo_dia_depois_de_amanha.month != amanha.month

    contas_notificar = []
    for conta in dados['Pagamento']:
        if conta['Dia'] == dia_amanha:
            contas_notificar.append(conta)
        elif conta['Dia'] == "ULTIMO" and e_ultimo_dia:
            contas_notificar.append(conta)

    if contas_notificar:
        enviar_aviso(contas_notificar)
        print(f"✅ Notificação enviada para {len(contas_notificar)} contas.")
    else:
        print("😴 Nenhuma conta vence amanhã. Enos voltando a dormir...")

if __name__ == "__main__":
    verificar_calendario()