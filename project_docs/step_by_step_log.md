# Registro Passo-a-Passo do Projeto doc_automation

Este documento registra todas as alterações, criações de arquivos e suas finalidades no projeto `doc_automation`.

## Estrutura do Projeto

O projeto foi inicializado com a seguinte estrutura:

```
doc_automation/
│
├── core/
│   ├── __init__.py      # Inicializador do pacote core, contém lógica central.
│
├── templates/           # Diretório para armazenar modelos de documentos.
│
├── outputs/
│   └── pdf/             # Diretório de saída para arquivos PDF gerados.
│
├── data/                # Diretório para dados de entrada (JSON, CSV, etc.).
│
└── main.py              # Ponto de entrada da aplicação.
```

## Histórico de Alterações

### [2025-01-01] - Inicialização do Projeto

#### Criação da Estrutura de Diretórios
- **Ação**: Criação das pastas `core`, `templates`, `outputs/pdf`, `data`.
- **Propósito**: Organizar o código fonte, templates, saídas e dados de forma modular e escalável.

#### Criação de Arquivos Iniciais
1.  **`doc_automation/main.py`**
    - **Função**: Ponto de entrada principal da aplicação.
    - **Utilidade**: Orquestra a execução da automação, chamando funções do módulo `core`. Atualmente contém um print de inicialização básico.

2.  **`doc_automation/core/__init__.py`**
    - **Função**: Marca o diretório `core` como um pacote Python.
    - **Utilidade**: Permite a importação de módulos dentro de `core`. Contém docstring inicial.

### [2025-01-01] - Criação do Primeiro Template e Teste de Geração

#### Criação de Templates
- **`templates/proposta.html`**: Criado um template HTML estático com CSS embutido.
    - **Estilo**: Layout profissional, tamanho A4, com cabeçalho, rodapé, tabelas estilizadas e numeração de página.
    - **Objetivo**: Validar a capacidade de renderização do motor WeasyPrint antes de implementar a lógica dinâmica.

#### Configuração e Testes
- **Atualização do `main.py`**: O arquivo foi atualizado para realizar um teste prático:
    1.  Lê o arquivo `templates/proposta.html`.
    2.  Utiliza o WeasyPrint para converter o HTML em PDF.
    3.  Salva o resultado em `outputs/pdf/proposta_teste.pdf`.
    4.  Inclui tratamento de erro específico para verificar a instalação das dependências GTK3 no Windows.

- **Configuração de Ambiente Windows**:
    - Identificada a necessidade do GTK3 Runtime para o WeasyPrint no Windows.
    - Criado arquivo `SETUP_WINDOWS.md` com instruções de instalação.
    - Dependência resolvida e teste executado com sucesso.

#### Resultados
- **PDF Gerado**: `outputs/pdf/proposta_teste.pdf` gerado com sucesso. O layout HTML/CSS foi renderizado corretamente para o formato PDF.

### [2025-01-01] - Implementação da Geração Dinâmica (Jinja2)

#### Novos Arquivos
- **`data/sample_proposal.json`**: Contém dados estruturados de exemplo (empresa, cliente, serviços, cronograma) para simular uma fonte de dados real.
- **`core/generator.py`**:
    - Criada a classe `PDFGenerator`.
    - Método `render_html`: Combina o template HTML com os dados JSON usando Jinja2.
    - Método `create_pdf`: Abstrai a chamada ao WeasyPrint para gerar o arquivo final.

#### Alterações
- **`templates/proposta.html`**:
    - Substituídos textos estáticos por variáveis Jinja2 (ex: `{{ client.name }}`).
    - Adicionados loops `{% for %}` para renderizar listas de serviços e cronograma dinamicamente.
    - Adicionada lógica de cálculo de totais diretamente no template (embora idealmente deva ser feito no backend, serve para demonstrar a capacidade do template).
- **`main.py`**:
    - Refatorado para carregar o JSON.
    - Instancia o `PDFGenerator`.
    - Gera um PDF com nome dinâmico baseado no nome do cliente (ex: `proposta_mega_corp_s.a..pdf`).

#### Resultado
- O sistema agora gera propostas personalizadas automaticamente a partir de um arquivo de dados.
- Teste realizado com sucesso gerando `outputs/pdf/proposta_mega_corp_s.a..pdf`.

### [2025-01-01] - Teste de Flexibilidade (Novo Template de Contrato)

#### Novos Arquivos
- **`templates/contrato.html`**:
    - Novo layout com estilo jurídico (fontes serifadas, texto justificado, numeração de cláusulas).
    - Estrutura completamente diferente da Proposta Comercial.
- **`data/sample_contract.json`**:
    - Novo conjunto de dados simulando um contrato real (partes, cláusulas, valores, assinaturas).

#### Alterações no `main.py`
- Refatoração para suportar a geração de múltiplos documentos em sequência.
- Criada função auxiliar `generate_document` para reutilizar a lógica de carga/renderização/geração.
- O script agora gera dois arquivos:
    1.  `proposta_comercial_mega_corp.pdf` (Baseado no template de Proposta).
    2.  `contrato_servicos_mega_corp.pdf` (Baseado no template de Contrato).

#### Resultados
- O sistema provou ser flexível: o mesmo motor (`PDFGenerator`) conseguiu processar dois tipos de documentos com layouts e estruturas de dados completamente distintos sem necessidade de alteração no código Core.

### [2025-01-01] - Interface Gráfica com Streamlit

#### Objetivo
Fornecer uma interface visual amigável (UI) para que usuários finais possam preencher os dados da proposta/contrato e gerar PDFs sem editar arquivos JSON ou código Python.

#### Implementação
- **Bibliotecas**: `streamlit` (UI) e `pandas` (tabelas editáveis).
- **Arquivo**: `doc_automation/app.py`.
- **Funcionalidades**:
    - **Seleção de Template**: Menu lateral para escolher entre "Proposta Comercial" e "Contrato de Serviços".
    - **Formulários Dinâmicos**: Campos de texto organizados em abas para preenchimento de dados da empresa e do cliente.
    - **Tabelas Editáveis**: Uso de `st.data_editor` para permitir adicionar/remover itens de serviço e etapas do cronograma visualmente.
    - **Geração e Download**: Botão que processa os dados inseridos, chama o `PDFGenerator` e disponibiliza o arquivo PDF para download imediato.

#### Como Executar
```bash
streamlit run doc_automation/app.py
```
A aplicação abrirá automaticamente no navegador padrão (geralmente em `http://localhost:8501`).

#### Próximos Passos
- Adicionar persistência (salvar propostas criadas em banco de dados ou JSON).
- Melhorar a visualização do PDF dentro da própria ferramenta (atualmente é feito download).
- Criar uma interface de linha de comando (CLI) mais robusta para passar arquivos de dados como argumento.

### [2025-01-01] - Instalação de Dependências

#### Bibliotecas Instaladas
- **Jinja2**: Motor de templates para Python. Será usado para preencher os modelos de documentos com dados dinâmicos.
- **WeasyPrint**: Biblioteca para renderização de HTML e CSS para PDF. Será usada para gerar os arquivos finais de saída.

#### Arquivos Criados
- **`requirements.txt`**: Lista as dependências do projeto para facilitar a instalação em outros ambientes.

#### Status Atual
- Projeto capaz de rodar localmente (Windows) e pronto para deploy em nuvem.
- Interface amigável substituindo a necessidade de CLI para operação comum.
- Arquivos de configuração (`packages.txt` e `config.toml`) validados para deploy no Streamlit Cloud.

### [2025-01-04] - Finalização para Testes de Terceiros

#### Ações Concluídas
- **Validação de Arquivos**: Confirmada a existência e conteúdo de `requirements.txt` e `.streamlit/config.toml`.
- **Criação de `packages.txt`**: Definidas as bibliotecas do sistema (Linux/Debian) necessárias para o WeasyPrint operar na nuvem.
- **Próximos Passos (Usuário)**:
    1. Subir o código para um repositório GitHub.
    2. Criar conta no Streamlit Cloud.
    3. Conectar o repositório e fazer o deploy.

### [2025-01-04] - Interface Gráfica com Streamlit

#### Criação da Aplicação Web
- **`doc_automation/app.py`**:
    - Criada interface interativa utilizando a biblioteca **Streamlit**.
    - **Funcionalidades**:
        - Menu lateral para seleção entre "Proposta Comercial" e "Contrato".
        - Formulários organizados em abas (Empresa, Cliente, Serviços, Cronograma).
        - Tabelas editáveis (`st.data_editor`) para inserção dinâmica de serviços e fases do projeto.
        - Botão de geração que aciona o motor WeasyPrint e disponibiliza o download imediato do PDF.
    - **Objetivo**: Permitir que usuários não-técnicos gerem documentos sem editar arquivos JSON manualmente.

#### Preparação para Deploy
- **`packages.txt`**: Criado arquivo de dependências de sistema (apt-get) para o WeasyPrint funcionar em ambientes Linux (como Streamlit Cloud). Inclui bibliotecas como `libcairo2`, `libpango-1.0-0`, etc.
- **`.streamlit/config.toml`**: Configuração para execução "headless" (sem abrir navegador automaticamente) em servidores de produção.

#### Status Atual
- Projeto capaz de rodar localmente (Windows) e pronto para deploy em nuvem.
- Interface amigável substituindo a necessidade de CLI para operação comum.
