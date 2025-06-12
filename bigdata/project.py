import pandas as pd

df = pd.read_csv('personality_dataset.csv')

print(f"\nFirst ten rows: ")
print(df.head(10))

print(f"\n\nDatatypes and statistics: ")
print("\n\nDataset information:" )
print(df.info())
