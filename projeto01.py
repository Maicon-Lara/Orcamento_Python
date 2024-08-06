import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# Configuração do e-mail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FROM_EMAIL = "seu_email@gmail.com"
PASSWORD = "sua_senha"

def send_email(to_email, subject, body, file):
    msg = MIMEMultipart()
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    
    msg.attach(MIMEText(body, "plain"))
    
    if file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {file.name}")
        msg.attach(part)
    
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(FROM_EMAIL, PASSWORD)
    server.sendmail(FROM_EMAIL, to_email, msg.as_string())
    server.quit()

def gerar_orcamento(nome, endereco, telefone, email, descricao, valor):
    orcamento = f"""
    Nome: {nome}
    Endereço: {endereco}
    Telefone: {telefone}
    E-mail: {email}
    Descrição: {descricao}
    Valor: {valor}
    """
    return orcamento

def main():
    st.title("Gerar Orçamento")
    st.write("Preencha os campos abaixo para gerar um orçamento")

    nome = st.text_input("Nome")
    endereco = st.text_input("Endereço")
    telefone = st.text_input("Telefone")
    email = st.text_input("E-mail")
    descricao = st.text_area("Descrição")
    valor = st.text_input("Valor")

    if st.button("Gerar Orçamento"):
        orcamento = gerar_orcamento(nome, endereco, telefone, email, descricao, valor)
        st.write("Orçamento gerado:")
        st.write(orcamento)

        if st.button("Enviar Orçamento por E-mail"):
            to_email = email
            subject = "Orçamento"
            body = "Segue em anexo o orçamento gerado"
            file = None
            send_email(to_email, subject, body, file)
            st.success("Orçamento enviado com sucesso!")

if __name__ == "__main__":
    main()