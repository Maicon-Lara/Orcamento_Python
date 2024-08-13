import streamlit as st
import win32com.client as win32
from fpdf import FPDF
import os
import tkinter as tk
from tkinter import filedialog

pdf_path = None

# Função para abrir a janela de diálogo de salvamento
def selecionar_caminho_pdf():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal do tkinter
    caminho_pdf = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        title="Salvar Arquivo"
    )
    pdf_path = (caminho_pdf)
    return caminho_pdf

def gerar_orcamento(nome, endereco, telefone, email, descricao, projeto, horas_estimadas, valor_hora, prazo):
    # Verificação se todos os campos foram preenchidos
    if not all([nome, endereco, telefone, email, descricao, projeto, horas_estimadas, valor_hora, prazo]):
        return "Preencha todos os campos!", None, None

    # Tentativa de conversão dos valores de horas e valor da hora
    try:
        valor_total = float(horas_estimadas) * float(valor_hora)
    except ValueError:
        return "Horas estimadas e valor da hora devem ser números!", None, None

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

    # Abrir a janela de diálogo para selecionar o local de salvamento
    caminho_pdf = selecionar_caminho_pdf()
    if not caminho_pdf:
        return "Nenhum caminho de salvamento foi selecionado.", None, None

    # Verificação se o diretório especificado existe, e criação se necessário
    diretorio = os.path.dirname(caminho_pdf)
    if not os.path.exists(diretorio):
        try:
            os.makedirs(diretorio, exist_ok=True)
        except Exception as e:
            return f"Erro ao criar diretório: {str(e)}", None, None

    # Geração do PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Orçamento", 1, 1, "C")
    pdf.ln(10)
    pdf.multi_cell(0, 10, orcamento)

    try:
        pdf.output(caminho_pdf, "F")
        if os.path.exists(caminho_pdf):
            return orcamento, valor_total, caminho_pdf
        else:
            return "Falha ao salvar o arquivo PDF.", None, None
    except Exception as e:
        return f"Erro ao gerar o PDF: {str(e)}", None, None

def enviar_email(email_destinatario, projeto, descricao, caminho_pdf):
    try:
        # Inicialização do cliente do Outlook
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = email_destinatario
        mail.Subject = projeto
        mail.HTMLBody = descricao

        # Verificação se o anexo existe antes de tentar adicionar
        if os.path.isfile(caminho_pdf):
            try:
                mail.Attachments.Add(caminho_pdf)
                mail.Send()
                print("Email Enviado")
                return True
            except Exception as e:
                print(f"Erro ao enviar e-mail: {str(e)}")
                return False
        else:
            print("Arquivo de anexo não encontrado.")
            return False
    except Exception as e:
        print(f"Erro ao enviar e-mail: {str(e)}")
        return False

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

    
    orcamento = ""
    valor_total = 0

    if st.button("Gerar Orçamento"):
        orcamento, valor_total, pdf_path = gerar_orcamento(nome, endereco, telefone, email_destinatario, descricao, projeto, horas_estimadas, valor_hora, prazo)
        if pdf_path:
            st.write("Orçamento gerado:")
            st.write(orcamento)
            st.success(f"PDF salvo em: {pdf_path}")
            
        else:
            st.error(orcamento)

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
