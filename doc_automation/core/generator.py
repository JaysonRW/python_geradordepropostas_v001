import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

class PDFGenerator:
    """
    Classe responsável por gerenciar a renderização de templates e geração de PDFs.
    """
    
    def __init__(self, templates_dir):
        """
        Inicializa o gerador com o diretório de templates.
        
        Args:
            templates_dir (str): Caminho absoluto para a pasta de templates.
        """
        self.templates_dir = templates_dir
        # Configura o ambiente do Jinja2
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))
    
    def render_html(self, template_name, context):
        """
        Renderiza o template HTML com os dados fornecidos.
        
        Args:
            template_name (str): Nome do arquivo de template (ex: 'proposta.html').
            context (dict): Dicionário com os dados para preencher o template.
            
        Returns:
            str: O conteúdo HTML renderizado.
        """
        try:
            template = self.env.get_template(template_name)
            return template.render(context)
        except Exception as e:
            raise Exception(f"Erro ao renderizar template '{template_name}': {e}")

    def create_pdf(self, html_content, output_path):
        """
        Gera o arquivo PDF a partir do conteúdo HTML.
        
        Args:
            html_content (str): O HTML já renderizado.
            output_path (str): Caminho completo onde o PDF será salvo.
        """
        try:
            # Garante que o diretório de saída existe
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Gera o PDF usando WeasyPrint
            HTML(string=html_content, base_url=self.templates_dir).write_pdf(output_path)
            
        except OSError as e:
             if "cannot load library" in str(e) or "module not found" in str(e).lower():
                 raise OSError(
                     "Erro de dependência GTK3. Verifique se o GTK3 Runtime está instalado e no PATH.\n"
                     "Consulte SETUP_WINDOWS.md para mais detalhes."
                 ) from e
             raise e
        except Exception as e:
            raise Exception(f"Erro ao gerar PDF: {e}")
