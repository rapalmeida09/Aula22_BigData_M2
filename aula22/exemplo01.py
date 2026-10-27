# pip install pandas numpy matplotlib
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


subprocess.run('cls', shell=True)
# Obtendo os dados
try:
    print('Obtendo dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'
    
    # utf-8, iso-8859-1, latin1, cp1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    #print(df_ocorrencias)

    #Filtro
    df_ocorrencias = df_ocorrencias[df_ocorrencias['regiao'] == 'Interior']

    # Delimitando dados
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]
    #print(df_roubo_veiculo.head(30))
    #print(df_roubo_veiculo.tail(30))


    # ### PREPARANDO OS DADOS
    # Totalizando os roubos por cidade (Var Qualitativa 'munic' e Var Quantitativa 'roubo_veiculo')
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()
    #print(df_roubo_veiculo.head(30))

    # Obtendo Toral e o percentual de roubos por municípios
    # Total
    total_roubos = df_roubo_veiculo['roubo_veiculo'].sum()

    # Percentual
    df_roubo_veiculo['percentual %'] = round(
        ((df_roubo_veiculo['roubo_veiculo'] / total_roubos) * 100), 2
    )


    # Ordenando os dados
    df_roubo_veiculo = df_roubo_veiculo.sort_values(
        by='roubo_veiculo',
        ascending=False
    )
    print(df_roubo_veiculo.head(10))
    #print(df_roubo_veiculo.tail(10))

except Exception as e:
    print(f'Erro ao obter os dados - {e}')


try:
    print(f'\nObtendo informações a cerca dos roubos dos veículos... ')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    # distancia da média para a mediana
    distancia = abs(
        (media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo * 100
    )

    print('\nMedias de tendência Central')
    print(f'Média: {media_roubo_veiculo:.2f}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distancia Entre Média e Mediana: {distancia:.2f}%')

except Exception as e:
    print(f'Obtendo Medidas - {e}')


try:
    q1 = np.quantile(array_roubo_veiculo, .25  ) # method='weibull'
    q2 = np.quantile(array_roubo_veiculo, .50)
    q3 = np.quantile(array_roubo_veiculo, .75)

    print('\nMedidas de Posição')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')

    # Cidades c/ Menos ocorrencias de roubos
    df_roubo_veiculo_menores = df_roubo_veiculo[
        df_roubo_veiculo['roubo_veiculo'] < q1
    ]

    # Cidades c/ Maiores ocorrencias de roubos
    df_roubo_veiculo_maiores = df_roubo_veiculo[
        df_roubo_veiculo['roubo_veiculo'] > q3
    ]

    # Exportar para CSV
    print('\nMunicipios com menores roubos ')
    print(30*'-')
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))
    df_roubo_veiculo_menores.to_csv('menores.csv', index=False, sep=';', encoding='iso-8859-1')

    print('\nMunicipios com Maiores roubos ')
    print(30*'-')
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))
    df_roubo_veiculo_maiores.to_csv('maiores.csv', index=False, sep=';', encoding='iso-8859-1')

except Exception as e:
    print(f'Erro ao Analizar a distribuição - {e}')


# Medidas de posição e Dispersão
try:
    print('\nCalculando a Amplitude Total')
    # amplitude_total = maior - menor
    # Quanto mais proximo do zero, mais homogênios são  os dados do conjunto.
    # Quanto mais proximo do maior valor, mais heterôgenio são  os dados do conjunto.
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo

except Exception as e:
    print(f'Erro ao calcular a amplitude - {e}')


# Medidas de Disperção
try:
    # Variancia
    # É uma medida para observar a disperção dos dados
    # Observa-se em relação a média
    # É a média dos quadrados das diferenças entre cada valor e a média
    # OBS: O resultado da variância está elevado ao quadrado
    variancia = np.var(array_roubo_veiculo)

    # Distancia variancia media
    # < 10% - Baixa Disperção
    # Entre 10% e 25% - Tendencia de moderada disperção
    # > 25% Alta disperção
    distancia_var_media = variancia / (media_roubo_veiculo ** 2) * 100

    # Desvio Padrão
    # É a raiz quadrada da Variancia. Observa-se em relação a média.
    # É a nomalização da variância.
    # Quanto os dados se afastam da Média.
    desvio_padrao = np.std(array_roubo_veiculo)

    # Coeficiente de Variação
    # É a magnitude do desvio padrão e relação a média
    coef_variacao = (desvio_padrao / media_roubo_veiculo) * 100

except Exception as e:
    print(f'Erro ao calcular a variabilidade do conjunto - {e}')


# Verificando a Assimetria da Distribuição
# Indica como os dados estão distribuidos. Para que lado tende a distribuição.
try:

    # Assimetria > 1
    # Positiva Alta
    # Cauda longa à direita
    # Existem valores altos puxando a média para cima
    # A média tende a ser maior que a mediana

    # Assimetria 0.5 e 1
    # Assimetria Positiva Moderada
    # Cauda existe, mas é menos acentuada
    # A média tende a ser maior que a mediana

    # Assimetria -0.5 e 0.5
    # Tendencia a uma Simetria
    # Os dados tende a estar equilibrados em torno do centro
    # A média e a Mediana tende a ter valores aproximados

    # Assimetria -1 e -0.5
    # Assimetria Negativa Moderada
    # Cauda existe, mas é menos acentuada
    # A média tende a ser menor que a mediana

    # Assimetria < 1
    # Assimetria Negativa Alta
    # Cauda longa à esquerda
    # Existem valores baixos puxando a média para baixo
    # A média tende a ser menor que a mediana

    assimetria = df_roubo_veiculo['roubo_veiculo'].skew()


    # Curtose
    # É uma medida que verifica o peso das caudas de uma distribuição
    # Indicando valores a importância dos valores extremos.
    # Quanto maior a curtose, Maior rende a ser a influencia dos extremos

    # Referência: Excesso de Curtose de Fisher

    # -0.5 a 0.5 (Aproximadamente Mesocúrtica)
    # Curtose próxima de uma distribuição normal
    # Outliers não são comuns, mas pode ocorrer.

    # Curtose > 0.5 (Leptocúrtica)
    # Caudas bem mais longas e pesadas e maior influência dos extremos.
    # Poucos valores muito extremos elevando bastante a curtose.
    # Pode apresentar picos muito alto
    # Outliers são mais frequentes
    
    # Curtose < -0.5 (Platicúrtica)
    # Caudas mais leves. Menor Influência dos extremos
    # Tende a Distribuição mais Achatada
    # Outliers podem aparecer

    curtose = df_roubo_veiculo['roubo_veiculo'].kurtosis()


    
    print('\nAnalizando a Distribuição')
    print(30*'-')
    print(f'Assimetria: {assimetria:.2f}')
    print(f'Curtose: {curtose:.2f}')

except Exception as e:
    print(f'Erro ao  calcular a simetria e Curtose dos dados - {e}')


# Achando os outliers
try:
    # Intervalo Interquartil (IQR)
    # É a amplitude dos dados mais centrais.
    # Quanto mais proximo do zero, mais homogênios são  os dados centrais.
    # Quanto mais proximo do q3, mais heterôgenio são  os dados dos 50% mais centrais.
    iqr = q3 - q1 
    # Ignora o maior e o menor valor.
    # Não sofre interferencia dos extremos.
    
    # print(iqr) # 970.75

    # Calcular os limites
    # Superior 
    limite_superior = q3 + (1.5 * iqr)
    print(f'\nLimite superior: {limite_superior}')

    # Inforior
    limite_inferior = q1 - (1.5 * iqr)
    print(f'\nLimite inferior: {limite_inferior}')

    # Filtrando outliers menores
    df_roubo_veiculo_outliers_menores = (
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]
    )

    print('\nMunicipios com outliers inferiores')
    print(30*'-')
    if len(df_roubo_veiculo_outliers_menores) == 0:
        print('Não há outliers Inferiores')
    else:
        print(df_roubo_veiculo_outliers_menores)

    # Filtrando outliers maiores
    df_roubo_veiculo_outliers_maiores = (
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    )

    print('\nMunicipios com outliers superiores')
    print(30*'-')
    if len(df_roubo_veiculo_outliers_maiores) == 0:
        print('Não há outliers maiores')
    else:
        print(df_roubo_veiculo_outliers_maiores)

except Exception as e:
    print(f'Erro ao calcular os outliers - {e}')

try:
    print('\nMonstrando Medidas')
    print(30*'-')
    print(f'Minimo: {minimo}')
    print(f'Limite Inferior: {limite_inferior}')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')
    print(f'Limite Superior: {limite_superior}')
    print(f'Maximo: {maximo}')
    print(f'Total de Roubos: {total_roubos}')

    print(f'\nMédia: {media_roubo_veiculo:.2f}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distancia Entre Média e Mediana: {distancia:.2f}%')
    print(f'IQR: {iqr}')
    print(f'Amplitude: {amplitude}')
    print(f'Variância: {variancia:.2f}')
    print(f'Distancia Variancia Média: {distancia_var_media:.2f}%')
    print(f'Disvio Padrão: {desvio_padrao:.2f}')
    print(f'Coeficiente de Variação: {coef_variacao:.2f}%')
    
except Exception as e:
    print(f'Erro ao mostrar medidas - {e}')

# # Plotando Gráfico
# try:
#     print('\nPlotando BoxPlot')
#     # pip install matplotlib
#     # import matplotlib.pyplot as plt

#     # BoxPlot
#     # showfliers=False - retirar os outliers
#     plt.boxplot(df_roubo_veiculo['roubo_veiculo'], orientation='horizontal', showmeans=True) 
#     plt.show()
    

# except Exception as e:
#     print(f'Erro ao plotar o gráfico - {e}')
    

try:
    print('\nInformações de Roubos de Veiculos')
    plt.figure(figsize={16, 10})

    # Posição 01 - boxplot
    plt.subplot(2, 2, 1)

    # showmeans=True - mostra a media 
    # showfliers=False - esconde os outliers
    plt.boxplot(df_roubo_veiculo['roubo_veiculo'], orientation='horizontal', showmeans=True) 
    plt.title('Distribuição dos Dados')
    plt.xlabel('Roubo de Veiculos')
    # plt.ylabel('Municípios')

    plt.subplot(2, 2, 2)

    plt.text(0.1, 0.95, f'Limite inferior: {limite_inferior}', fontsize=12)
    plt.text(0.1, 0.90, f'Minimo: {minimo}', fontsize=12)
    plt.text(0.1, 0.85, f'Q1: {q1}', fontsize=12)
    plt.text(0.1, 0.80, f'Q2: {q2}', fontsize=12)
    plt.text(0.1, 0.75, f'Q3: {q3}', fontsize=12)
    plt.text(0.1, 0.70, f'Limite Superior: {limite_superior}', fontsize=12)
    plt.text(0.1, 0.65, f'Máximo: {maximo}', fontsize=12)

    plt.text(0.1, 0.55, f'Mediana: {mediana_roubo_veiculo}', fontsize=12)
    plt.text(0.1, 0.50, f'Média: {media_roubo_veiculo}', fontsize=12)
    plt.text(0.1, 0.45, f'IQR - Intervalo Interquartil: {iqr}', fontsize=12)
    plt.text(0.1, 0.40, f'Amplitude Total: {amplitude}', fontsize=12)
    plt.text(0.1, 0.35, f'Distância: {distancia}', fontsize=12)
    plt.axis('off')

    # 3ª Histograma | Roubos por municipios
    plt.subplot(2, 2, 3)
    # histograma
    plt.hist(array_roubo_veiculo, bins=100, edgecolor='black')
    plt.axvline(media_roubo_veiculo, color='green', linewidth=1) # Média
    plt.axvline(mediana_roubo_veiculo, color='orange', linewidth=1) # Mediana

    contagens, limites = np.histogram(array_roubo_veiculo, bins=100)

    print(f'\nFixas de Roubos do Histograma')
    for i in range(len(contagens)):
        # Não Printa as contagens de 0 municipios
        if contagens[i] > 0:
            print(
                f'Faixa {i+1}: '
                f'{limites [i]:.0f} até {limites[i+1]:.0f} Roubos:  '
                f'=> {contagens[i]} Municipios'
            )







    # 4ª posição Colunas | Top 10 maiores
    plt.subplot(2,2,4)

    # Filtrando e Ordenando
    df_roubo_veiculo_10maiores = (
        df_roubo_veiculo_maiores
        .head(10)
        .sort_values(by='roubo_veiculo', ascending=True)
    )

    plt.bar(df_roubo_veiculo_10maiores['munic'], df_roubo_veiculo_10maiores['roubo_veiculo'])
    plt.xticks(rotation=45, ha='right') # Rotacona
    plt.xlabel('Municípios')
    plt.ylabel('Roubos de Veículos')


    plt.suptitle('Imformações Sobre Roubo de Veiculos')
    plt.show()
    
except Exception as e:
    print(f'Erro ao plotar o gráfico - {e}')
