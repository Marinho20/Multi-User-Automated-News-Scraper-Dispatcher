import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from database import connect_database,get_all_users,get_seen_titles,get_keywords
from scanner import runscaner,fetch_headlines,insert_seen_news
import os
from dotenv import load_dotenv

connection = connect_database()

load_dotenv()


def send_email(user_id,news_list):
    #depois tem de ir para o .env
    sender_gmail = os.getenv("BOT_sender_gmail")
    sender_password = os.getenv("BOT_sender_password")
    #gets the user name and email
    cursor = connection.cursor(dictionary = True)
    cursor.execute ("Select email,username from users where id = %s", (user_id,))
    user_data = cursor.fetchone()

    if not user_data:
        print(f"user with id {user_id} not found")
        return
    
    receiver_email = user_data['email']
    user_name = user_data['username']

    #configure bot

    msg = MIMEMultipart()
    msg['From'] = sender_gmail
    msg['To'] = receiver_email
    msg['subject'] = f"user {user_name} has {len(news_list)} new news"


    text_body = "Here are fresh news\n"
    for title,url in news_list:
        text_body += f"-TITLE: {title}\n"
        text_body += f"LINK: {url}\n"
        text_body += "-" * 40 + "\n"
    
    text_body += "\nBot v1.0 - Engenharia"

    msg.attach(MIMEText(text_body,"plain"))

    # send the email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls() # encrypt for security

                #login
                server.login(sender_gmail,sender_password)

                #send 
                server.send_message(msg)
    
    except Exception as e:
         print(f"error sending email {e}")

def run_global_bot():
    # 1. Busca as notícias na BBC uma única vez (eficiência!)
    all_headlines = fetch_headlines() 
    if not all_headlines:
        print("BBC fora do ar ou sem notícias.")
        return

    # 2. Busca todos os clientes/utilizadores
    users = get_all_users() 

    for user in users:
        u_id = user['id']
        u_email = user['email']
        print(f"--- Processando: {user['username']} ---")

        # 3. Busca o que ESTE user já viu e o que ele quer
        seen_titles = get_seen_titles(u_id)
        user_keywords = get_keywords(u_id)

        interesting_for_this_user = []

        # 4. Filtra as notícias para este user específico
        for title, link in all_headlines:
            # Verifica se alguma keyword do user está no título
            # E verifica se ele ainda NÃO viu este título
            is_match = any(k[0].lower() in title.lower() for k in user_keywords)
            
            if is_match and title not in seen_titles:
                interesting_for_this_user.append((title, link))

        # 5. Se houver novidades exclusivas para ele, envia!
        if interesting_for_this_user:
            print(f"✅ found {len(interesting_for_this_user)} news {u_email}")
            send_email(u_id, interesting_for_this_user)
            
            # 6. Regista que ele já as viu para não repetir no próximo ciclo
            for title, link in interesting_for_this_user:
                insert_seen_news(u_id, title, link)
        else:
            print(f"😴 Sem novidades para {user['username']}.")
