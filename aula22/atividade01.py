import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


subprocess.run('cls', shell=True)
# Obtendo os dados
try:
    print('Obtendo dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

    df_cvli = df_ocorrencias[['aisp', 'cvli']]
    
    df_cvli = df_cvli.groupby('aisp', as_index=False)['cvli'].sum()

    # Total
    total_cvli = df_cvli['cvli'].sum()

    # Percentual
    df_cvli['percentual %'] = round(
        ((df_cvli['cvli'] / total_cvli) * 100), 2
    )
    
    print(f'''
-------------------------------------------
Crimes Violentos Letais Intencionais (CVLI)
-------------------------------------------
{df_cvli}
''')

except Exception as e:
    print(f'Erro ao obter os dados - {e}')


# Obtendo medidas
try:
    array_cvli = np.array(df_cvli['cvli'])
    
    # Medida de tendência central
    media_cvli = np.mean(array_cvli)
    mediana_cvli = np.median(array_cvli)

    # Medidas de Posição
    maximo = np.max(array_cvli)
    minimo = np.min(array_cvli)
    
    q1 = np.quantile(array_cvli, .25) 
    q2 = np.quantile(array_cvli, .50)
    q3 = np.quantile(array_cvli, .75)

    # Medidas de Dispersão
    amplitude = maximo - minimo
    
    distancia_media_mediana = abs(
        (media_cvli - mediana_cvli) / mediana_cvli * 100
    )
    
    variancia = np.var(array_cvli)
    distancia_var_media = variancia / (media_cvli ** 2) * 100
    desvio_padrao = np.std(array_cvli)
    coef_variacao = (desvio_padrao / media_cvli) * 100

    # Verificando a Assimetria e Curtose da Distribuição
    assimetria = df_cvli['cvli'].skew()
    curtose = df_cvli['cvli'].kurtosis()

except Exception as e:
    print(f'Erro ao obter Medidas - {e}')
    print(f'Linha: {e.__traceback__.tb_lineno}')



# Maiores e menores ocorrencias
try:
    
    df_cvli_menores = df_cvli[
        df_cvli['cvli'] < q1
    ]

    df_cvli_maiores = df_cvli[
        df_cvli['cvli'] > q3
    ]

    print(f'''\n
-----------------------------------------
Batalhoes com Menos Ocorrencias de "CVLI"
-----------------------------------------
{df_cvli_menores.sort_values(by='cvli', ascending=True)}

-----------------------------------------
Batalhoes com Mais Ocorrencias de "CVLI"
-----------------------------------------
{df_cvli_maiores.sort_values(by='cvli', ascending=False)}
''')

except Exception as e:
    print(f'Erro ao Analizar a distribuição - {e}')


# calculando os outliers
try:
    iqr = q3 - q1 

    limite_superior = q3 + (1.5 * iqr)
    limite_inferior = q1 - (1.5 * iqr)

    # Menores
    df_cvli_outliers_menores = (
        df_cvli[df_cvli['cvli'] < limite_inferior]
    )
    # Maiores
    df_cvli_outliers_maiores = (
        df_cvli[df_cvli['cvli'] > limite_superior]
    )

    print(f'''
-----------------------------
CVLI" com outliers inferiores
-----------------------------
    ''')

    if len(df_cvli_outliers_menores) == 0:
        print('Não há outliers Inferiores')
    else:
        print(df_cvli_outliers_menores)


    print(f'''
-----------------------------
CVLI" com outliers superiores
-----------------------------
    ''')

    if len(df_cvli_outliers_maiores) == 0:
        print('Não há outliers maiores')
    else:
        print(df_cvli_outliers_maiores)

except Exception as e:
    print(f'Erro ao calcular os outliers - {e}')

# Mostrando Todas a Medidas
try:
    print(f'''
------------------
Monstrando Medidas
------------------

Minimo: {minimo}')
Limite Inferior: {limite_inferior}
Q1: {q1}')
Q2: {q2}')
Q3: {q3}')
Limite Superior: {limite_superior}
Maximo: {maximo}
Total de CVLI: {total_cvli}

Média: {media_cvli:.2f}
Mediana: {mediana_cvli}
Distancia Entre Média e Mediana: {distancia_media_mediana:.2f}%
IQR: {iqr}')
Amplitude: {amplitude}
Variância: {variancia:.2f}
Distancia Variancia Média: {distancia_var_media:.2f}%
Disvio Padrão: {desvio_padrao:.2f}
Coeficiente de Variação: {coef_variacao:.2f}%

Assimetria: {assimetria:.2f}
Curtose: {curtose:.2f}
''')


    print(f'''
----------------------------
Análise de CVLI por Batalhão
----------------------------
-   Os batalhões não apresentam um padrão médio de CVLI, Os dados são muito heterogêneos.

-   O coeficiente de variação é de {coef_variacao:.2f}%, muito acima de 25%,
que é o limite comum para considerar um Tendencia de Alta disperção em um conjunto de dados.

-   O desvio padrão de {desvio_padrao:.2f} é quase do tamanho da própria média {media_cvli:.2f}.

-   A média de {media_cvli:.2f} fica {distancia_media_mediana:.2f}% acima da mediana que é de {mediana_cvli}, 
o que indica poucos batalhões com valores altos puxam a média para cima.

-   A amplitude é enorme: de {minimo} a {maximo}, ou seja, {amplitude} ocorrências de diferença.

-   Os quartis mostram a dispersão: 25% dos batalhões têm até {q1} ocorrências, e os 25% maiores tem de {q3} até {maximo}.

-   A média está acima da mediana indicando assimetria à direita: poucos batalhões com valores altos
puxam a média para cima.

-   Há batalhões com ocorrências muito superiores aos demais pelo critério do IQR, com limite superior há {limite_superior}:

{df_cvli_outliers_maiores}

-   Não há outliers inferiores: o limite inferior de {limite_inferior} é negativo, e está abaixo do Minimo que é de {minimo}.
''')

except Exception as e:
    print(f'Erro ao mostrar medidas - {e}')

# Gráfico
try:
    plt.figure(figsize=(16, 9))
    plt.suptitle('Imformações Sobre: Crimes Violentos Letais Intencionais (CVLI)', fontsize=14)

    # 1ª posição - Distribuição
    plt.subplot(2, 2, 1)
    plt.boxplot(df_cvli['cvli'], orientation='horizontal', showmeans=True) 
    plt.title('Distribuição das ocorrências por Batalhões')
    plt.xlabel('Nº de Casos de CVLI')
    plt.ylabel('Distribuição')


    # 2ª posição - As Medidas
    plt.subplot(2, 2, 2)
    plt.title('Medidas estatísticas')

    plt.text(0.1, 0.95, f'Limite inferior: {limite_inferior}', fontsize=12)
    plt.text(0.1, 0.90, f'Minimo: {minimo}', fontsize=12)
    plt.text(0.1, 0.85, f'Q1: {q1}', fontsize=12)
    plt.text(0.1, 0.80, f'Q2: {q2}', fontsize=12)
    plt.text(0.1, 0.75, f'Q3: {q3}', fontsize=12)
    plt.text(0.1, 0.70, f'Limite Superior: {limite_superior}', fontsize=12)
    plt.text(0.1, 0.65, f'Máximo: {maximo}', fontsize=12)
    
    plt.text(0.1, 0.55, f'Mediana: {mediana_cvli}', fontsize=12)
    plt.text(0.1, 0.50, f'Média: {media_cvli:.2f}', fontsize=12)
    plt.text(0.1, 0.45, f'IQR - Intervalo Interquartil: {iqr}', fontsize=12)
    plt.text(0.1, 0.40, f'Amplitude Total: {amplitude}', fontsize=12)
    plt.text(0.1, 0.35, f'Distância: {distancia_media_mediana:.2f}', fontsize=12)

    plt.text(0.1, 0.25, f'Distancia Variancia Média: {distancia_var_media:.2f}', fontsize=12)
    plt.text(0.1, 0.20, f'Disvio Padrão: {desvio_padrao:.2f}', fontsize=12)
    plt.text(0.1, 0.15, f'Coeficiente de Variação: {coef_variacao:.2f}', fontsize=12)
    plt.axis('off')


    # 3ª posição - Os maiores
    plt.subplot(2, 2, 3)
    plt.title('TOP 10 - Ocorrencias por Batalhões')
    df_cvli_10maiores = (
        df_cvli_maiores
        .head(10)
        .sort_values(by='cvli')
         
    )
    plt.bar(df_cvli_10maiores['aisp'].astype(str), df_cvli_10maiores['cvli'])
    plt.xlabel('Nº de batalhões')
    plt.ylabel('Nº de Casos de CVLI')


    # 4ª Histograma
    plt.subplot(2, 2, 4)
    plt.title('')
    plt.hist(array_cvli, bins=100, edgecolor='black')
    plt.axvline(media_cvli, color='green', linewidth=1) # Média
    plt.axvline(mediana_cvli, color='orange', linewidth=1) # Mediana
    plt.xlabel('Limites')
    plt.ylabel('Contagens')
    
    plt.show()

    contagens, limites = np.histogram(array_cvli, bins=100)

    print(f'\nFixas de CVLI do Histograma')
    for i in range(len(contagens)):
        if contagens[i] > 0:
            print(
                f'Faixa {i+1}: '
                f'{limites [i]:.0f} até {limites[i+1]:.0f} CVLIs:  '
                f'=> {contagens[i]} batalhões'
            )

except Exception as e:
    print(f'Erro ao gerar o painel - {e}')