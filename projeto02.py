import streamlit as st
import yagmail
from fpdf import FPDF

# Configuração do e-mail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FROM_EMAIL = "mixmaicon@gmail.com"


def send_email(to_email, subject, body, file):
    try:
        with yagmail.SMTP(FROM_EMAIL) as yag:
            yag.send(to_email, subject, body, attachments=[file])
        return True
    except yagmail.SMTPAuthenticationError as e:
        print(f"Erro de autenticação: {e}")
        return False
    except yagmail.SMTPException as e:
        print(f"Erro de envio de e-mail: {e}")
        return False
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return False


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

    ###def gerar_pdf(orcamento):
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
    projeto = st.text_input("Nome do projeto")
    horas_estimadas = st.text_input("Horas estimadas")
    valor_hora = st.text_input("Valor da hora trabalhada:")
    prazo = st.text_input("Prazo")

    if st.button("Gerar Orçamento"):
        orcamento, valor_total = gerar_orcamento(
            nome,
            endereco,
            telefone,
            email,
            descricao,
            projeto,
            horas_estimadas,
            valor_hora,
            prazo,
        )
        st.write("Orçamento gerado:")
        st.write(orcamento)

    if st.button("Enviar Orçamento por E-mail"):
        password = st.text_input("Senha do e-mail", type="password")
    if password:
        try:
            to_email = email
            subject = "Orçamento"
            body = "Segue em anexo o orçamento gerado"
            file = "Orçamento.pdf"
            send_email(to_email, subject, body, file, password)
            st.success("Orçamento enviado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao enviar e-mail: {e}")
    else:
        st.error("Senha do e-mail é obrigatória")


if __name__ == "__main__":
    main()
