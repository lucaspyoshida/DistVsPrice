import requests
from bs4 import BeautifulSoup
import re
url = "https://www.flightmanager.com/content/TimeDistanceForm.aspx"
header = {
'method' : 'post',
'validateHttpsCertificates' : "false",
}

def achardistancia(origem,destino):
    payload = {
        "ctl00$ContentPlaceHolder1$txtDepartureICAO": origem,
        "ctl00$ContentPlaceHolder1$txtArrivalICAO": destino,
        "ctl00$ContentPlaceHolder1$txtAirSpeed": 450,
        "ctl00$ContentPlaceHolder1$BtnSubmit": 'Submit',
        "__VIEWSTATEGENERATOR":"EAE2BF6D",
        "__VIEWSTATE": 'kQe/LNkE1X5HAfDvU3+JuwP3SwKu4LQ7eXimqRgYo21UDv4O+slIlpG8TueG8G5a4i/9D8v9ydj/EOOSdvOHfEc7gn0ajDjYXUCdThQ1dTsYwa6S'
    }

    response = requests.post(url, headers=header, data=payload)
    soup = BeautifulSoup(response.text, 'lxml')

    tds = soup.find_all('td')
    def texto_direto(td):
        return ''.join(td.find_all(string=True, recursive=False)).strip()

    celula = list(filter(lambda x: 'Distance:' in texto_direto(x), tds))
    texto = celula[0].text
    texto = texto.replace('.', ',')
    match = re.search(r'(\d{1,3}(?:,\d{3})*,\d+)\s*\(KM\)', texto)

    if match:
        bruto = match.group(1)        
        partes = bruto.split(',')
        numero_final = ''.join(partes[:-1]) + ',' + partes[-1] 
        valor_float = float(numero_final.replace(',', '.'))  # <- aqui a correção
        return valor_float


if __name__ == "__main__":
    print(achardistancia("SBBR","SBSP"))
    