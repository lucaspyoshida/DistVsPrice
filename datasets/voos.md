# voos.csv

Resultados obtidos do scraper do Google Flights para cada rota analisada.

| Coluna            | Tipo    | Descrição                                                     |
|-------------------|---------|---------------------------------------------------------------|
| is_best           | lógico  | Indica se o Google marcou o voo como melhor opção            |
| cia               | texto   | Companhia aérea                                               |
| departure         | texto   | Data e hora de saída no formato do site                       |
| arrival           | texto   | Data e hora de chegada no formato do site                     |
| duration          | texto   | Duração total do voo                                          |
| stops             | inteiro | Número de paradas                                             |
| price             | inteiro | Preço da passagem (BRL)                                       |
| origem (IATA)     | texto   | Código IATA do aeroporto de origem                            |
| origem (ICAO)     | texto   | Código ICAO do aeroporto de origem                            |
| origem            | texto   | Nome do aeroporto ou cidade de origem                         |
| destino           | texto   | Nome do aeroporto ou cidade de destino                        |
| destino (ICAO)    | texto   | Código ICAO do aeroporto de destino                           |
| destino (IATA)    | texto   | Código IATA do aeroporto de destino                           |
| distancia         | decimal | Distância da rota em quilômetros                              |
