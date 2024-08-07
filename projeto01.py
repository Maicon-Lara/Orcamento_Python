import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from fpdf import FPDF

# Configuração do e-mail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FROM_EMAIL = "mail@gmail.com"
PASSWORD = "XXXXXX"

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

def gerar_orcamento(nome, endereco, telefone, email, descricao, projeto,
                    horas_estimadas, valor_hora, prazo):
    valor_total = int(horas_estimadas) * int(valor_hora)
    orcamento = f"""
    Nome: {nome}
    Endereço: {endereco}
    Telefone: {telefone}
    E-mail: {email}
    Descrição: {descricao}
    Nome do projeto: {projeto}
    Horas estimadas: {horas_estimadas}
    Valor da hora trabalhada: {valor_hora}
    Prazo: {prazo}
    Valor total: {valor_total}
    """
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial")

    pdf.image("template.png", x=0, y=0)

    pdf.text(115, 145, projeto)
    pdf.text(115, 160, horas_estimadas)
    pdf.text(115, 175, valor_hora)
    pdf.text(115, 190, prazo)
    pdf.text(115, 205, str(valor_total))

    pdf.output("Orçamento.pdf")
    return orcamento, valor_total

def main():
    st.title("Gerar Orçamento")
    st.write("Preencha os campos abaixo para gerar um orçamento")

    nome = st.text_input("Nome")
    endereco = st.text_input("Endereço")
    telefone = st.text_input("Telefone")
    email = st.text_input("E-mail")
    descricao = st.text_area("Descrição")
    projeto = st.text_input("Nome do projeto")
    horas_estimadas = st.text_input("Horas estimadas")
    valor_hora = st.text_input("Valor da hora trabalhada:")
    prazo = st.text_input("Prazo")

    if st.button("Gerar Orçamento"):
        orcamento, valor_total = gerar_orcamento(nome, endereco, telefone, email, descricao, projeto,
                    horas_estimadas, valor_hora, prazo)
        st.write("Orçamento gerado:")
        st.write(orcamento)

        if st.button("Enviar Orçamento por E-mail"):
            to_email = email
            subject = "Orçamento"
            body = "Segue em anexo o orçamento gerado"
            file = open("Orçamento.pdf", "rb")
            send_email(to_email, subject, body, file)
            st.success("Orçamento enviado com sucesso!")

if __name__ == "__main__":
    main()