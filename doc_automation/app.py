import streamlit as st
import pandas as pd
import json
import os
import sys
from datetime import datetime

# Adiciona o diretório atual ao path para importar o core
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from core.generator import PDFGenerator

# Configurações da Página
st.set_page_config(
    page_title="Gerador de Propostas",
    page_icon="📄",
    layout="wide"
)

# Caminhos
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs', 'pdf')

def main():
    st.title("📄 Sistema de Automação de Documentos")
    st.markdown("---")

    # Sidebar - Seleção de Template
    st.sidebar.header("Configurações")
    template_option = st.sidebar.selectbox(
        "Selecione o Tipo de Documento",
        ["Proposta Comercial", "Contrato de Serviços"]
    )

    if template_option == "Proposta Comercial":
        render_proposal_form()
    elif template_option == "Contrato de Serviços":
        render_contract_form()

def render_proposal_form():
    st.header("Nova Proposta Comercial")

    # Tabs para organização
    tab1, tab2, tab3, tab4 = st.tabs(["🏢 Empresa & Cliente", "📝 Detalhes da Proposta", "💰 Serviços & Valores", "📅 Cronograma"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Sua Empresa")
            company_name = st.text_input("Nome da Empresa", "Trae Solutions Tech")
            company_address = st.text_input("Endereço", "Av. Paulista, 1000")
            company_city = st.text_input("Cidade/Estado", "São Paulo - SP")
            company_email = st.text_input("Email", "contato@traesolutions.com.br")
            company_phone = st.text_input("Telefone", "(11) 3333-4444")
        
        with col2:
            st.subheader("Cliente")
            client_name = st.text_input("Empresa Cliente", "Cliente Exemplo Ltda")
            client_contact = st.text_input("Nome do Contato", "Fulano de Tal")
            client_email = st.text_input("Email do Cliente", "fulano@cliente.com")

    with tab2:
        st.subheader("Dados da Proposta")
        prop_title = st.text_input("Título da Proposta", "Sistema de Automação")
        prop_date = st.text_input("Data", datetime.now().strftime("%d de %B de %Y"))
        prop_validity = st.text_input("Validade", "15 dias")
        prop_desc = st.text_area("Descrição", "Desenvolvimento de solução backend...")
        prop_goal = st.text_area("Objetivo", "Automatizar processos manuais...")

    with tab3:
        st.subheader("Serviços")
        st.info("Adicione ou edite os serviços abaixo.")
        
        # Dados iniciais para a tabela
        default_services = [
            {"name": "Consultoria", "hours": 10.0, "rate": 150.00},
            {"name": "Desenvolvimento", "hours": 40.0, "rate": 150.00},
        ]
        
        df_services = pd.DataFrame(default_services)
        column_config = {
            "name": st.column_config.TextColumn("Serviço", required=True),
            "hours": st.column_config.NumberColumn("Horas", min_value=0.0, step=0.5, required=True),
            "rate": st.column_config.NumberColumn("Valor Hora", min_value=0.0, step=10.0, format="R$ %.2f", required=True)
        }
        edited_df_services = st.data_editor(df_services, num_rows="dynamic", column_config=column_config)

    with tab4:
        st.subheader("Cronograma")
        default_timeline = [
            {"phase": "Fase 1", "desc": "Planejamento", "duration": "1 semana"},
            {"phase": "Fase 2", "desc": "Execução", "duration": "2 semanas"},
        ]
        df_timeline = pd.DataFrame(default_timeline)
        edited_df_timeline = st.data_editor(df_timeline, num_rows="dynamic")

    st.markdown("---")
    
    if st.button("Gerar Proposta PDF", type="primary"):
        # Montar o dicionário de dados (JSON structure)
        data = {
            "company": {
                "name": company_name,
                "address": company_address,
                "city": company_city,
                "email": company_email,
                "phone": company_phone
            },
            "client": {
                "company_name": client_name,
                "contact_name": client_contact,
                "email": client_email
            },
            "proposal": {
                "title": prop_title,
                "date": prop_date,
                "validity": prop_validity,
                "description": prop_desc,
                "goal": prop_goal
            },
            "services": edited_df_services.to_dict("records"),
            "timeline": edited_df_timeline.to_dict("records")
        }

        generate_and_show_pdf("proposta.html", data, f"proposta_{client_name}.pdf")

def render_contract_form():
    st.header("Novo Contrato de Serviços")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Contratada (Você)")
        contractor_name = st.text_input("Razão Social", "Trae Solutions Tech LTDA")
        contractor_cnpj = st.text_input("CNPJ Contratada", "12.345.678/0001-90")
        contractor_addr = st.text_input("Endereço Completo", "Av. Paulista, 1000 - SP")
        contractor_rep = st.text_input("Representante Legal", "Carlos Trae")
        
    with col2:
        st.subheader("Contratante (Cliente)")
        client_name = st.text_input("Razão Social Cliente", "Mega Corp S.A.")
        client_cnpj = st.text_input("CNPJ Cliente", "98.765.432/0001-10")
        client_addr = st.text_input("Endereço Cliente", "Rua Funchal, 200 - SP")
        client_rep = st.text_input("Representante Cliente", "Maria Souza")

    st.subheader("Detalhes do Contrato")
    c_number = st.text_input("Número do Contrato", "2026/001")
    c_date = st.text_input("Data de Assinatura", datetime.now().strftime("%d de %B de %Y"))
    c_object = st.text_area("Objeto do Contrato", "Prestação de serviços de desenvolvimento...")
    c_value = st.text_input("Valor Global (Texto)", "R$ 10.000,00 (Dez mil reais)")

    st.subheader("Cláusulas")
    default_clauses = [
        {"title": "1. Do Objeto", "text": "Descrição do objeto..."},
        {"title": "2. Do Prazo", "text": "O prazo será de..."},
    ]
    df_clauses = pd.DataFrame(default_clauses)
    edited_df_clauses = st.data_editor(df_clauses, num_rows="dynamic", use_container_width=True)

    if st.button("Gerar Contrato PDF", type="primary"):
        data = {
            "contract_number": c_number,
            "date_signed": c_date,
            "contractor": {
                "name": contractor_name,
                "cnpj": contractor_cnpj,
                "address": contractor_addr,
                "representative": contractor_rep
            },
            "contracted": {
                "name": client_name,
                "cnpj": client_cnpj,
                "address": client_addr,
                "representative": client_rep
            },
            "object": c_object,
            "value": c_value,
            "clauses": edited_df_clauses.to_dict("records")
        }
        
        generate_and_show_pdf("contrato.html", data, f"contrato_{client_name}.pdf")

def generate_and_show_pdf(template_name, data, output_filename):
    with st.spinner('Gerando PDF...'):
        try:
            generator = PDFGenerator(TEMPLATE_DIR)
            
            # Renderiza HTML
            html_content = generator.render_html(template_name, data)
            
            # Caminho de saída
            # Sanitizar nome do arquivo
            safe_filename = "".join([c for c in output_filename if c.isalpha() or c.isdigit() or c==' ' or c=='.']).rstrip()
            output_path = os.path.join(OUTPUT_DIR, safe_filename)
            
            # Gera PDF
            generator.create_pdf(html_content, output_path)
            
            st.success("PDF Gerado com Sucesso!")
            
            # Mostrar botão de download
            with open(output_path, "rb") as pdf_file:
                PDFbyte = pdf_file.read()

            st.download_button(label="📥 Baixar PDF",
                                data=PDFbyte,
                                file_name=safe_filename,
                                mime='application/octet-stream')
            
            # Visualização (Iframe básico se o navegador suportar)
            # Nota: Exibir PDF diretamente em Streamlit local pode ser tricky, 
            # o download button é o mais garantido.
            
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")

if __name__ == "__main__":
    main()
