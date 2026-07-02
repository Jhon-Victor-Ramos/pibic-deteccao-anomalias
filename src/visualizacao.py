import numpy as np
import matplotlib.pyplot as plt

# Configuração para integração do LaTeX na plotagem de gráfico
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif"
})

def plotar_analise_rms(valores_rms, predicoes, tamanho_janela, acuracia, precisao, recall):
    """
    Plota o sinal do RMS em função do tempo e aponta os dados anômalos
    encontrados e marca-os com um 'X' vermelho
    """

    # Define o tamanho da imagem
    plt.figure( figsize = (10, 5) )

    # Desenha a linha que representa o dado
    plt.plot(valores_rms[:, 0], label = "Sinal RMS", color = "blue")

    # Identifica os índices e os valores correspondentes de RMS das anomalias preditas
    indice_anomalia = np.arange( len(valores_rms) )[predicoes == -1, 0]

    # Faz ...
    rms_anomalias = valores_rms[predicoes == -1, 0]

    # Faz as marcações dos dados anômalos
    plt.scatter(indice_anomalia, rms_anomalias, marker = "X", color = "red", label = "Anomalia encontrada")

    # --- Estilização do gráfico ---
    # Define o título do gráfico, dando suporte ao uso do LaTeX
    plt.title(rf'Detecção de anomalias no sinal de vibração (CWRU) — Janela: {tamanho_janela}')

    # Define o texto para cada eixo (X e Y) do gráfico, indicando o que cada um representa
    plt.xlabel(r'Tempo ($t$)')
    plt.ylabel(r'RMS ($g$)')

    # Cria uma caixa de texto que serve para melhor entendimento (em valores) do gráfico
    texto_resultados = (f"Acurácia: {acuracia: .2%}\n"
                        f"Precisão: {precisao: .2%}\n"
                        f"Recall: {recall: .2%}\n"
                        f"Anomalias: {len(rms_anomalias): .2%}\n")

    # Insere a caixa de texto na diagonal inferior direita do gráfico
    plt.text(0.947, 0.05, texto_resultados, transform = plt.gcal().transAxes,
             fontsize=12, verticalalignment = 'bottom', horizontalalignment = 'right',
             bbox=dict(boxstyle='round', facecolor='white', alpha = 0.8))

    # Salva a imagem
    plt.savefig("grafico_final_pibic.png", dpi=300, bbox_inches='tight')

    plt.legend()
    plt.grid(True)
    plt.show()

    print(f" *-> {len(rms_anomalias)} foram encontradas!")




