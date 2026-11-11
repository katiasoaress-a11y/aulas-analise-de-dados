from pathlib import Path
import pandas as pd


pasta_atual = Path(__file__).parent
caminho_entrada = pasta_atual / "dados_despadronizados.csv"
caminho_saida = pasta_atual / "dados_padronizados.csv"

df = pd.read_csv(caminho_entrada, dtype=str)

cpf_limpo = (
    df["cpf"]
    .str.replace(".", "", regex=False)
    .str.replace("-", "", regex=False)
    .str.replace(" ", "", regex=False)
)


df["cpf_valido"] = (cpf_limpo.str.len() == 11) & (cpf_limpo.str.isdigit())


df["cpf_formatado"] = (
    cpf_limpo.str.slice(0, 3) + "." +
    cpf_limpo.str.slice(3, 6) + "." +
    cpf_limpo.str.slice(6, 9) + "-" +
    cpf_limpo.str.slice(9, 11)
)

numero_limpo = (
    df["numero"]
    .str.replace("+55", "", regex=False)
    .str.replace("(", "", regex=False)
    .str.replace(")", "", regex=False)
    .str.replace("-", "", regex=False)
    .str.replace(" ", "", regex=False)
)

df["numero_valido"] = (numero_limpo.str.len() == 11) & (numero_limpo.str.isdigit())

df["numero_formatado"] = (
    "(" + numero_limpo.str.slice(0, 2) + ") " +
    numero_limpo.str.slice(2, 7) + "-" +
    numero_limpo.str.slice(7, 11)
)

salario_limpo = df["salario"].str.replace("R$", "", regex=False).str.strip()

tem_virgula = salario_limpo.str.contains(",", regex=False)

salario_br = (
    salario_limpo[tem_virgula]
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
)
salario_us = salario_limpo[~tem_virgula]

salario_numerico = pd.concat([salario_br, salario_us]).sort_index().astype(float)

df["salario_formatado"] = salario_numerico.apply(
    lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
)

salario_anual_num = salario_numerico * 12
df["salario_anual"] = salario_anual_num.apply(
    lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
)

colunas_finais = [
    "nome",
    "cpf",
    "cpf_formatado",
    "cpf_valido",
    "numero",
    "numero_formatado",
    "numero_valido",
    "salario",
    "salario_formatado",
    "salario_anual"
]

df_final = df[colunas_finais]

df_final.to_csv(caminho_saida, index=False, encoding="utf-8-sig")

print("Processamento concluído! Arquivo 'dados_padronizados.csv' gerado com sucesso.")
print(df_final.head())
