from PIL import Image
import pandas as pd
import numpy as np
import folium
import streamlit as st

#/c/Users/vitor/anaconda3/python
# ------------------------------------------VARIÁVEIS------------------------------------------ #
coordenadas_vale = [[-5.517017, -38.268787], [-6.032490, -38.347886], [-5.811328, -38.304214],
                    [-5.609542, -38.762743], [-4.831508, -37.781000], [-5.894643, -38.624820],
                    [-5.145575, -38.096861], [-5.101460, -38.370047], [-5.454494, -38.467930], [-4.746674, -37.964020], 
                    [-6.047814, -38.462518], [-5.722839, -38.153925], [-5.073436, -37.988587], [-4.937737, -37.976338], 
                    [-5.270538, -38.272238], [-5.244573, -38.128230]]
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

CAMINHO_ARQUIVO = 'planilhas\cnpjs.xlsx'

# ------------------------------------------FUNÇÕES------------------------------------------ #
def criacao_lat_long(coordenadas, cidades):
    # Criando o dicionário com as colunas
    dados = {
        'Cidade': cidades,
        'Latitude': [coord[0] for coord in coordenadas],
        'Longitude': [coord[1] for coord in coordenadas],
    }

    # Criando o DataFrame
    df = pd.DataFrame(dados)

    return df

def lista_cnpj(caminho):
    lista_cnpj = pd.read_excel(caminho)
    return lista_cnpj

def limpeza_df(df):
    # Filtrar apenas CNPJs
    df = df[df['CNPJ'].str.len() > 14]

    # Substituir os valores dos pontos e traços
    #df['CNPJ'] = df['CNPJ'].str.replace('.', '').str.replace('-', '').str.replace('/', '')
    #df['Valor (R$)'] = df['Valor (R$)'].str.replace('.', '').str.replace(',', '')

    # Selecionar as despesas de interesse
    
    df = df[df['Despesa'].isin(despesas)]

    # Converta as chaves do dicionário para o tipo de dados da coluna 'Número do Município'
    df['Número do Município'] = df['Número do Município'].astype(int)

    # Substituir os números pelo nome dos municípios usando o mapeamento_cidades
    df['Número do Município'] = df['Número do Município'].map(mapeamento_cidades)

    # Renomear a coluna
    df = df.rename(columns={'Número do Município': 'Município', 
                            'Despesa': 'Categoria da Despesa'})

    return df

def soma(df):
    soma = df['Valor (R$)'].sum()
    return soma

def load_map_html(df):
    m = folium.Map(location=[-5.690900, -38.575244], zoom_start=8, min_zoom=7)

    # Percorremos o dataframe e colocamos um marcador em cada cidade do Vale
    for _, row in df.iterrows():
        popup_content = f"<b>Cidade: </b>{row['Cidade']}/CE <br>"
        marker = folium.Marker(location=[row['Latitude'], row['Longitude']],
                               popup=popup_content,
                               icon=folium.Icon(color='red', icon='info-sign'))
        marker.add_to(m)

    map_html = m.get_root().render()
    return map_html

# ------------------------------------------CONFIGURAÇÃO STREAMLIT------------------------------------------#
st.set_page_config(page_title='Consultoria - CNPJs', layout='wide')
st.title('Consultoria - CNPJs')

#-----------------------------------------STREAMLIT: BARRA LATERAL-------------------------------------------#

st.sidebar.markdown('### Essa é a visão geral dos dados.')
st.sidebar.markdown(' ### Aqui temos um mapa indicando cada município analisado, assim como uma planilha com os dados referentes a todas as informaçções de despesas, municípios, CNPJs, etc.')

image = Image.open('logo.png')

st.sidebar.image(image, width=120)

# ------------------------------------------LAYOUT PRINCIPAL STREAMLIT------------------------------------------ #

df_lat_long = criacao_lat_long(coordenadas_vale, cidades_vale)

def main():
    global show_map
    # Carregamento do DataFrame e criação do mapa são realizados apenas uma vez
    df_lat_long = criacao_lat_long(coordenadas_vale, cidades_vale)
    mapa = load_map_html(df_lat_long)

    if show_map:
        # Mostra o mapa no Streamlit    
        st.components.v1.html(mapa, height=400, width=900)
    
    st.markdown('## Essa planilha representa as despesas interessadas e seus respectivos municípios e CNPJs associados')
    
    # Verifica se os dados foram previamente carregados em cache
    @st.cache_data(persist=True)
    def get_cleaned_data(caminho):
        return limpeza_df(lista_cnpj(caminho))
    
    # Carrega o DataFrame após a limpeza e filtragem dos dados
    df = get_cleaned_data(CAMINHO_ARQUIVO)

    # Exibe o DataFrame filtrado no Streamlit
    st.dataframe(df)

    # Concatenando as cidades em uma única string separada por vírgulas
    cidades_texto = ", ".join(cidades_vale)

    # Exibindo "Municípios" em fonte maior e em negrito
    st.markdown("<h3><b>Municípios</b></h3>", unsafe_allow_html=True)
    # Exibindo as cidades lado a lado
    st.write(cidades_texto)

    # Concatenando as despesas em uma única string separada por vírgulas
    despesas_texto = ", ".join(despesas)

    # Exibindo "Despesas" em fonte maior e em negrito
    st.markdown("<h3><b>Despesas</b></h3>", unsafe_allow_html=True)

    # Exibindo as despesas lado a lado
    st.write(despesas_texto)

if __name__ == '__main__':
    main()
