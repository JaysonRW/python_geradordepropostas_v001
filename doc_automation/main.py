import sys
import os
import json
from core.generator import PDFGenerator

# Configura caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs', 'pdf')

# Adiciona o diretório atual ao path
sys.path.append(BASE_DIR)

def load_data(filename):
    """Carrega dados de um arquivo JSON."""
    file_path = os.path.join(DATA_DIR, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_document(generator, template_name, data_filename, output_name):
    """
    Função auxiliar para gerar um documento específico.
    """
    print(f"\n--- Gerando: {output_name} ---")
    
    # 1. Carregar dados
    print(f"1. Carregando dados de {data_filename}...")
    data = load_data(data_filename)
    
    # 2. Renderizar HTML
    print(f"2. Renderizando template {template_name}...")
    html_content = generator.render_html(template_name, data)
    
    # 3. Gerar PDF
    output_path = os.path.join(OUTPUT_DIR, output_name)
    print(f"3. Gerando PDF em: {output_path}")
    generator.create_pdf(html_content, output_path)
    
    print(f"✔ Documento gerado com sucesso!")

def main():
    """
    Função principal da automação.
    """
    print("Iniciando Sistema de Automação de Documentos...")
    print(f"Diretório de saída: {OUTPUT_DIR}")
    
    try:
        # Inicializar Gerador (uma única vez)
        generator = PDFGenerator(TEMPLATE_DIR)

        # CASO 1: Gerar Proposta Comercial
        generate_document(
            generator, 
            template_name='proposta.html', 
            data_filename='sample_proposal.json', 
            output_name='proposta_comercial_mega_corp.pdf'
        )

        # CASO 2: Gerar Contrato de Prestação de Serviços
        generate_document(
            generator, 
            template_name='contrato.html', 
            data_filename='sample_contract.json', 
            output_name='contrato_servicos_mega_corp.pdf'
        )

        print("\n==============================================")
        print("✔ TODOS OS DOCUMENTOS FORAM GERADOS COM SUCESSO!")
        print("==============================================")

    except Exception as e:
        print(f"\n❌ ERRO FATAL: {e}")

if __name__ == "__main__":
    main()
