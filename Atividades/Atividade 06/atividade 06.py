import matplotlib.pyplot as plt
import pandas as pd


caminho_arquivo = 'customers-10000.csv'
df = pd.read_csv(caminho_arquivo)

# Visualizar as colunas disponíveis para conferência
print('Colunas da base:', df.columns.tolist())
print('-' * 50)



top_paises = df['Country'].value_counts()
pais_mais_vendido = top_paises.idxmax()
qtd_pais = top_paises.max()


top_cidades = df['City'].value_counts()
cidade_mais_vendida = top_cidades.idxmax()
qtd_cidade = top_cidades.max()

print(
    f'1. País com mais assinaturas: {pais_mais_vendido} ({qtd_pais} registros)'
)
print(
    f'   Cidade com mais assinaturas: {cidade_mais_vendida} ({qtd_cidade}'
    ' registros)'
)
print('-' * 50)


top_10_paises = top_paises.head(10).sort_values(
    ascending=True
)  # Ordena para o maior ficar no topo

plt.figure(figsize=(10, 6))
top_10_paises.plot(kind='barh', color='#2b5c8f', edgecolor='black')
plt.title('Top 10 Países com Maior Número de Clientes', fontsize=14, pad=15)
plt.xlabel('Quantidade de Assinaturas', fontsize=12)
plt.ylabel('País', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('top_10_paises.png', dpi=300)  # Salva o gráfico em alta qualidade
plt.show()


df['Subscription Date'] = pd.to_datetime(df['Subscription Date'])


df['Ano'] = df['Subscription Date'].dt.year
df['Mes'] = df['Subscription Date'].dt.month
df['Ano_Mes'] = df['Subscription Date'].dt.to_period('M')

vendas_por_ano = df['Ano'].value_counts().sort_index()
vendas_por_mes = df['Mes'].value_counts().sort_values(ascending=False)
vendas_por_ano_mes = df['Ano_Mes'].value_counts().sort_index()

print('2. Volume de vendas por Ano:')
print(vendas_por_ano)
print('\n   Top 3 Meses com maior volume histórico (1=Jan, 12=Dez):')
print(vendas_por_mes.head(3))
print(
    f'\n   Mês/Ano específico com maior pico: {vendas_por_ano_mes.idxmax()}'
    f' ({vendas_por_ano_mes.max()} vendas)'
)
print('-' * 50)


plt.figure(figsize=(12, 5))
vendas_por_ano_mes.plot(
    kind='line', marker='o', color='#d95f02', linewidth=2, markersize=4
)
plt.title('Evolução da Quantidade de Assinaturas ao Longo do Tempo', fontsize=14)
plt.xlabel('Período (Ano-Mês)', fontsize=12)
plt.ylabel('Quantidade de Assinaturas', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('evolucao_assinaturas.png', dpi=300)
plt.show()


top_5_empresas = df['Company'].value_counts().head(5)

print('3. Top 5 Maiores Clientes Corporativos (B2B):')
print(top_5_empresas)
print('-' * 50)
