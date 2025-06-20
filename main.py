from gerarlink.criarendereco import criar_url_voo
from scrap import lerurl
from lerhtml import parse_response
import pandas as pd
import time
from distancia.distancia import achardistancia
import os
import re

voos = pd.read_csv('./datasets/malha_aerea_codigos.csv')
filtro_sexta = voos['Frequencia'].str.contains('sexta', case=False, na=False)
df_sexta = voos[filtro_sexta].copy() 
df_sexta.loc[:, 'Rota'] = df_sexta['Origem (IATA)'] + '-' + df_sexta['Destino (IATA)']
filtro_rotas_unicas = ~df_sexta.duplicated(subset='Rota', keep=False)
df_rotas_unicas = df_sexta[filtro_rotas_unicas]

final = []

def iterar_voos():
    for index, row in df_rotas_unicas.iterrows():
        try:
            url = criar_url_voo(
                date="2025-09-19",
                from_airport=row['Origem (IATA)'],
                to_airport=row['Destino (IATA)'],
                max_stops=0,
                airlines=["G3"],  
            )
            body = lerurl(url)
            origem_iata = row['Origem (IATA)']
            destino_iata = row['Destino (IATA)']
            origem_icao = row['Origem (ICAO)']
            destino_icao = row['Destino (ICAO)']
            origem_nome = row['Origem'].replace(' ', '_')
            destino_nome = row['Destino'].replace(' ', '_')
            nome_arquivo = (
                f'raw_data/{origem_iata}-{origem_icao}_{origem_nome}'
                f'__{destino_iata}-{destino_icao}_{destino_nome}.html'
            )
            os.makedirs('raw_data', exist_ok=True)
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write(body)
            print(f"✔ HTML salvo: {nome_arquivo}")

        #     voos = parse_response(body) 
        #     voos['origem (IATA)'] = row['Origem (IATA)']
        #     voos['origem (ICAO)'] = row['Origem (ICAO)']
        #     voos['origem'] = row['Origem']
        #     voos['destino'] = row['Destino']
        #     voos['destino (ICAO)'] = row['Destino (ICAO)']
        #     voos['destino (IATA)'] = row['Destino (IATA)']
        #     voos['distancia'] = achardistancia(row['Origem (ICAO)'], row['Destino (ICAO)'])
        #     final.append(voos)
        #     df_final = pd.DataFrame(final)
        #     df_final.to_csv('./datasets/voos.csv', index=False)
        #     print(voos)
        #     time.sleep(5)
        except Exception as e:
            print(f"Erro ao processar rota {row['Origem (IATA)']} - {row['Destino (IATA)']}: {str(e)}")
            time.sleep(5)
    
    processar_raw_data()


def processar_raw_data():
    final = []
    arquivos = [f for f in os.listdir("raw_data") if f.endswith('.html')]
    os.makedirs(os.path.dirname("./datasets/voos.csv"), exist_ok=True)
    for arquivo in arquivos:
        try:
            #Regex para extrair dados do nome do arquivo
            match = re.match(r'^([A-Z]{3})-([A-Z]{4})_(.+?)__([A-Z]{3})-([A-Z]{4})_(.+?)\.html$', arquivo)
            if not match:
                print(f"Nome de arquivo inválido: {arquivo}")
                continue

            origem_iata, origem_icao, origem_nome, destino_iata, destino_icao, destino_nome = match.groups()

            with open(os.path.join("raw_data", arquivo), 'r', encoding='utf-8') as f:
                body = f.read()

            voo = parse_response(body)

            voo['origem (IATA)'] = origem_iata
            voo['origem (ICAO)'] = origem_icao
            voo['origem'] = origem_nome.replace('_', ' ')
            voo['destino (IATA)'] = destino_iata
            voo['destino (ICAO)'] = destino_icao
            voo['destino'] = destino_nome.replace('_', ' ')
            voo['distancia'] = achardistancia(origem_icao, destino_icao)
            final.append(voo)

            print(f"✔ Processado: {origem_iata}-{destino_iata}")
            df_final = pd.DataFrame(final)
            df_final.to_csv("./datasets/voos.csv", index=False)
            time.sleep(1)

        except Exception as e:
            print(f"❌ Erro ao processar {arquivo}: {e}")
            continue

    print(f"\n✅ CSV salvo em: voos.csv")

iterar_voos()

