import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('vgchartz-2024.csv')

sales = df.groupby('console')['total_sales'].sum()
sales = sales.sort_values(ascending=False)
sales[:5].plot(kind='bar')
plt.xlabel('Konsol')
plt.ylabel('Försäljning (miljon kr)')
plt.show()
