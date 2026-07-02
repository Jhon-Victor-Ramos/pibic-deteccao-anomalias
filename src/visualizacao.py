import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
from scipy.stats import kurtosis
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score

# Configuração global de plotagem para integração com relatórios acadêmicos (LaTeX)
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif"
})

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


def extrair_caracteristicas(sinal, tamanho_janela = 1024):
    """
    Divide o sinal de vibração bruto em janelas temporais de tamanho fixo
    e calcula o valor RMS para cada janela individual.
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


def plotar_analise_rms(valores_rms, predicoes, tamanho_janela, acuracia, precisao, recall):
    """
    Plota o sinal temporal do RMS e sinaliza as anomalias encontradas
    com marcadores de 'X' em vermelho.
    """
    plt.figure(figsize=(10, 5))

    plt.plot(valores_rms[:, 0], label="Sinal RMS", color="blue")

    # Identifica os índices e os respectivos valores de RMS das anomalias preditas
    indice_anomalia = np.arange(len(valores_rms))[predicoes == -1]


    rms_anomalias = valores_rms[predicoes == -1, 0]

    # Desenha as marcas vermelhas
    plt.scatter(indice_anomalia, rms_anomalias, marker="X", color="red", label="Anomalia encontrada")

    # Estilização do gráfico
    plt.title(rf'Detecção de Anomalias no Sinal de Vibração (Dataset CWRU) - Janela: ${tamanho_janela}$')
    plt.xlabel(r'Tempo ($t$)')
    plt.ylabel(r'RMS da Vibração ($g$)')

    # Criando uma caixa de texto para o gráfico
    texto_resultados = (f"Acurácia: {acuracia:.2%}\n"
                        f"Precisão: {precisao:.2%}\n"
                        f"Recall: {recall:.2%}\n"
                        f"Anomalias: {len(rms_anomalias)}")

    # Inserindo a caixa de texto no canto inferior direito
    plt.text(0.947, 0.05, texto_resultados, transform=plt.gca().transAxes,
             fontsize=10, verticalalignment='bottom', horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    #Salvando a imagem
    plt.savefig("grafico_final_pibic.png", dpi=300, bbox_inches='tight')

    plt.legend()
    plt.grid(True)
    plt.show()

    print(f"{len(rms_anomalias)} anomalias foram encontradas")


if __name__ == "__main__":
    # --- Carregando e processando os sinais ---
    sinal_normal = carregar_sinal_cwru("../data/97.mat")
    sinal_falha = carregar_sinal_cwru("../data/105.mat")

    tamanho_da_janela = 1024

    caracteristicas_normal = extrair_caracteristicas(sinal_normal, tamanho_janela=tamanho_da_janela)
    caracteristicas_falha = extrair_caracteristicas(sinal_falha, tamanho_janela=tamanho_da_janela)

    # União dos sinais temporais e redimensionamento para duas dimensões
    valores_caracteristicas = np.concatenate([caracteristicas_normal, caracteristicas_falha])

    # Treinamento do modelo com o funcionamento normal da máquina
    scaler = StandardScaler()

    # O scaler aprende somente com o funcionamento normal da máquina
    scaler.fit(caracteristicas_normal)

    # Transformação das características da zona saudável para a escala (média: 0; variância: 1)
    normal_escala = scaler.transform(caracteristicas_normal)

    # Aplica a escala aprendida a todos os dados
    # Como o modelo não conhece os dados da falha, eles terão valores muito altos e serão
    # facilmente isolados
    valores_escalados = scaler.transform(valores_caracteristicas)

    # --- Um "gabarito", para ver o desempenho do modelo ---
    #  1: estado normal,
    # -1: estado de falha
    valores_concatenados = np.concatenate([
        np.ones(len(caracteristicas_normal)),
        -np.ones(len(caracteristicas_falha))
    ])

    # --- treinando o modelo e realizando predições ---
    modelo = IsolationForest(contamination="auto", random_state=32)
    modelo.fit(normal_escala)
    predicoes_originais = modelo.predict(valores_escalados)

    predicoes_filtradas = np.ones(len(predicoes_originais))

    # --- Filtro para verificar as reais anomalias ---
    for i in range(2, len(predicoes_originais)):
        if predicoes_originais[i] == -1 and predicoes_originais[i - 1] == -1 and predicoes_originais[i - 2] == -1:
            predicoes_filtradas[i] = -1

    # --- Calculando as métricas e as exibindo ---
    acuracia = accuracy_score(valores_concatenados, predicoes_filtradas)
    precisao = precision_score(valores_concatenados, predicoes_filtradas, pos_label=-1)
    recall = recall_score(valores_concatenados, predicoes_filtradas, pos_label=-1)
    matriz_confusao = confusion_matrix(valores_concatenados, predicoes_filtradas, labels=[1, -1])

    print("------ RESULTADOS DO MODELO (CWRU) ------")
    print(f"Acurácia: {acuracia:.4f}")
    print(f"Precisão: {precisao:.4f}")
    print(f"Recall:    {recall:.4f}")
    print("\nMatriz de Confusão:")
    print(matriz_confusao)

    # --- Avaliando o desempenho do modelo quanto ao tempo ---
    # Para verificar se seria realmente bom para colocar no microcomputador
    janela_individual = valores_escalados[0:1]
    rodadas = 1000
    tempos = []

    # Primeira execução para evitar o atraso de inicialização nas medições
    modelo.predict(janela_individual)

    for _ in range(rodadas):
        inicio = time.perf_counter()
        modelo.predict(janela_individual)
        fim = time.perf_counter()
        tempos.append((fim - inicio) * 1000)

    tempo_medio = np.mean(tempos)
    desvio_padrao = np.std(tempos)

    print("\n-----\n")
    print(f"Número de execuções: {rodadas}")
    print(f"Tempo médio por janela: {tempo_medio:.4f} ms ± {desvio_padrao:.4f} ms")

    # --- Plotando o gráfico ---
    plotar_analise_rms(valores_caracteristicas, predicoes_filtradas, tamanho_da_janela, acuracia, precisao, recall)
    print("-> Imagem gerada!")