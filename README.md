# Projetos-Python
=====================

Este é um aplicativo web desenvolvido com Streamlit que gera um orçamento personalizado com base nas informações fornecidas pelo usuário e envia o orçamento por e-mail.

Funcionalidades
---------------

* Gera um orçamento personalizado com base nas informações fornecidas pelo usuário
* Envio de orçamento por e-mail com anexo em PDF

Requisitos
------------

* Python 3.7+
* Streamlit 0.73+
* FPDF 1.7+
* smtplib 0.2+

Instalação
------------

1. Clone o repositório: `git clone https://github.com/your-username/orcamento-generator.git`
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute o aplicativo: `streamlit run app.py`

Uso
----

1. Abra o aplicativo em um navegador web: `http://localhost:8501`
2. Preencha os campos com as informações necessárias
3. Clique no botão "Gerar Orçamento" para gerar o orçamento
4. Clique no botão "Enviar Orçamento por E-mail" para enviar o orçamento por e-mail

Configuração do E-mail
---------------------

* Edite as variáveis `SMTP_SERVER`, `SMTP_PORT`, `FROM_EMAIL` e `PASSWORD` no arquivo `app.py` para configurar o servidor de e-mail

Licença
--------

Este projeto é licenciado sob a licença MIT.

Autor
------

Maicon-Lara
