import pandas as pd
df = pd.read_csv("vgchartz-2024.csv")

print("\n\n 1:")
print(df.head(10))

print("\n\n 2:")
print(f"Number of rows: {df.shape[0]}")
print(f"Number of columns: {df.shape[1]}")
print(f"Data type of critic_score: {type(df['critic_score'])}")
sales_columns = sum('_sales' in col for col in df.columns)
print(f"Number of columns including _sales: {sales_columns}")

print("\n\n 3:")
critics_score = df[df['critic_score'] > 9.9]
print(f"Critic score over 9.9: {critics_score[['title', 'critic_score', 'total_sales']]}")
gta_game = df[df['title'] == 'Grand Theft Auto V']
print(f"\nGrand Theft Auto V has sold {gta_game['total_sales'].values[0]} miljoner kopior")

