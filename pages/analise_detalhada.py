import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from unidecode import unidecode
import locale
import streamlit as st
from PIL import Image

#/c/Users/vitor/anaconda3/python
# ------------------------------------------VARIÁVEIS------------------------------------------ #
cidades_vale = ['Alto Santo', 'Erere', 'Iracema', 'Jaguaretama', 'Jaguaribara', 'Jaguaruana', 'Jaguaribe', 'Limoeiro Do Norte', 
                'Morada Nova', 'Palhano', 'Pereiro', 'Potiretama', 'Quixere', 'Russas', 'Sao Joao Do Jaguaribe', 'Tabuleiro Do Norte']

municipios = ["9","53","80","88","89","91","90","97","113","126","135","142","147","150","158","164"]


mapeamento_cidades = {
    9: "Alto Santo",
    53: "Erere",
    80: "Iracema",
    88: "Jaguaretama",
    89: "Jaguaribara",
    91: "Jaguaruana",
    90: "Jaguaribe",
    97: "Limoeiro Do Norte",
    113: "Morada Nova",
    126: "Palhano",
    135: "Pereiro",
    142: "Potiretama",
    147: "Quixere",
    150: "Russas",
    158: "Sao Joao Do Jaguaribe",
    164: "Tabuleiro Do Norte"
}

despesas = ['Outros Serviços de Terceiros - Pessoa Jurídica', 'Material de Consumo',
                'Obras e Instalações', 'Material, Bem ou Serviço para Distribuição Gratuita',
                'Serviços de Tecnologia da Informação e Comunicação \x96 Pessoa Jurídica',
                'Serviços de Consultoria', 'Equipamentos e Material Permanente']

# Lista de Cidades do Ceará

cidades_ceara = [
    "Abaiara","Acarapé","Acaraú","Acopiara","Aiuaba","Alcântaras","Altaneira","Alto Santo","Amontada","Antonina Do Norte","Apuiarés",
    "Aquiraz","Aracati","Aracoiaba","Ararendá","Araripe","Aratuba","Arneiroz","Assaré","Aurora","Baixio","Banabuiú","Barbalha",
    "Barreira","Barro","Barroquinha","Baturité","Beberibe","Bela Cruz","Boa Viagem","Brejo Santo","Camocim","Campos Sales",
    "Canindé","Capistrano","Caridade","Cariré","Caririaçu","Cariús","Carnaubal", "Cascavel","Catarina","Catunda","Caucaia", 
    "Cedro","Chaval","Choró","Chorozinho","Coreaú","Crateús","Crato","Croatá","Cruz","Deputado Irapuan Pinheiro","Erere",
    "Eusébio","Farias Brito","Forquilha","Fortaleza","Fortim","Frecheirinha","General Sampaio","Graça","Granja","Granjeiro",
    "Groaíras","Guaiúba","Guaraciaba Do Norte","Guaramiranga","Hidrolândia","Horizonte","Ibaretama","Ibiapina","Ibicuitinga",
    "Icapuí","Icó","Iguatu","Independência","Ipaporanga","Ipaumirim","Ipu","Ipueiras","Iracema","Irauçuba","Itaiçaba","Itaitinga",
    "Itapagé","Itapipoca","Itapiúna","Itarema","Itatira","Jaguaretama","Jaguaribara","Jaguaribe","Jaguaruana","Jardim","Jati",
    "Jijoca De Jericoacoara","Juazeiro Do Norte","Jucás","Lavras Da Mangabeira","Limoeiro Do Norte","Madalena","Maracanaú",
    "Maranguape","Marco","Martinópole","Massapê","Mauriti""Meruoca","Milagres","Milhã","Miraíma","Missão Velha","Mombaça",
    "Monsenhor Tabosa","Morada Nova","Moraújo","Morrinhos","Mucambo","Mulungu","Nova Olinda","Nova Russas","Novo Oriente","Ocara",
    "Orós","Pacajus","Pacatuba","Pacoti","Pacujá","Palhano","Palmácia","Paracuru","Paraipaba","Parambu","Paramoti","Pedra Branca",
    "Penaforte","Pentecoste","Pereiro","Pindoretama","Piquet Carneiro","Pires Ferreira","Poranga","Porteiras","Potengi","Potiretama",
    "Quiterianópolis","Quixadá","Quixelô","Quixeramobim","Quixere","Redenção","Reriutaba","Russas","Saboeiro","Salitre","Santa Quitéria",
    "Santana Do Acaraú","Santana Do Cariri","São Benedito","São Gonçalo Do Amarante","Sao Joao Do Jaguaribe","São Luís Do Curu",
    "Senador Pompeu","Senador Sá","Sobral","Solonópole","Tabuleiro Do Norte","Tamboril","Tarrafas","Tauá","Tejuçuoca","Tianguá","Trairi",
    "Tururu","Ubajara","Umari","Umirim","Uruburetama","Uruoca","Varjota","Várzea Alegre","Viçosa do Ceará"
]

cidades_ceara = [unidecode(cidade) for cidade in cidades_ceara]

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

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

    #Colocando as cidades em title

    df['Cidade']  = df['Cidade'].str.title()

    # Renomear a coluna
    df = df.rename(columns={'Número do Município': 'Município', 
                            'Título da Despesa': 'Categoria da Despesa'})
    df['Valor'] = df['Valor'].apply(lambda x: locale.currency(x / 100, grouping=True, symbol=None))
    df['Valor'] = df['Valor'].apply(locale.atof)

    return df

def visualizacao_df(df, name):
    # Filtro de Municípios
    if cidade_interesse:
        df = df[df['Município'].isin(cidade_interesse)]

    # Filtro de Despesas
    if despesas_interesse:
        df = df[df['Categoria da Despesa'].isin(despesas_interesse)]
    
    # Filtro de Município associado ao CNPJ
    if localidade_interesse:
        df = df[df['Cidade'].isin(localidade_interesse)]

    #Filtro de Valores
    if valor_interesse:
        df = df[(df["Valor"] >= valor_interesse[0]) & (df["Valor"] <= valor_interesse[1])]
    
    # Verifica se o DataFrame está vazio após aplicar os filtros
    if df.empty and name == 'CNPJ' and (cidade_interesse or despesas_interesse or valor_interesse or localidade_interesse):
        # Escreve a mensagem de não correspondência no Streamlit
        st.warning(f"Não há correspondência para os filtros selecionados.")
    else:
        # Verifica se há filtros de cidade e despesa aplicados
        if (cidade_interesse or despesas_interesse or localidade_interesse) and name == 'CNPJ':
            # Cria as duas colunas
            col1, col2 = st.columns(2)

            # Coluna 1 - DataFrame filtrado
            col1.dataframe(df)

            # Verifica se há filtros de cidade, despesa e valor aplicados
            if cidade_interesse:
                cidades_filtradas = ', '.join(cidade_interesse)
                col2.markdown(f"<h3><b>Filtro de Cidade</b></h3>", unsafe_allow_html=True)
                col2.write(cidades_filtradas)

            if despesas_interesse:
                despesas_filtradas = ', '.join(despesas_interesse)
                col2.markdown(f"<h3><b>Filtro de Despesa</b></h3>", unsafe_allow_html=True)
                col2.write(despesas_filtradas)
            
            if valor_interesse:
                valor_minimo_formatado = locale.currency(valor_interesse[0], grouping=True, symbol=None)
                valor_maximo_formatado = locale.currency(valor_interesse[1], grouping=True, symbol=None)

                # Criando a string com a formatação desejada
                texto_filtro = f"Entre R$ {valor_minimo_formatado} - {valor_maximo_formatado}"
                col2.markdown(f"<h3><b>Filtro de Valor</b></h3>", unsafe_allow_html=True)
                col2.write(texto_filtro)

            if localidade_interesse:
                localidades_filtradas = ', '.join(localidade_interesse)
                col2.markdown(f"<h3><b>Filtro de município associado ao CNPJ</b></h3>", unsafe_allow_html=True)
                col2.write(localidades_filtradas)
        else:
            # Se não houver filtros aplicados ou o nome não for 'CNPJ', exibe o DataFrame inteiro sem utilizar colunas
            st.dataframe(df)
       
def download(df, cidade_interesse, despesas_interesse, localidade_interesse, valor_interesse):
    # Aplica os filtros no DataFrame
    if cidade_interesse:
        df = df[df['Município'].isin(cidade_interesse)]

    if despesas_interesse:
        df = df[df['Categoria da Despesa'].isin(despesas_interesse)]

    if localidade_interesse:
        df = df[df['Cidade'].isin(localidade_interesse)]

    if valor_interesse:
        df = df[(df["Valor"] >= valor_interesse[0]) & (df["Valor"] <= valor_interesse[1])]

    # Realiza o download da planilha
    csv = df.to_csv().encode('utf-8')
    st.download_button(
        label="Faço o download da planilha em formato .csv",
        data=csv,
        file_name='planilha_total.csv',
        mime='text/csv',
    )
    st.write('Se você realizou  seleções com os filtros, a planilha baixada terá também os filtros aplicados.')

def analise1(cidade_interesse, localidade_interesse, valor_interesse):
    df = limpeza_df_cnpj()
    #Colocando as cidades em title
    df['Cidade']  = df['Cidade'].str.title()
    # Verificar se os valores da coluna 'Cidade' estão presentes na lista de cidades_vales
    condicao = df['Cidade'].isin(cidades_ceara)
    # Aplica os filtros no DataFrame
    if cidade_interesse:
        df = df[df['Município'].isin(cidade_interesse)]

    if localidade_interesse:
        df = df[df['Cidade'].isin(localidade_interesse)]

    if valor_interesse:
        df = df[(df["Valor"] >= valor_interesse[0]) & (df["Valor"] <= valor_interesse[1])]
    
    # Filtrar as linhas do DataFrame que atendem à condição
    mpes_ceara = df[condicao]

    # Agrupar os dados e ordená-los
    analise1 = mpes_ceara.groupby(['Município']).sum().reset_index().sort_values('Valor', ascending=False)

    # Verificar se o DataFrame analise1 está vazio
    if analise1.empty:
        st.warning("Não há dados para exibir no gráfico.")
        return
    num_cidades = len(cidade_interesse) if cidade_interesse else 0
    font_size = get_font_size(num_cidades)
    # Criar o gráfico de barras usando Seaborn
    ax = sns.barplot(data=analise1, x='Município', y='Valor')

    # Rotacionar os rótulos do eixo x em 45 graus
    rotation = 0 if len(mpes_ceara['Município'].unique()) == 1 else 45
    ax.set_xticklabels(ax.get_xticklabels(), rotation=rotation, ha='right')

    # Adicionar título e rótulos dos eixos
    plt.title('Valor total das despesas realizadas com MPEs dentro do Ceará por município selecionado')
    plt.xlabel('Município')
    plt.ylabel('Valor (R$)')

    # Formatar rótulos do eixo y para exibir valores exatos sem notação científica
    plt.ticklabel_format(style='plain', axis='y')

    # Exibir o gráfico
    plt.show()

def analise2(cidade_interesse, despesas_interesse, localidade_interesse, valor_interesse):
    df = limpeza_df_cnpj()
    #Colocando as cidades em title
    # Aplica os filtros no DataFrame
    if cidade_interesse:
        df = df[df['Município'].isin(cidade_interesse)]

    if despesas_interesse:
        df = df[df['Categoria da Despesa'].isin(despesas_interesse)]

    if localidade_interesse:
        df = df[df['Cidade'].isin(localidade_interesse)]

    if valor_interesse:
        df = df[(df["Valor"] >= valor_interesse[0]) & (df["Valor"] <= valor_interesse[1])]
    
    df['Cidade']  = df['Cidade'].str.title()
    # Verificar se os valores da coluna 'Cidade' estão presentes na lista de cidades_vales
    condicao = df['Cidade'].isin(cidades_ceara)
    # Filtrar as linhas do DataFrame que atendem à condição
    mpes_ceara = df[condicao]
    # Agrupar os dados e ordená-los
    analise2 = mpes_ceara.groupby(['Município', 'Categoria da Despesa']).sum().reset_index().sort_values('Valor', ascending=False)
    if analise2.empty:
        st.warning("Não há dados para exibir no gráfico.")
        return
    else:
        st.dataframe(analise2)
        st.write('Esta planilha mostra a concentração de despesas com MPEs de dentro do Estado do Ceará, por município e categoria de despesa selecionados.')
        st.write('Observação: para melhor visualização do gráfico abaixo, é recomendado que sejam selecionadas até 4 municípios por vez, caso todas as despesas estejam também seleciondas.')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax = sns.barplot(data = analise2, x = 'Município', y = 'Valor', hue = 'Categoria da Despesa')
        rotation = 0 if len(mpes_ceara['Município'].unique()) == 1 else 45
        ax.set_xticklabels(ax.get_xticklabels(), rotation=rotation, ha='right')

        # Adicionar título e rótulos dos eixos
        plt.title('Valor total das despesas realizadas com MPEs dentro do Ceará por município e despesa selecionados',  fontweight='bold')
        plt.xlabel('Município', fontweight='bold')
        plt.ylabel('Valor', fontweight='bold')

        # Formatar rótulos do eixo y para exibir valores exatos sem notação científica
        plt.ticklabel_format(style='plain', axis='y')

        # Colocar a legenda abaixo do gráfico
        plt.legend(title='Legenda', bbox_to_anchor=(0.2, -0.10) if len(cidade_interesse) == 1 else (0.2, -0.35), loc='upper center')
        st.pyplot(fig)
        st.write('Este gráfico reflete a planilha anterior, representando os valores das somas de despesas com MPEs nos municípios e despesas selecionados.')

def analise3(cidade_interesse, localidade_interesse, valor_interesse):
    df = limpeza_df_cnpj()
    # Verificar se os valores da coluna 'Cidade' estão presentes na lista de cidades_vales
    df['Cidade']  = df['Cidade'].str.title()
    condicao = df['Cidade'].isin(cidades_vale)
    # Aplica os filtros no DataFrame
    if cidade_interesse:
        df = df[df['Município'].isin(cidade_interesse)]

    if localidade_interesse:
        df = df[df['Cidade'].isin(localidade_interesse)]

    if valor_interesse:
        df = df[(df["Valor"] >= valor_interesse[0]) & (df["Valor"] <= valor_interesse[1])]
    # Filtrar as linhas do DataFrame que atendem à condição
    mpes_vale = df[condicao]

    analise3 = mpes_vale.groupby(['Município']).sum().reset_index().sort_values('Valor', ascending=False)
# Verificar se o DataFrame analise1 está vazio
    if analise3.empty:
        st.warning("Não há dados para exibir no gráfico.")
    else:
        st.dataframe(analise3)
        st.write('Esta planilha mostra a concentração de despesas com MPEs de dentro do Vale do Jaguaribe, por município selecionado.')
        num_cidades = len(cidade_interesse) if cidade_interesse else 0
        font_size = get_font_size(num_cidades)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax = sns.barplot(data=analise3, x='Município', y='Valor')

        # Rotacionar os rótulos do eixo x em 45 graus
        rotation = 0 if len(mpes_vale['Município'].unique()) == 1 else 45
        ax.set_xticklabels(ax.get_xticklabels(), rotation=rotation, ha='right')

        # Adicionar título e rótulos dos eixos
        plt.title('Valor total das despesas realizadas com MPEs dentro do Ceará por município selecionado')
        plt.xlabel('Município')
        plt.ylabel('Valor (R$)')

        # Formatar rótulos do eixo y para exibir valores exatos sem notação científica
        plt.ticklabel_format(style='plain', axis='y')
        plt.legend().remove()
        # Exibir o gráfico
        st.pyplot(fig)


def analise4(cidade_interesse, despesas_interesse, localidade_interesse, valor_interesse):
    df = limpeza_df_cnpj()
    #Colocando as cidades em title
    # Aplica os filtros no DataFrame
    if cidade_interesse:
        df = df[df['Município'].isin(cidade_interesse)]

    if despesas_interesse:
        df = df[df['Categoria da Despesa'].isin(despesas_interesse)]

    if localidade_interesse:
        df = df[df['Cidade'].isin(localidade_interesse)]

    if valor_interesse:
        df = df[(df["Valor"] >= valor_interesse[0]) & (df["Valor"] <= valor_interesse[1])]
    
    df['Cidade']  = df['Cidade'].str.title()
    # Verificar se os valores da coluna 'Cidade' estão presentes na lista de cidades_vales
    condicao = df['Cidade'].isin(cidades_vale)
    # Filtrar as linhas do DataFrame que atendem à condição
    mpes_vale = df[condicao]
    # Agrupar os dados e ordená-los
    analise4 = mpes_vale.groupby(['Município', 'Categoria da Despesa']).sum().reset_index().sort_values('Valor', ascending=False)
    if analise4.empty:
        st.warning("Não há dados para exibir no gráfico.")
        return
    else:
        st.dataframe(analise4)
        st.write('Esta planilha mostra a concentração de despesas com MPEs de dentro do Estado do Ceará, por município e categoria de despesa selecionados.')
        st.write('Observação: para melhor visualização do gráfico abaixo, é recomendado que sejam selecionadas até 4 municípios por vez, caso todas as despesas estejam também seleciondas.')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax = sns.barplot(data = analise4, x = 'Município', y = 'Valor', hue = 'Categoria da Despesa')
        rotation = 0 if len(mpes_vale['Município'].unique()) == 1 else 45
        ax.set_xticklabels(ax.get_xticklabels(), rotation=rotation, ha='right')

        # Adicionar título e rótulos dos eixos
        plt.title('Valor total das despesas realizadas com MPEs dentro do Vale do Jaguaribe por município e despesa selecionados',  fontweight='bold')
        plt.xlabel('Município', fontweight='bold')
        plt.ylabel('Valor', fontweight='bold')

        # Formatar rótulos do eixo y para exibir valores exatos sem notação científica
        plt.ticklabel_format(style='plain', axis='y')

        # Colocar a legenda abaixo do gráfico
        plt.legend(title='Legenda', bbox_to_anchor=(0.2, -0.10) if len(cidade_interesse) == 1 else (0.2, -0.35), loc='upper center')
        st.pyplot(fig)
        st.write('Este gráfico reflete a planilha anterior, representando os valores das somas de despesas com MPEs nos municípios e despesas selecionados.')

def analise5(cidade_interesse, localidade_interesse, valor_interesse):
    df = limpeza_df_cnpj()
    # Verificar se os valores da coluna 'Cidade' estão presentes na lista de cidades_vales
    df['Cidade']  = df['Cidade'].str.title()
    # Aplica os filtros no DataFrame
    if cidade_interesse:
        df = df[df['Município'].isin(cidade_interesse)]

    if localidade_interesse:
        df = df[df['Cidade'].isin(localidade_interesse)]

    if valor_interesse:
        df = df[(df["Valor"] >= valor_interesse[0]) & (df["Valor"] <= valor_interesse[1])]
    
    mpe_cidade_igual = df.query("Município == Cidade")

    analise5 = mpe_cidade_igual.groupby(['Município']).sum().reset_index().sort_values('Valor', ascending=False)
    if analise5.empty:
        st.warning("Não há dados para exibir no gráfico.")
        return
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(analise5)
        with col2:
            st.write('Esta planilha mostra que a cidade em que a empresa está localizada é a mesma da cidade contratante, ou seja, se a despesa foi realizada com uma MPE dentro da própria cidade. Filtrado por município.')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax = sns.barplot(data=analise5, x='Município', y='Valor')
        # Rotacionar os rótulos do eixo x em 45 graus
        rotation = 0 if len(mpe_cidade_igual['Município'].unique()) == 1 else 45
        ax.set_xticklabels(ax.get_xticklabels(), rotation=rotation, ha='right')
        # Adicionar título e rótulos dos eixos
        plt.title('Valor total das despesas realizadas com MPEs dentro do Ceará por município selecionado')
        plt.xlabel('Município')
        plt.ylabel('Valor (R$)')

        # Formatar rótulos do eixo y para exibir valores exatos sem notação científica
        plt.ticklabel_format(style='plain', axis='y')
        plt.legend().remove()
        # Exibir o gráfico
        st.pyplot(fig)
        st.write('Este gráfico reflete a planilha anterior, representando os valores das somas de despesas realizadas com MPEs do próprio município, nos municípios e despesas selecionados.')

def analise6(cidade_interesse, despesas_interesse, localidade_interesse, valor_interesse):
    df = limpeza_df_cnpj()
    #Colocando as cidades em title
    # Aplica os filtros no DataFrame
    if cidade_interesse:
        df = df[df['Município'].isin(cidade_interesse)]

    if despesas_interesse:
        df = df[df['Categoria da Despesa'].isin(despesas_interesse)]

    if localidade_interesse:
        df = df[df['Cidade'].isin(localidade_interesse)]

    if valor_interesse:
        df = df[(df["Valor"] >= valor_interesse[0]) & (df["Valor"] <= valor_interesse[1])]
    
    df['Cidade']  = df['Cidade'].str.title()
    # Verificar se os valores da coluna 'Cidade' estão presentes na lista de cidades_vales
    # Agrupar os dados e ordená-los
    mpe_cidade_igual = df.query("Município == Cidade")
    analise6 = mpe_cidade_igual.groupby(['Município', 'Categoria da Despesa']).sum().reset_index().sort_values('Valor', ascending=False)
    if analise6.empty:
        st.warning("Não há dados para exibir no gráfico.")
        return
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(analise6)
        with col2:
            st.write('Esta planilha mostra que a cidade em que a empresa está localizada é a mesma da cidade contratante, ou seja, se a despesa foi realizada com uma MPE dentro da própria cidade. Filtrado por município e tipo de despesa.')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax = sns.barplot(data = analise6, x = 'Município', y = 'Valor', hue = 'Categoria da Despesa')        
        rotation = 0 if len(mpe_cidade_igual['Município'].unique()) == 1 else 45
        ax.set_xticklabels(ax.get_xticklabels(), rotation=rotation, ha='right')
    # Adicionar título e rótulos dos eixos
        plt.title('Valor total das despesas realizadas com MPEs do próprio município.')
        plt.xlabel('Município', fontweight='bold')
        plt.ylabel('Valor', fontweight='bold')
    # Formatar rótulos do eixo y para exibir valores exatos sem notação científica
        plt.ticklabel_format(style='plain', axis='y')
        plt.legend(title='Legenda', bbox_to_anchor=(0.2, -0.10) if len(cidade_interesse) == 1 else (0.2, -0.35), loc='upper center')
        st.pyplot(fig)
        st.write('Este gráfico reflete a planilha anterior, representando os valores das somas de despesas realizadas com MPEs do próprio município, nos municípios e despesas selecionados.')



def get_font_size(num_cidades):
    # Tamanho base da fonte
    base_font_size = 16

    # Número máximo de cidades para ajustar o tamanho da fonte
    max_cidades = 10

    # Cálculo do tamanho da fonte proporcional ao número de cidades selecionadas
    font_size = max(base_font_size - num_cidades, 8)  # O tamanho mínimo da fonte será 8

    return font_size

def soma1(cidade_interesse, localidade_interesse, valor_interesse, ):
    df = limpeza_df_cnpj()
    condicao = df['Cidade'].isin(cidades_ceara)
    # Aplica os filtros no DataFrame
    if cidade_interesse:
        df = df[df['Município'].isin(cidade_interesse)]

    if localidade_interesse:
        df = df[df['Cidade'].isin(localidade_interesse)]

    if valor_interesse:
        df = df[(df["Valor"] >= valor_interesse[0]) & (df["Valor"] <= valor_interesse[1])]
    mpes_ceara = df[condicao]
    analise1 = mpes_ceara.groupby(['Município']).sum().reset_index().sort_values('Valor', ascending=False)
    total_soma = analise1['Valor'].sum()

    return total_soma.round(2)

def soma2(cidade_interesse, localidade_interesse, valor_interesse, ):
    df = limpeza_df_cnpj()
    condicao = df['Cidade'].isin(cidades_vale)
    # Aplica os filtros no DataFrame
    if cidade_interesse:
        df = df[df['Município'].isin(cidade_interesse)]

    if localidade_interesse:
        df = df[df['Cidade'].isin(localidade_interesse)]

    if valor_interesse:
        df = df[(df["Valor"] >= valor_interesse[0]) & (df["Valor"] <= valor_interesse[1])]
    mpes_vale = df[condicao]
    analise3 = mpes_vale.groupby(['Município']).sum().reset_index().sort_values('Valor', ascending=False)
    total_soma = analise3['Valor'].sum()

    return total_soma.round(2)

    
#----------------------STREAMLIT - BARRA LATERAL------------------------------------------ #

st.set_option('deprecation.showPyplotGlobalUse', False)
# ------------------------------------------STREAMLIT - BARRA LATERAL------------------------------------------ #

## Filtro Cidade
st.sidebar.markdown('## Selecione o(s) município(s) de interesse')
cidade_interesse = st.sidebar.multiselect(
'Filtro de municípios - esses são os municípios que realizaram a compra',
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

## Filtro Localidades
df = limpeza_df_cnpj()
cidades_unicas = df['Cidade'].str.title().unique()
st.sidebar.markdown('## Selecione o(s) município(s) de interesse')
localidade_interesse = st.sidebar.multiselect(
'Filtro de municípios - esses são os municípios nos quais as empresas contratadas estão localizadas (última coluna da planilha)',
sorted(cidades_unicas),
default = None
)


## Filtro Valor
df = limpeza_df_cnpj()
valor_minimo = df["Valor"].min()
valor_maximo = df["Valor"].max()
st.sidebar.markdown('## Selecione o intervalo de valores de interesse')
valor_interesse = st.sidebar.slider(
'Selecione o intervalo de valores de interesse - aqui serão filtrados as despesas com valor correspondente ao intervalo selecionado.',
min_value=valor_minimo,
max_value=valor_maximo,
value=(valor_minimo, valor_maximo), 
)

image = Image.open('logo.png')

st.sidebar.image(image, width=120)

# ------------------------------------------STREAMLIT - LAYOUT PRINCIPAL------------------------------------------ #

def main():
    # Carrega o DataFrame após a limpeza e filtragem dos dados
    df_cnpjs = limpeza_df_cnpj()
    # Faz a soma dos valores

    total_soma = soma1(cidade_interesse, cidade_interesse, valor_interesse)
    total_soma2 = soma2(cidade_interesse, cidade_interesse, valor_interesse)
    # Descrição da Planilha
    st.markdown('#### Essa planilha registra todas as transações com MPEs nos municípios e despesas selecionadas')
    
    # Visualização do df de CNPJs
    visualizacao_df(df_cnpjs, 'CNPJ')
    download(df_cnpjs, cidade_interesse, despesas_interesse, localidade_interesse, valor_interesse)
    #Início dos gráficos
    st.markdown(f"<h2><b>Análises Gerais</b></h2>", unsafe_allow_html=True)
    st.markdown(f"<h2><b>1) Concentração das despesas com MPEs dentro do Estado de origem (Ceará) por município.</b></h2>", unsafe_allow_html=True)
    st.write("Nesse gráfico, os filtros de despesa não são aplicados. Os demais são normalmente.")
    st.pyplot(analise1(cidade_interesse, localidade_interesse, valor_interesse))
    st.markdown(f"<h5> A soma total das despesas realizadas com MPEs dentro de algum município do Ceará, contando os municípios selecionados é de: R${total_soma}</h5>", unsafe_allow_html=True)
    st.markdown(f"<h2><b>2) Concentração das despesas com MPEs dentro do Estado de origem (Ceará) por município e despesa.</b></h2>", unsafe_allow_html=True)
    analise2(cidade_interesse, despesas_interesse, localidade_interesse, valor_interesse)
    st.markdown(f"<h2><b>3) Concentração das despesas com MPEs dentro do Vale do Jaguaribe por município.</b></h2>", unsafe_allow_html=True)
    st.write("Nesse gráfico, os filtros de despesa não são aplicados. Os demais são normalmente.")
    analise3(cidade_interesse, localidade_interesse, valor_interesse)
    st.markdown(f"<h5> A soma total das despesas realizadas com MPEs dentro de algum município do Vale do Jaguaribe/CE, contando os municípios selecionados é de: R${total_soma2}</h5>", unsafe_allow_html=True)
    st.markdown(f"<h2><b>4) Concentração das despesas com MPEs dentro do Vale do Jaguaribe por município e despesa.</b></h2>", unsafe_allow_html=True)
    analise4(cidade_interesse, despesas_interesse, localidade_interesse, valor_interesse)
    st.markdown(f"<h2><b>5) Esta planilha mostra que a cidade em que a empresa está localizada é a mesma da cidade contratante, ou seja, mostra se a despesa foi realizada com uma MPE dentro da própria cidade.</b></h2>", unsafe_allow_html=True)
    st.write("Nesse gráfico, os filtros de despesa não são aplicados. Os demais são normalmente.")
    analise5(cidade_interesse, localidade_interesse, valor_interesse)
    st.markdown(f"<h2><b>6) Esta planilha mostra que a cidade em que a empresa está localizada é a mesma da cidade contratante, ou seja, mostra se a despesa foi realizada com uma MPE dentro da própria cidade.</b></h2>", unsafe_allow_html=True)
    analise6(cidade_interesse, despesas_interesse, localidade_interesse, valor_interesse)
if __name__ == '__main__':
    main()



