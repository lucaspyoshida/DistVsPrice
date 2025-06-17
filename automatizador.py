from gerarlink.criarendereco import criar_url_voo
from scrap import lerurl
from lerhtml import parse_response
import pandas as pd
import time
from distancia.distancia import achardistancia

voos = pd.read_csv('./malha_aerea_codigos.csv')
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
            voos = parse_response(body) 
            voos['origem (IATA)'] = row['Origem (IATA)']
            voos['origem (ICAO)'] = row['Origem (ICAO)']
            voos['origem'] = row['Origem']
            voos['destino'] = row['Destino']
            voos['destino (ICAO)'] = row['Destino (ICAO)']
            voos['destino (IATA)'] = row['Destino (IATA)']
            voos['distancia'] = achardistancia(row['Origem (ICAO)'], row['Destino (ICAO)'])
            final.append(voos)
            df_final = pd.DataFrame(final)
            df_final.to_csv('voos.csv', index=False)
            print(voos)
            time.sleep(5)
        except Exception as e:
            print(f"Erro ao processar rota {row['Origem (IATA)']} - {row['Destino (IATA)']}: {str(e)}")
            time.sleep(5)

iterar_voos()