from bs4 import BeautifulSoup
from typing import Optional, List, Dict


def parse_response(
    html: str, *, dangerously_allow_looping_last_item: bool = False
) -> Dict:
    class _Blank:
        def get_text(self, *_, **__):
            return ""

        def select(self, *_, **__):
            return []

    blank = _Blank()                         # Instância única p/ retornos vazios
    safe = lambda node: node or blank        # Wrapper de segurança

    soup = BeautifulSoup(html, "lxml")

    # Seletor dos cartõezinhos de voos (primeiro = “melhor voo”)
    cards = soup.select('div[jsname="IWWDBc"], div[jsname="YdtKid"]')
    flights: List[Dict] = []

    for i, card in enumerate(cards):
        is_best_flight = i == 0

        # Cada voo fica em um <li>; às vezes o último é “+ N voos”
        items = card.select("ul.Rk10dc li")
        if not dangerously_allow_looping_last_item and not is_best_flight:
            items = items[:-1]  # descarta último, se existir

        for li in items:
            # Companhia
            name = safe(li.select_one("div.sSHqwe.tPgKwe.ogfYpf span")) \
                   .get_text(strip=True)

            # Partida / chegada
            dp_ar = li.select("span.mv1WYe div")
            departure_time = dp_ar[0].get_text(strip=True) if len(dp_ar) > 0 else ""
            arrival_time   = dp_ar[1].get_text(strip=True) if len(dp_ar) > 1 else ""

            # Duração
            duration = safe(li.select_one("li div.Ak5kof div")).get_text(strip=True)

            # Escalas
            stops_raw = safe(li.select_one(".BbR8Ec .ogfYpf")).get_text(strip=True)
            try:
                stops_fmt = 0 if stops_raw == "Nonstop" else int(stops_raw.split(" ", 1)[0])
            except ValueError:
                stops_fmt = "Unknown"

            # Preço
            price_raw = safe(li.select_one(".YMlIz.FpEdX")).get_text(strip=True) or "0"
            price_int = int(price_raw.replace("R$", "").replace(",", "").strip())

            flights.append(
                {
                    "is_best": is_best_flight,
                    "cia": name,
                    "departure": " ".join(departure_time.split()),
                    "arrival": " ".join(arrival_time.split()),
                    "duration": duration,
                    "stops": stops_fmt,
                    "price": price_int,
                }
            )

    if not flights:
        raise RuntimeError("No flights found in supplied HTML.")

    # Seleciona o(s) voo(s) de menor preço e devolve o primeiro
    cheapest = min(f["price"] for f in flights)
    return next(f for f in flights if f["price"] == cheapest)