from pathlib import Path
import numpy as np
import pandas as pd

pasta_script = Path(__file__).parent
caminho_csv = pasta_script / 'vendas_mercados.csv'

if not caminho_csv.exists():
  arquivos_encontrados = list(
      pasta_script.parents[1].rglob('vendas_mercados.csv')
  )
  if arquivos_encontrados:
    caminho_csv = arquivos_encontrados[0]
  else:
    raise FileNotFoundError(
        "Arquivo 'vendas_mercados.csv' não encontrado no projeto. Verifique se"
        ' ele foi salvo dentro da pasta do PyCharm.'
    )


df = pd.read_csv(caminho_csv, sep=None, engine='python')


print('Colunas encontradas:', df.columns.tolist(), '\n')


df['Lucro'] = (df['Preco_Unitario'] - df['Custo_Unitario']) * df['Quantidade']
lucro_mercado = df.groupby('Mercado')['Lucro'].sum().sort_values(ascending=False)
print('=== 1. LUCRO POR MERCADO ===')
print(lucro_mercado, '\n')


pag_regiao = df.groupby(['Regiao', 'Forma_Pagamento']).size().unstack(fill_value=0)
print('=== 2. FORMA DE PAGAMENTO MAIS USADA POR REGIÃO ===')
print(pag_regiao.idxmax(axis=1), '\n')


qtd_produto = df.groupby('Produto')['Quantidade'].sum().sort_values(ascending=False)
print('=== 3. QUANTIDADE VENDIDA POR PRODUTO ===')
print(qtd_produto, '\n')


media_preco = df.groupby('Mercado')['Preco_Unitario'].mean().sort_values(ascending=False)
print('=== 4. MÉDIA DE PREÇO POR MERCADO ===')
print(media_preco.round(2), '\n')


df['Faturamento'] = df['Preco_Unitario'] * df['Quantidade']
faturamento_rede = np.sum(df['Faturamento'])
faturamento_mercado = df.groupby('Mercado')['Faturamento'].sum().sort_values(ascending=False)

print('=== 5. FATURAMENTO ===')
print(f'Faturamento Total da Rede: R$ {faturamento_rede:.2f}')
print(faturamento_mercado, '\n')


df['Preco_Promocional'] = np.where(
    df['Quantidade'] >= 10,
    df['Preco_Unitario'] * 0.90,  # Aplica 10% de desconto (paga 90%)
    df['Preco_Unitario'],  # Mantém o preço original
)

df['Faturamento_Promocional'] = df['Preco_Promocional'] * df['Quantidade']
novo_faturamento_rede = np.sum(df['Faturamento_Promocional'])

print('=== 6. SIMULAÇÃO DE PROMOÇÃO ===')
print(f'Novo Faturamento Total da Rede: R$ {novo_faturamento_rede:.2f}')

