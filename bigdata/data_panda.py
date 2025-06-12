import pandas as pd
df = pd.read_csv("vgchartz-2024.csv")

print("\n\nDataset information:")
print(df.info())

print("\n\nDataset description:")
print(df.describe())

print("\n\nDataset columns:")
print(df.columns)

print("\n\nDataset shape:")
print(df.shape)

print("\n\nTotal sales > 10: ")
high_sales = df[df['total_sales'] > 10]
print(high_sales[['title', 'total_sales', 'console']])

print("\n\nTop 5 games by total sales:")
top_sales = df.nlargest(5, 'total_sales')
print(top_sales[['title', 'total_sales', 'console']])

print("\n\nTotal sales per console")
sales_per_console = df.groupby('console')['total_sales'].sum()
print(sales_per_console)