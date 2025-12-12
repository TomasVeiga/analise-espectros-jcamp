🧪 Análise Automatizada de Espectros JCAMP-DX

Sistema desenvolvido durante o estágio no Departamento de Química da Faculdade de Filosofia, Ciências e Letras de Ribeirão Preto (USP-RP) para automatizar a leitura, padronização e tratamento de espectros no formato JCAMP-DX (.jdx).

📌 Descrição do Projeto

Este projeto consiste no desenvolvimento de um software em Python capaz de:

Ler arquivos de espectros no formato JCAMP-DX

Padronizar todos os espectros em um único eixo (ex.: 400 a 4000 cm⁻¹)

Aplicar tratamentos matemáticos como suavização, normalização e correção de linha base

Realizar automação de processamento para dezenas ou centenas de arquivos

Permitir visualização gráfica dos espectros processados

Disponibilizar uma interface gráfica simples (Tkinter) para facilitar o uso

Gerar arquivos de saída padronizados e prontos para análise científica

O software foi desenvolvido como parte das atividades do estágio, com foco em auxiliar pesquisadores na análise rápida, reprodutível e padronizada de espectros.

✨ Funcionalidades

📥 Leitura de arquivos .JDX (parser próprio)

📊 Padronização do eixo x para todos os espectros

🔧 Suavização (ex.: média móvel, Savitzky–Golay)

📉 Correção de linha de base

📈 Normalização dos espectros

⚙️ Automação do processamento de múltiplos arquivos

🖥️ Interface gráfica (Tkinter) para seleção de arquivos e execução

📂 Geração de espectros padronizados

🔍 Validação dos resultados por comparação visual e numérica

📂 Estrutura do Projeto (exemplo)
analise-espectros-jcamp/
│
├── src/
│   ├── parser.py
│   ├── preprocessing.py
│   ├── smoothing.py
│   ├── gui.py
│   └── utils.py
│
├── examples/
│   └── espectros-exemplo/
│
├── requirements.txt
└── README.md


(Se quiser, podemos adaptar isso para refletir exatamente sua estrutura real.)

🛠️ Instalação
1. Criar ambiente virtual (recomendado)
python -m venv venv

2. Ativar ambiente virtual

Windows

venv\Scripts\activate


Linux/Mac

source venv/bin/activate

3. Instalar dependências
pip install -r requirements.txt


Se você ainda não criou o requirements.txt, basta rodar:

pip freeze > requirements.txt

🚀 Como usar
1. Executar a interface gráfica
python src/gui.py

2. Selecionar os arquivos .jdx

Pela interface, selecione:

Um ou vários espectros para análise

A pasta de saída

Opções de tratamento (suavização, normalização, etc.)

3. Processar os espectros

O software irá:

Ler cada arquivo

Aplicar padronização de eixo

Aplicar as técnicas de pré-processamento

Salvar espectros novos e gráficos

Exibir visualizações se configurado

🧮 Principais Técnicas Implementadas

Parser JCAMP-DX (leitura chave–valor + matriz XY)

Interpolação (ex.: np.interp) para padronização

Suavização (média móvel ou Savitzky–Golay)

Normalização vetorial ou min–max

Baseline correction (polinomial ou linear)

Tratamento de ruído

Automação com loop de diretório

📘 Tecnologias Utilizadas

Python 3.x

NumPy

SciPy

Matplotlib

Tkinter

OS / Glob (manipulação de arquivos)

👨‍🔬 Contexto Acadêmico

Este software foi desenvolvido como parte do estágio curricular no:

Departamento de Química — FFCLRP / USP
Universidade de São Paulo
Ribeirão Preto – SP

Orientação: [Nome do orientador (se quiser colocar)]
Atividades desenvolvidas incluíram estudo de espectroscopia, formatação JCAMP-DX, processamento matemático e desenvolvimento de software científico.

👨‍💻 Autor

Tomas Veiga
Estagiário de Desenvolvimento — Departamento de Química / USP
GitHub: https://github.com/TomasVeiga
