import numpy as np
import scipy.io as sio
from scipy.stats import kurtosis

# --- Carregamento do arquivo .mat que contém a informação do motor ---

def carregar_sinal_cwru(caminho_arquivo):
    """
    Carrega o arquivo .mat e extrai o sinal do
    acelerômetro Drive End (DE)
    """
    dados = sio.loadmat(caminho_arquivo)
    # Busca a chave correspondente ao Drive End
    key = [k for k in dados.keys() if 'DE_time' in k][0]
    sinal_bruto = dados[key].ravel()
    return sinal_bruto


# --- Extação de características dos .mat ---

def extrair_caracteristicas(sinal, tamanho_janela = 1024):
    """
    Divide o sinal de vibração bruto em janelas temporais de tamanho fixo
    e calcula o valor RMS e da Curtosi para cada janela (de forma individual).
    """
    n_janelas = len(sinal) // tamanho_janela
    sinal_truncado = sinal[:n_janelas * tamanho_janela]

    # Redimensiona para matriz onde cada linha representa uma janela temporal
    matriz_janelas = sinal_truncado.reshape(n_janelas, tamanho_janela)

    # Aplica a fórmula do RMS
    rms_por_janela = np.sqrt(np.mean(matriz_janelas ** 2, axis=1))

    # Aplica a fórmula da Kurtosis
    kurtosis_por_janela = kurtosis(matriz_janelas, axis = 1)

    # Junta as duas características em uma matriz só
    caracteristicas = np.column_stack((rms_por_janela, kurtosis_por_janela))

    return caracteristicas