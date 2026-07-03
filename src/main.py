import time
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
from processamento import carregar_sinal_cwru, extrair_caracteristicas
from visualizacao import plotar_analise_rms

if __name__ == "__main__":
    # Carregando os arquivos
    sinal_normal = carregar_sinal_cwru("../data/97.mat")
    sinal_falha = carregar_sinal_cwru("../data/105.mat")

    # Definindo o tamanho da janela que será observada
    tamanho_da_janela = 1024

    # Extraindo as características de cada arquivo
    caracteristicas_normal = extrair_caracteristicas(sinal_normal, tamanho_janela = tamanho_da_janela)
    caracteristicas_falha = extrair_caracteristicas(sinal_falha, tamanho_janela = tamanho_da_janela)

    # Unindo ambos os sinais para o momento de teste/predição
    caracteristicas_unidas = np.concatenate([caracteristicas_normal, caracteristicas_falha])

    # Inicialização do scaler (uma régua) para treinamento
    scaler = StandardScaler()

    # Treinando a régua com o funcionamento normal da máquina
    scaler.fit(caracteristicas_normal)

    # Transformação das características da zona saudável para uma escala
    # Nessa escala, tem-se:
        # média:     0
        # variância: 1
    escala_normalizada = scaler.transform(caracteristicas_normal)

    # Aplica o que aprendeu da escala a todos os dados
    # Como a régua não conhece os dados de falha, esses terão os seus valores
    # muito alto e, portanto, serão facilmente isolados
    valores_escalados = scaler.transform(caracteristicas_unidas)

    # Criando um gabarito para conseguir testar o desempenho do modelo
    #    1: estado normal,
    #   -1: estado de falha
    gabarito = np.concatenate([
        np.ones( len(caracteristicas_normal) ),
        -np.ones( len(caracteristicas_falha) )
    ])

    # --- Treinando o modelo preditivo
    modelo = IsolationForest(contamination = "auto", random_state = 32)
    # O modelo aprende como é o comportamento saudável da máquina
    modelo.fit(escala_normalizada)
    # Modelo testa com todos os dados. Os que ele não reconhecer, maca como -1
    predicoes_originais = modelo.predict(valores_escalados)

    # Cópia da lista de predições para realizar um filtro
    predicoes_filtradas = np.ones(len(predicoes_originais))

    # --- Filtro para verificar as reais anomalias ---
    for i in range (2, len(predicoes_originais)):
        # Para considerar um evento de fato anômalo, precisa que os dois eventos
        # anteriores também sejam anômalos
        if predicoes_originais[i] == -1 and predicoes_originais[i - 1] == -1 and predicoes_originais[i - 2] == -1:
            predicoes_filtradas[i] = -1

    # --- Calculando as métricas ---
    acuracia = accuracy_score(gabarito, predicoes_filtradas)
    precisao = precision_score(gabarito, predicoes_filtradas, pos_label = -1)
    recall = recall_score(gabarito, predicoes_filtradas, pos_label = -1)
    matriz_confusao = confusion_matrix(gabarito, predicoes_filtradas, labels = [1, -1])

    # Exibindo, no terminal, os resultados
    print("-=-=-=-=-=-[ Resultados do modelo (CWRU) ]-=-=-=-=-=-\n")
    print(f"Acurácia: {acuracia:.4f}")
    print(f"Precisão: {precisao:.4f}")
    print(f"Recall: {recall:.4f}")
    print("\nMatriz de confusão:")
    print(matriz_confusao)

    # --- Avaliando o desempenho do modelo quanto ao tempo ---
    janela_individual = valores_escalados[0:1]
    rodadas = 1000
    tempos = []

    # Primeira execução para evitar o atraso de inicialização nas mediçoes
    modelo.predict(janela_individual)

    for _ in range(rodadas):

        # Começa a contar o tempo, para verificar a perfomance
        inicio = time.perf_counter()

        # O modelo realiza uma predição na janela individual
        modelo.predict(janela_individual)

        # Finaliza a contagem do tempo
        fim = time.perf_counter()

        # Adiciona na lista 'tempo' o intervalo calculado
        tempos.append((fim - inicio) * 1000)

    # Calculando o tempo médio obtido no vetor 'tempo'
    tempo_medio = np.mean(tempos)

    # Calculando o desvio padrão
    desvio_padrao = np.std(tempos)

    # Exibindo, no terminal, quantas execuções foram feitas
    print(f"Vezes executadas: {rodadas}")
    print(f"Tempo médio por janela: {tempo_medio: .4f} ms ± {desvio_padrao:.4f} ms")
    
    # --- Plotando o gráfico
    plotar_analise_rms(caracteristicas_unidas, predicoes_filtradas, tamanho_da_janela, acuracia, precisao, recall)
    print(" *--> Gráfico gerado!")

