from typing import List, Optional
from .flights_impl import FlightData, Passengers, TFSData

def criar_url_voo(
    date: str,
    from_airport: str,
    to_airport: str,
    max_stops: Optional[int],
    airlines: Optional[List[str]] = None,
) -> str:
    flight_data = [
        FlightData(date=date, from_airport=from_airport, to_airport=to_airport,airlines=airlines)
    ]
    passengers = Passengers(adults=1)
    tfs_data_obj = TFSData.from_interface(
        flight_data=flight_data,
        trip="one-way",
        passengers=passengers,
        seat="economy",
        max_stops=max_stops,
        airlines=airlines
    )

    # 4. Serializa e codifica os dados em Base64 para gerar o parâmetro 'tfs'
    b64_string = tfs_data_obj.as_b64()

    # 5. Monta o dicionário de parâmetros para a URL
    params = {
        "tfs": b64_string.decode("utf-8"),
        "hl": "en",  # Define o idioma para inglês
    }

    # Adiciona o parâmetro das companhias aéreas ('i'), se fornecido
    # if airlines:
    #     params["i"] = ",".join(airlines)

    # 6. Constrói a URL final, juntando a base com os parâmetros
    url = "https://www.google.com/travel/flights?" + "&".join(
        f"{k}={v}" for k, v in params.items() if v
    )

    return url


# Exemplo de como usar a função
if __name__ == "__main__":
    url_gerada = criar_url_voo(
        date="2025-09-15",
        from_airport="BSB",
        to_airport="GRU",
        max_stops=0,
        airlines=["G3"],  
    )
    print("URL Gerada:")
    print(url_gerada)