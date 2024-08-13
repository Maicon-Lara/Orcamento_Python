import streamlit as st
import win32com.client as win32
from fpdf import FPDF
import os

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
    # Validação de entrada: Verifica se todos os campos foram preenchidos
    if not nome or not endereco or not telefone or not email or not descricao or not projeto or not horas_estimadas or not valor_hora or not prazo:
        return "Preencha todos os campos!", None, None

    # Conversão e cálculo de valores: Tenta converter horas_estimadas e valor_hora para inteiros e calcula o valor total
    try:
        valor_total = int(horas_estimadas) * int(valor_hora)
    except ValueError:
        return "Horas estimadas e valor da hora devem ser números inteiros!", None, None

    # Criação do conteúdo do orçamento
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

    # Criação e configuração do PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Orçamento", 1, 1, "C")
    pdf.ln(10)
    pdf.multi_cell(0, 10, orcamento)

    # Caminho onde o PDF será salvo
    pdf_output_path = "C:\\Users\\maicon.lara\\Desktop\\Projeto_Python\\orcamento.pd"  # Ajustar o caminho conforme necessário
    #C:\\Users\\maicon.lara\\Desktop\\Projeto_Python\\orcamento.pdf
    
    try:
        # Tenta salvar o PDF no caminho especificado
        pdf.output(pdf_output_path, "F")
        # Verifica se o arquivo foi salvo corretamente
        if os.path.exists(pdf_output_path):
            return orcamento, valor_total, pdf_output_path
        else:
            return "Falha ao salvar o arquivo PDF.", None, None
    except Exception as e:
        # Captura e retorna erros durante a criação do PDF
        return f"Erro ao gerar o PDF: {str(e)}", None, None

def enviar_email(email_destinatario, projeto, descricao, anexo):
    # Criação da integração com o Outlook
    outlook = win32.Dispatch('outlook.application')

    # Criação do e-mail
    mail = outlook.CreateItem(0)  # Renomeado para evitar conflito

    # Configuração do e-mail
    mail.To = email_destinatario
    mail.Subject = projeto
    mail.HTMLBody = descricao

    # Verifica se o anexo existe antes de tentar adicionar
    if os.path.exists(anexo):
        mail.Attachments.Add(anexo)
        try:
            mail.Send()
            print("Email Enviado")
            return True
        except Exception as e:
            print(f"Erro ao enviar e-mail: {str(e)}")
            return False
    else:
        print("Arquivo de anexo não encontrado.")
        return False

def main():
    st.title("Gerar Orçamento")
    st.write("Preencha os campos abaixo para gerar um orçamento")

    # Coleta de dados de entrada do usuário
    nome = st.text_input("Nome")
    endereco = st.text_input("Endereço")
    telefone = st.text_input("Telefone")
    email_destinatario = st.text_input("E-mail")
    descricao = st.text_area("Descrição")
    projeto = st.text_input("Nome do projeto")
    horas_estimadas = st.text_input("Horas estimadas")
    valor_hora = st.text_input("Valor da hora trabalhada:")
    prazo = st.text_input("Prazo")

    pdf_path = None  # Inicializa pdf_path como None para evitar uso antes da definição
    orcamento = ""
    valor_total = 0

    # Botão para gerar o orçamento
    if st.button("Gerar Orçamento"):
        orcamento, valor_total, pdf_path = gerar_orcamento(
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
        if pdf_path:
            st.write("Orçamento gerado:")
            st.write(orcamento)
            st.success(f"PDF salvo em: {pdf_path}")
        else:
            st.error(orcamento)  # Exibindo a mensagem de erro, se houver

    # Botão para enviar o orçamento por e-mail
    if st.button("Enviar Orçamento por E-mail"):
        if pdf_path and os.path.exists(pdf_path):
            if enviar_email(email_destinatario, projeto, descricao, pdf_path):
                st.success("Orçamento enviado com sucesso!")
            else:
                st.error("Erro ao enviar e-mail")
        else:
            st.error("O arquivo PDF não foi encontrado ou não foi gerado ainda.")

if __name__ == "__main__":
    main()
