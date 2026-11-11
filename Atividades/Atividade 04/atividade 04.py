from pathlib import Path
import pandas as pd

caminho_arquivo = Path(__file__).parent / "estoque_supermercado.csv"
df = pd.read_csv(caminho_arquivo)


df["preco"] = (
    df["preco"]
    .astype(str)
    .str.replace("R$", "", regex=False)
    .str.replace(",", ".", regex=False)
    .str.strip()
)
df["preco"] = pd.to_numeric(df["preco"], errors="coerce")
df["preco"] = df["preco"].fillna(df["preco"].mean())

# 2.2 Limpeza da Coluna 'quantidade'
df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce")
df["quantidade"] = df["quantidade"].fillna(0).astype(int)

# 2.3 Padronização da Coluna 'setor'
df["setor"] = df["setor"].fillna("sem setor").str.strip().str.capitalize()
df["setor"] = df["setor"].replace({"": "sem setor", "Nan": "sem setor"})

# 2.4 Tratamento de Datas
df["data_compra"] = pd.to_datetime(df["data_compra"], format="%d/%m/%Y", errors="coerce")
df["data_vencimento"] = pd.to_datetime(df["data_vencimento"], format="%d/%m/%Y", errors="coerce")


print("\n--- BASE DE DADOS LIMPA ---")
print(df.head(10))



print("\n--- PRODUTOS VENCENDO ESTA SEMANA ---")
vencendo_semana = df[
    (df["data_vencimento"] >= "2026-10-27") &
    (df["data_vencimento"] <= "2026-11-03")
]
print(vencendo_semana[["nome", "quantidade", "setor", "data_vencimento"]])

print("\n--- MAIOR QUANTIDADE A VENCER ---")
maior_qtd_vencer = vencendo_semana.sort_values(by="quantidade", ascending=False).head(1)
print(maior_qtd_vencer[["nome", "quantidade", "setor", "data_vencimento"]])


print("\n--- COMPRAS RECENTES (ÚLTIMOS 3 DIAS) ---")
compras_recentes = df[
    (df["data_compra"] >= "2026-10-24") &
    (df["data_compra"] <= "2026-10-27")
]
print(compras_recentes[["nome", "quantidade", "setor", "data_compra"]])


print("\n--- PRODUTOS SEM DATA DE VENCIMENTO ---")
sem_vencimento = df[df["data_vencimento"].isna()]
print(sem_vencimento[["nome", "quantidade", "setor", "data_vencimento"]])


df["valor_total_estoque"] = df["quantidade"] * df["preco"]

print("\n--- MAIOR VALOR PATRIMONIAL POR SETOR ---")
valor_por_setor = (
    df.groupby("setor")["valor_total_estoque"]
    .sum()
    .sort_values(ascending=False)
)
print(valor_por_setor)

setor_campeao = valor_por_setor.idxmax()
valor_campeao = valor_por_setor.max()
print(f"\nSetor com maior valor parado no estoque: {setor_campeao} (R$ {valor_campeao:,.2f})")
