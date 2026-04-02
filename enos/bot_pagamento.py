import os
import json
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage
from dotenv import load_dotenv

# Configurações de diretório e segurança
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
# Garante que ele ache o .env mesmo rodando no servidor ou local
load_dotenv(os.path.join(diretorio_atual, '.env'))

def enviar_relatorio_geral(contas):
    EMAIL_REMETENTE = os.getenv('EMAIL_USER')
    SENHA_APP = os.getenv('EMAIL_PASS')
    # Adicionei a Pamela conforme sua preferência anterior
    DESTINATARIOS = ["barbosamaverickv8@gmail.com", "pamelabarbosa.m@gmail.com"]

    if not EMAIL_REMETENTE or not SENHA_APP:
        print("❌ Erro: Credenciais não encontradas no .env")
        return

    msg = EmailMessage()
    msg['Subject'] = "📊 ENOS: Relatório Geral de Contas do Mês"
    msg['From'] = f"Enos <{EMAIL_REMETENTE}>"
    msg['To'] = ", ".join(DESTINATARIOS)

    # Montando o corpo do e-mail com todas as contas do JSON
    corpo = "Olá Pedro,\n\nConforme solicitado, aqui está a lista completa de todas as suas contas registradas:\n\n"
    corpo += "--------------------------------------\n"
    
    for item in contas:
        # Verifica se é o caso especial da Receita Federal
        dia = "Último dia do mês" if item['Dia'] == "ULTIMO" else f"Dia {item['Dia']}"
        corpo += f"✅ {item['Nome'].ljust(20)} | Vencimento: {dia}\n"
    
    corpo += "--------------------------------------\n"
    corpo += f"\nRelatório gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    corpo += "\n\nAtenciosamente,\nEnos - Seu Assistente de Automação."

    msg.set_content(corpo)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            # Remove espaços da senha de app do Gmail para evitar erro de login
            smtp.login(EMAIL_REMETENTE, SENHA_APP.replace(" ", "").strip())
            smtp.send_message(msg)
            print("🚀 Contas enviadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")

def rodar_enos():
    caminho_json = os.path.join(diretorio_atual, 'pagamentos.json')
    
    try:
        with open(caminho_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        todas_as_contas = dados.get('Pagamento', [])

        if todas_as_contas:
            enviar_relatorio_geral(todas_as_contas)
        else:
            print("🤔 O arquivo JSON está vazio ou sem contas.")
            
    except FileNotFoundError:
        print(f"❌ Erro: O arquivo {caminho_json} não foi encontrado!")
    except json.JSONDecodeError:
        print("❌ Erro: O arquivo pagamentos.json está com formato inválido!")

if __name__ == "__main__":
    rodar_enos()