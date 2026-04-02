import os
import json
import smtplib
from datetime import datetime
from email.message import EmailMessage
from dotenv import load_dotenv

# Configurações de diretório e segurança
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
# Carrega as variáveis do arquivo .env (EMAIL_USER e EMAIL_PASS)
load_dotenv(os.path.join(diretorio_atual, '.env'))

def enviar_relatorio_geral(contas):
    EMAIL_REMETENTE = os.getenv('EMAIL_USER')
    SENHA_APP = os.getenv('EMAIL_PASS')
    DESTINATARIOS = ["barbosamaverickv8@gmail.com", "pamelabarbosa.m@gmail.com"]

    if not EMAIL_REMETENTE or not SENHA_APP:
        print("❌ Erro: Credenciais não encontradas no arquivo .env")
        return

    msg = EmailMessage()
    msg['Subject'] = "📊 ENOS: Relatório Geral de Contas do Mês"
    msg['From'] = f"Enos <{EMAIL_REMETENTE}>"
    msg['To'] = ", ".join(DESTINATARIOS)

    # Montando o corpo do e-mail de forma organizada
    corpo = "Olá Pedro,\n\nConforme solicitado, aqui está a lista completa de todas as suas contas registradas para este mês:\n\n"
    corpo += "--------------------------------------------------\n"
    corpo += f"{'CONTA'.ljust(25)} | {'VENCIMENTO'}\n"
    corpo += "--------------------------------------------------\n"
    
    for item in contas:
        # Lógica para exibir o dia correto ou "Último dia"
        dia_texto = "Último dia do mês" if item['Dia'] == "ULTIMO" else f"Dia {item['Dia']}"
        corpo += f"✅ {item['Nome'].ljust(23)} | {dia_texto}\n"
    
    corpo += "--------------------------------------------------\n"
    corpo += f"\nRelatório gerado automaticamente em: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    corpo += "\n\nAtenciosamente,\nEnos - Seu Assistente de Automação."

    msg.set_content(corpo)

    try:
        # O Gmail exige que a senha de app não tenha espaços
        senha_limpa = SENHA_APP.replace(" ", "").strip()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_REMETENTE, senha_limpa)
            smtp.send_message(msg)
            print("🚀 Relatório mensal enviado com sucesso para os destinatários!")
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")

def rodar_enos():
    caminho_json = os.path.join(diretorio_atual, 'pagamentos.json')
    
    # --- TRAVA DE SEGURANÇA MENSAL ---
    hoje = datetime.now()
    DIA_DO_RELATORIO = 1  # <--- Altere aqui para testar (ex: colocar 2 para hoje)
    
    if hoje.day != DIA_DO_RELATORIO:
        print(f"😴 Hoje é dia {hoje.day}. O relatório está programado apenas para o dia {DIA_DO_RELATORIO}.")
        print("Enos voltando a dormir...")
        return
    # ----------------------------------

    try:
        # Verifica se o arquivo JSON existe antes de tentar abrir
        if not os.path.exists(caminho_json):
            print(f"❌ Erro: O arquivo {caminho_json} não foi encontrado!")
            return

        with open(caminho_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        todas_as_contas = dados.get('Pagamento', [])

        if todas_as_contas:
            enviar_relatorio_geral(todas_as_contas)
        else:
            print("🤔 O arquivo JSON está vazio ou não contém a chave 'Pagamento'.")
            
    except json.JSONDecodeError:
        print("❌ Erro: O arquivo pagamentos.json está com formato inválido (JSON corrompido)!")
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    rodar_enos()