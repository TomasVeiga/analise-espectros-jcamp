"""
Script: processar_espectros_jcamp.py
Autor: Tomás Mesquita Silva da Veiga
Descrição:
    - Lê arquivos de espectros em formato JCAMP-DX (.JDX ou .DX)
    - Aceita arquivos individuais ou um arquivo ZIP contendo vários espectros
    - Extrai e normaliza os espectros (Y), aplica fator de escala
    - Interpola todos para o mesmo eixo X (mesma dimensão)
    - Gera uma matriz onde cada linha é um espectro processado
    - Salva o resultado final em 'espectros_processados.csv'

----------------------------------------------------------------------------------
Suavização: Quanto MAIOR, mais suave e lisa fica a curva, mas perde detalhes.

Quanto MENOR, mais fiel ao original, porém com mais ruído.

window_length=5 → quase sem suavização

window_length=11 → suave moderado (valor padrão)

window_length=21 → bem suave

window_length=31 → MUITO suave (riscos de apagar picos finos)

----------------------------------------------------------------------------------------
polyorder - 2 ou 3 = comum

4 ou 5 = suaviza pouco, preserva muitos detalhes

valores altos raramente são bons para espectroscopia!!
"""

import os
import io
import zipfile
import numpy as np
import pandas as pd
from jcamp import jcamp_readfile
import tempfile

# SUAVIZAÇÃO (ADICIONADO)
from scipy.signal import savgol_filter

# ======================================================
# 🧩 CONFIGURAÇÕES GERAIS
# ======================================================

# Caminho do arquivo ZIP ou pasta contendo os .JDX
# O CAMINHO PODE MUDAR DE PESSOA PARA PESSOA, BASTA VER ONDE SUA PASTA ZIP COM OS ESPECTROS ESTÁ
CAMINHO = "C:/Users/Tomas/OneDrive/Documentos/estagioespectros/JCAMP_051524.zip"

# Intervalo e número de pontos para padronizar todos os espectros
X_INICIAL = 650       # cm⁻¹
X_FINAL = 4000        # cm⁻¹
NUM_PONTOS = 2000     # número de pontos do eixo comum

# Caminho de saída
ARQUIVO_SAIDA = "espectros_processados.csv"

# ======================================================
# ⚙️ FUNÇÃO PARA LER E PROCESSAR UM ÚNICO ARQUIVO .JDX
# ======================================================

def processar_jdx(conteudo_bytes):
    """
    Lê o conteúdo de um arquivo JDX e retorna arrays X e Y normalizados.
    """
    try:
        # Criar arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jdx") as tmp:
            tmp.write(conteudo_bytes)
            tmp_path = tmp.name

        # Ler o arquivo temporário com jcamp
        dados = jcamp_readfile(tmp_path)

        # Apagar o arquivo temporário
        os.remove(tmp_path)

        x = np.array(dados["x"], dtype=float) * float(dados.get("xfactor", 1))
        y = np.array(dados["y"], dtype=float) * float(dados.get("yfactor", 1))

        # Remove NaN ou valores inválidos
        mascara = np.isfinite(x) & np.isfinite(y)
        x, y = x[mascara], y[mascara]

        # Normalização Min-Max
        if np.ptp(y) > 0:
            y = (y - np.min(y)) / (np.max(y) - np.min(y))
        else:
            y = np.zeros_like(y)

        # 🔹 SUAVIZAÇÃO (ADICIONADO)
        # Quanto maior o window_length, mais suave (deve ser ímpar)
        y = savgol_filter(y, window_length=17, polyorder=3)

        return x, y

    except Exception as e:
        print(f"[ERRO] Falha ao processar arquivo JDX: {e}")
        return None, None

# ======================================================
#  FUNÇÃO PARA LER ARQUIVOS DE UM ZIP
# ======================================================

def ler_arquivos_zip(caminho_zip):
    """
    Lê todos os arquivos .JDX dentro de um ZIP e retorna uma lista de (nome, conteúdo)
    """
    arquivos = []
    with zipfile.ZipFile(caminho_zip, "r") as zip_ref:
        for nome_arquivo in zip_ref.namelist():
            if nome_arquivo.lower().endswith((".jdx", ".dx")):
                conteudo = zip_ref.read(nome_arquivo)
                arquivos.append((nome_arquivo, conteudo))
    return arquivos

# ======================================================
#  PIPELINE PRINCIPAL (SEM ALTERAÇÃO)
# ======================================================

def main():
    # Gera o eixo X padrão
    x_padrao = np.linspace(400, 4000, 3600)
    espectros_processados = []
    nomes_arquivos = []

    # Detecta se o caminho é ZIP ou pasta
    arquivos_lidos = []
    if CAMINHO.lower().endswith(".zip"):
        print(" Lendo arquivos de dentro do ZIP...")
        arquivos_lidos = ler_arquivos_zip(CAMINHO)
    else:
        print("📂 Lendo arquivos de uma pasta...")
        for nome in os.listdir(CAMINHO):
            if nome.lower().endswith((".jdx", ".dx")):
                with open(os.path.join(CAMINHO, nome), "rb") as f:
                    arquivos_lidos.append((nome, f.read()))

    # Processa cada espectro
    for nome, conteudo in arquivos_lidos:
        print(f"🔹 Processando: {nome}")
        x, y = processar_jdx(conteudo)
        if x is None or len(x) == 0:
            print(f"⚠️  Erro ao processar {nome}, ignorando...")
            continue

        # Interpolação para eixo comum
        y_interp = np.interp(x_padrao, x, y)
        espectros_processados.append(y_interp)
        nomes_arquivos.append(nome)

    # Converte para DataFrame
    df_final = pd.DataFrame(espectros_processados, columns=[f"x_{i}" for i in range(len(x_padrao))])
    df_final.insert(0, "Arquivo", nomes_arquivos)

    # Salva em CSV
    df_final.to_csv(ARQUIVO_SAIDA, index=False, sep=';')
    print(f"\n✅ Processamento concluído!")
    print(f"→ Arquivo salvo em: {os.path.abspath(ARQUIVO_SAIDA)}")
    print(f"→ Total de espectros processados: {len(df_final)}")

# ======================================================
#  EXECUÇÃO
# ======================================================

if __name__ == "__main__":
    main()
