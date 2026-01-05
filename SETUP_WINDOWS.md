# Configuração do Ambiente Windows para WeasyPrint

O WeasyPrint requer bibliotecas GTK+ que não são instaladas automaticamente pelo `pip` no Windows.

## Passo 1: Baixar o GTK3 Installer

1. Acesse o repositório oficial do GTK para Windows (mantido pela comunidade):
   - Link direto (recomendado): [gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/download/2022-01-04/gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe)
   - Ou acesse a página de releases: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases

## Passo 2: Instalar

1. Execute o instalador baixado.
2. Siga as instruções padrão.
3. **IMPORTANTE**: Na tela de seleção de componentes, certifique-se de que a opção "Set up PATH environment variable" (ou similar) esteja marcada para adicionar o GTK ao PATH do sistema.

## Passo 3: Verificar Instalação

Após instalar, abra um novo terminal (pode ser necessário reiniciar o VS Code/Trae) e tente executar o script novamente:

```bash
python doc_automation/main.py
```

## Solução de Problemas

Se ainda der erro de DLL, você pode precisar adicionar manualmente a pasta `bin` do GTK ao seu PATH ou configurar no código Python (o `main.py` já tenta ajudar com isso se encontrar a instalação padrão).

Caminho comum da instalação: `C:\Program Files\GTK3-Runtime Win64\bin`
