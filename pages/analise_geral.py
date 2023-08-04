import streamlit as st
from PIL import Image
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import locale


#/c/Users/vitor/anaconda3/python
# ------------------------------------------VARIÁVEIS------------------------------------------ #
cidades_vale = ['Alto Santo','Ererê', 'Iracema', 'Jaguaretama', 'Jaguaribara', 'Jaguaruana', 
                'Jaguaribe', 'Limoeiro do Norte', 'Morada Nova', 'Palhano', 'Pereiro', 'Potiretama', 
                'Quixeré', 'Russas', 'São João do Jaguaribe', 'Tabuleiro do Norte']

municipios = ["9","53","80","88","89","91","90","97","113","126","135","142","147","150","158","164"]


mapeamento_cidades = {
    9: "Alto Santo",
    53: "Ererê",
    80: "Iracema",
    88: "Jaguaretama",
    89: "Jaguaribara",
    91: "Jaguaruana",
    90: "Jaguaribe",
    97: "Limoeiro do Norte",
    113: "Morada Nova",
    126: "Palhano",
    135: "Pereiro",
    142: "Potiretama",
    147: "Quixeré",
    150: "Russas",
    158: "São João do Jaguaribe",
    164: "Tabuleiro do Norte"
}

despesas = ['Outros Serviços de Terceiros - Pessoa Jurídica', 'Material de Consumo',
                'Obras e Instalações', 'Material, Bem ou Serviço para Distribuição Gratuita',
                'Serviços de Tecnologia da Informação e Comunicação \x96 Pessoa Jurídica',
                'Serviços de Consultoria', 'Equipamentos e Material Permanente']
show_map = True


CAMINHO_ARQUIVO_TOTAL = 'dataframes\despesas-mpe.xlsx'
CAMINHO_ARQUIVO = 'dataframes\despesas_total.xlsx'

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# ------------------------------------------FUNÇÕES------------------------------------------ #

def limpeza_df_cnpj():
    CAMINHO_ARQUIVO = 'dataframes\despesas_total.xlsx'
    df = pd.read_excel(CAMINHO_ARQUIVO, dtype = {'CNPJ':str})
    # Filtrar apenas CNPJs
    df['CNPJ'] = df['CNPJ'].astype(str)

    df = df.drop('Lista de CNPJ', axis = 1)
    # Selecionar as despesas de interesse
    
    df = df[df['Título da Despesa'].isin(despesas)]

    # Selecionar o porte

    df = df.loc[df['Porte'] != 'DEMAIS']

    # Converta as chaves do dicionário para o tipo de dados da coluna 'Número do Município'
    df['Número do Município'] = df['Número do Município'].astype(int)

    # Substituir os números pelo nome dos municípios usando o mapeamento_cidades
    df['Número do Município'] = df['Número do Município'].map(mapeamento_cidades)

    # Renomear a coluna
    df = df.rename(columns={'Número do Município': 'Município', 
                            'Título da Despesa': 'Categoria da Despesa'})
    df['Valor'] = df['Valor'].apply(lambda x: locale.currency(x / 100, grouping=True, symbol=None))
    df['Valor'] = df['Valor'].apply(locale.atof)

    return df

def limpeza_df_mpe():
    df = pd.read_excel(CAMINHO_ARQUIVO_TOTAL)
    # Renomear coluna
    df = df.rename(columns={'Natureza da Despesa': 'Categoria da Despesa'})

    # Arredondar a porcentagem
    df['(%)MPE/TOTAL'] = df['(%)MPE/TOTAL'].round(2)

    # Remover a coluna "Unnamed: 0"
    df = df.drop(columns=['Unnamed: 0'], axis=1)
    df['Total das Compras (R$)'] = df['Total das Compras (R$)'].apply(lambda x: locale.currency(x, grouping=True, symbol=None))
    df['Total das Compras (R$)'] = df['Total das Compras (R$)'].apply(locale.atof)
    df['Valor MPE (R$)'] = df['Valor MPE (R$)'].apply(lambda x: locale.currency(x, grouping=True, symbol=None))
    df['Valor MPE (R$)'] = df['Valor MPE (R$)'].apply(locale.atof)

    return df

def visualizacao_df(df, name):
    # Filtro de Municípios
    if cidade_interesse:
        df = df[df['Município'].isin(cidade_interesse)]

    # Filtro de Despesas
    if despesas_interesse:
        df = df[df['Categoria da Despesa'].isin(despesas_interesse)]
    
    # Verifica se o DataFrame está vazio após aplicar os filtros
    if df.empty and name == 'CNPJ' and (cidade_interesse or despesas_interesse):
        # Escreve a mensagem de não correspondência no Streamlit
        st.warning(f"Não há correspondência da despesa {', '.join(despesas_interesse)} para o(s) município(s) {', '.join(cidade_interesse)}")
    else:
        # Verifica se há filtros de cidade e despesa aplicados
        if (cidade_interesse or despesas_interesse) and name == 'CNPJ':
            # Cria as duas colunas
            col1, col2 = st.columns(2)

            # Coluna 1 - DataFrame filtrado
            col1.dataframe(df)

            # Verifica se há filtros de cidade e despesa aplicados
            if cidade_interesse:
                cidades_filtradas = ', '.join(cidade_interesse)
                col2.markdown(f"<h3><b>Filtro de Cidade</b></h3>", unsafe_allow_html=True)
                col2.write(cidades_filtradas)

            if despesas_interesse:
                despesas_filtradas = ', '.join(despesas_interesse)
                col2.markdown(f"<h3><b>Filtro de Despesa</b></h3>", unsafe_allow_html=True)
                col2.write(despesas_filtradas)
        else:
            # Se não houver filtros aplicados ou o nome não for 'CNPJ', exibe o DataFrame inteiro sem utilizar colunas
            st.dataframe(df)
       
def analise1(df, cidade_interesse=None):
    if cidade_interesse:
        df = df[df['Município'].isin(cidade_interesse)]

    num_cidades = len(cidade_interesse) if cidade_interesse else 0
    font_size = get_font_size(num_cidades)

    analise1 = df.groupby('Município').sum().reset_index()[['Município', 'Total das Compras (R$)', 'Valor MPE (R$)']].sort_values('Total das Compras (R$)', ascending=False)

    pd.options.display.float_format = '{:.2f}'.format
    analise1['Porcentagem'] = (analise1['Valor MPE (R$)'] / analise1['Total das Compras (R$)']) * 100
    analise1['Porcentagem'] = analise1['Porcentagem'].round(2)  # Arredondamento para duas casas decimais
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6), dpi = 1000)
    # Criando o gráfico de barras
    ax = sns.barplot(x='Município', y='Total das Compras (R$)', data=analise1, label='Total das Compras (R$)',palette='Set2')
    ax = sns.barplot(x='Município', y='Valor MPE (R$)', data=analise1, label='Valor MPE (R$)', palette='Set2', hatch = '/ /')

    plt.xticks(rotation=0 if len(cidade_interesse) == 1 else (90 if len(cidade_interesse) > 7 else 45), fontsize=get_font_size(num_cidades), fontweight='bold')  # Adicionando fontweight='bold'
    plt.ylabel('R$', fontsize=get_font_size(num_cidades), fontweight='bold')
    plt.title('Total das Compras e Valor MPE por Município', fontsize=get_font_size(num_cidades)+4, fontweight='bold')
    # Define o formato dos números no eixo y como 'plain' (números reais)
    plt.ticklabel_format(style='plain', axis='y')
    plt.legend()

    # Retorna o gráfico em vez de exibi-lo com plt.show()
    return plt


def analise2(df, cidade_interesse=None, despesa_interesse=None):
    if cidade_interesse:
        df = df[df['Município'].isin(cidade_interesse)]

    if despesa_interesse:
        df = df[df['Categoria da Despesa'].isin(despesa_interesse)]

    num_cidades = len(cidade_interesse) if cidade_interesse else 0
    font_size = get_font_size(num_cidades)

    pd.options.display.float_format = '{:.2f}'.format
    analise2 = df.groupby(['Categoria da Despesa', 'Município']).sum().reset_index()
    analise2['Porcentagem'] = (analise2['Valor MPE (R$)'] / analise2['Total das Compras (R$)']) * 100
    analise2['Porcentagem'] = analise2['Porcentagem'].round(2)  # Arredondamento para duas casas decimais

    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 8), dpi=1000)  # Aumente a altura do gráfico para dar espaço à legenda abaixo

    # Criando o gráfico de barras
    ax = sns.barplot(x='Município', y='Total das Compras (R$)', hue='Categoria da Despesa', data=analise2, palette='Set2')
    ax = sns.barplot(x='Município', y='Valor MPE (R$)', hue='Categoria da Despesa', data=analise2, palette='Set2', hatch='//')

    plt.xticks(rotation= 0 if len(cidade_interesse) == 1 else 45, ha='right', fontsize=get_font_size(num_cidades), fontweight='bold')
    plt.ylabel('R$', fontsize=get_font_size(num_cidades), fontweight='bold')
    plt.xlabel(' ')
    plt.title('Total das Compras e Valor MPE por Município e Categoria de Despesa', fontsize=get_font_size(num_cidades) + 4, fontweight='bold')
    # Define o formato dos números no eixo y como 'plain' (números reais)
    plt.ticklabel_format(style='plain', axis='y')
    
    # Coloca a legenda abaixo do gráfico, fora da figura, sem sobrepor
    plt.legend(title='Legenda', bbox_to_anchor=(0.2, -0.10) if len(cidade_interesse) == 1 else (0.2, -0.30), loc='upper center')

    # Retorna o gráfico em vez de exibi-lo com plt.show()
    return plt

def analise3(cidade_interesse = None):
    df = limpeza_df_cnpj()
    if cidade_interesse:
        df = df[df['Município'].isin(cidade_interesse)]
    num_cidades = len(cidade_interesse) if cidade_interesse else 0
    font_size = get_font_size(num_cidades)
    valor_medio = df.groupby(['Município'])['Valor'].mean().reset_index().sort_values('Valor', ascending = False)
    # Configurações do gráfico
    plt.figure(figsize=(12, 6))  # Define o tamanho da figura
    sns.barplot(x='Município', y='Valor', data=valor_medio, palette='Set2')  # Cria o gráfico de barras
    plt.title('Valor Médio das despesas com MPEs por município', fontsize=get_font_size(num_cidades) + 4, fontweight='bold')  # Define o título do gráfico
    plt.xlabel(' ')
    plt.ylabel('Valor', fontsize=get_font_size(num_cidades), fontweight='bold')
    # Rotacionar rótulos do eixo x para melhor visualização
    plt.xticks(rotation= 0 if len(cidade_interesse) == 1 else 45, ha='right', fontsize=get_font_size(num_cidades), fontweight='bold')

    # Mostrar o gráfico
    plt.show()

def analise4(cidade_interesse=None, despesas_interesse=None):
    df = limpeza_df_cnpj()
    if cidade_interesse:
        df = df[df['Município'].isin(cidade_interesse)]
    if despesas_interesse:
        df = df[df['Categoria da Despesa'].isin(despesas_interesse)]
    num_cidades = len(cidade_interesse) if cidade_interesse else 0
    font_size = get_font_size(num_cidades)
    valor_medio_despesa = df.groupby(['Município', 'Categoria da Despesa']).mean().reset_index()
    plt.figure(figsize=(12, 6))  # Define o tamanho da figura
    sns.barplot(x='Município', y='Valor', hue = 'Categoria da Despesa', data=valor_medio_despesa, palette='Set2')  # Cria o gráfico de barras
    plt.title('Valor Médio das despesas com MPEs por município', fontsize=get_font_size(num_cidades) + 4, fontweight='bold')  # Define o título do gráfico
    plt.xlabel(' ')
    plt.ylabel('Valor', fontsize=get_font_size(num_cidades), fontweight='bold')
    # Rotacionar rótulos do eixo x para melhor visualização
    plt.xticks(rotation= 0 if len(cidade_interesse) == 1 else 45, ha='right', fontsize=get_font_size(num_cidades), fontweight='bold')
    plt.legend(title='Legenda', bbox_to_anchor=(0.2, -0.10) if len(cidade_interesse) == 1 else (0.2, -0.35), loc='upper center')
    plt.ticklabel_format(style='plain', axis='y')
    # Mostrar o gráfico
    plt.show()
def get_font_size(num_cidades):
    # Tamanho base da fonte
    base_font_size = 16

    # Número máximo de cidades para ajustar o tamanho da fonte
    max_cidades = 10

    # Cálculo do tamanho da fonte proporcional ao número de cidades selecionadas
    font_size = max(base_font_size - num_cidades, 8)  # O tamanho mínimo da fonte será 8

    return font_size

def download(df, cidade_interesse, despesas_interesse):
    # Aplica os filtros no DataFrame
    if cidade_interesse:
        df = df[df['Município'].isin(cidade_interesse)]

    if despesas_interesse:
        df = df[df['Categoria da Despesa'].isin(despesas_interesse)]

    # Realiza o download da planilha
    csv = df.to_csv().encode('utf-8')
    st.download_button(
        label="Faço o download da planilha em formato .csv",
        data=csv,
        file_name='planilha_total.csv',
        mime='text/csv',
    )
    st.write('Se você realizou  seleções com os filtros, a planilha baixada terá também os filtros aplicados.')


# ------------------------------------------STREAMLIT - BARRA LATERAL------------------------------------------ #

st.set_option('deprecation.showPyplotGlobalUse', False)
# ------------------------------------------STREAMLIT - BARRA LATERAL------------------------------------------ #

## Filtro Cidade
st.sidebar.markdown('## Selecione o(s) município(s) de interesse')
cidade_interesse = st.sidebar.multiselect(
'Filtro de municípios',
cidades_vale,
default = None
)

## Filtro Despesas
st.sidebar.markdown('## Selecione a(s) despesa(s) de interesse')
despesas_interesse = st.sidebar.multiselect(
'Filtro de despesa',
despesas,
default = None
)

image = Image.open('logo.png')

st.sidebar.image(image, width=120)

# ------------------------------------------STREAMLIT - LAYOUT PRINCIPAL------------------------------------------ #

def main():
    # Carrega o DataFrame após a limpeza e filtragem dos dados
    df_cnpjs = limpeza_df_cnpj()
    df_despesa_mpe = limpeza_df_mpe()

    # Descrição da Planilha
    st.markdown('#### Essa planilha registra todas as transações com MPEs nos municípios e despesas selecionadas')
    
    # Visualização do df de CNPJs
    visualizacao_df(df_cnpjs, 'CNPJ')
    download(df_cnpjs, cidade_interesse, despesas_interesse)
    #Descrição de Planilha
    st.markdown('#### Essa planilha registra a soma total por despesa em cada município selecionado, a soma de despesas com MPEs no mesmo município e a porcentagem desta soma em relação ao total. ')
    # Visualização do df de MPEs
    visualizacao_df(df_despesa_mpe, 'MPE')
    download(df_despesa_mpe, cidade_interesse, despesas_interesse)
    #Início dos gráficos
    st.markdown(f"<h2><b>Análises Gerais</b></h2>", unsafe_allow_html=True)
    st.markdown(f"<h3><b>1) Participação das MPEs nas compras públicas por município, sem considerar as despesas individualmente.</b></h3>", unsafe_allow_html=True)
    st.pyplot(analise1(df_despesa_mpe, cidade_interesse))
    plt.close()
    st.markdown(f' ##### No gráfico acima, temos como barra cheia o total de compras do município no ano de 2022. Como barra hachurada, temos a quantidade de compras do município destinadas à MPEs, em comparação com o total.')
    st.markdown(f"<h3><b>2) Participação das MPEs nas compras públicas por município e por categoria de desepsa.</b></h3>", unsafe_allow_html=True)
    st.write('Observação: para melhor visualização deste gráfico, é recomendado que sejam selecionadas até 4 municípios por vez, caso todas as despesas estejam também seleciondas. As marcas hachuradas representam o valor total das transações realizadas com as MPEs.')
    st.pyplot(analise2(df_despesa_mpe, cidade_interesse, despesas_interesse))
    st.markdown(f' ##### No gráfico acima, temos como barra cheia o total de compras do município no ano de 2022, separado por categoria. Como barra hachurada, temos a quantidade de compras do município destinadas à MPEs, em comparação com o total, também separada por categoria de despesa.')
    st.markdown(f"<h3><b>3) Valor médio das transações com as MPEs por município.</b></h3>", unsafe_allow_html=True)
    st.pyplot(analise3(cidade_interesse))
    st.markdown(f' ##### No gráfico acima, temos o valor médio das transações com MPEs feitas nos municípios no ano de 2022.')
    st.markdown(f"<h3><b>4) Valor médio das transações com as MPEs por município e categoria de despesa.</b></h3>", unsafe_allow_html=True)
    st.write('Observação: para melhor visualização deste gráfico, é recomendado que sejam selecionadas até 4 municípios por vez, caso todas as despesas estejam também seleciondas.')   
    st.pyplot(analise4(cidade_interesse, despesas_interesse))
    st.markdown(f' ##### No gráfico acima, temos o valor médio das transações com MPEs feitas nos municípios no ano de 2022, por categoria de despesa.')
if __name__ == '__main__':
    main()




