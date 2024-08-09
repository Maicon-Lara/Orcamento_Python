import streamlit as st
import win32com.client as win32
from fpdf import FPDF

def gerar_orcamento(
    nome,
    endereco,
    telefone,
    email,
    descricao,
    projeto,
    horas_estimadas,
    valor_hora,
    prazo,
):
    # validação de entrada
    if not nome or not endereco or not telefone or not email or not descricao or not projeto or not horas_estimadas or not valor_hora or not prazo:
        return "Preencha todos os campos!"

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
    Valor total: {str(valor_total)}
    """

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Orçamento", 1, 1, "C")
    pdf.ln(10)
    pdf.multi_cell(0, 10, orcamento, 1, "L")
    pdf.output("orcamento.pdf", "F")
    return orcamento, valor_total

def enviar_email(email_destinatario, projeto, descricao, anexo):
    # criar a integração com o outlook
    outlook = win32.Dispatch('outlook.application')

    # criar um email
    email = outlook.CreateItem(0)

    # configurar as informações do seu e-mail
    email.To = email_destinatario
    email.Subject = projeto
    email.HTMLBody = descricao

    email.Attachments.Add(anexo)

    email.Send()
    print("Email Enviado")
    return True

def main():
    st.title("Gerar Orçamento")
    st.write("Preencha os campos abaixo para gerar um orçamento")

    nome = st.text_input("Nome")
    endereco = st.text_input("Endereço")
    telefone = st.text_input("Telefone")
    email_destinatario = st.text_input("E-mail")
    descricao = st.text_area("Descrição")
    projeto = st.text_input("Nome do projeto")
    horas_estimadas = st.text_input("Horas estimadas")
    valor_hora = st.text_input("Valor da hora trabalhada:")
    prazo = st.text_input("Prazo")

    if st.button("Gerar Orçamento"):
        orcamento = gerar_orcamento(
            nome,
            endereco,
            telefone,
            email_destinatario,
            descricao,
            projeto,
            horas_estimadas,
            valor_hora,
            prazo,
        )
        st.write("Orçamento gerado:")
        st.write(orcamento)

    if st.button("Enviar Orçamento por E-mail"):
        anexo = "C:\\ws-python\\Projeto1\\template.png"
        if enviar_email(email_destinatario, projeto, descricao, anexo):
            st.success("Orçamento enviado com sucesso!")
        else:
            st.error("Erro ao enviar e-mail")

if __name__ == "__main__":
    main()