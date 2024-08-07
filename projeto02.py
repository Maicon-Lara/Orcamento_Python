import streamlit as st
import yagmail
from fpdf import FPDF

# Configuração do e-mail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FROM_EMAIL = "seu_email@gmail.com"
PASSWORD = "sua_senha"

def send_email(to_email, subject, body, file):
    yag = yagmail.SMTP(FROM_EMAIL, PASSWORD)
    yag.send(to_email, subject, body, attachments=file)

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

def gerar_pdf(orcamento):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Orçamento", 1, 1, "C")
    pdf.ln(10)
    pdf.multi_cell(0, 10, orcamento, 1, "L")
    pdf.output("orcamento.pdf", "F")

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
            gerar_pdf(orcamento)
            file = "orcamento.pdf"
            send_email(to_email, subject, body, file)
            st.success("Orçamento enviado com sucesso!")

if __name__ == "__main__":
    main()