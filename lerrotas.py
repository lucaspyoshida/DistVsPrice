import pandas as pd

df = pd.read_csv('./malha_aerea_codigos.csv', sep=';')
print(df.head(5))
