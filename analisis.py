import matplotlib.pyplot as plt
import seaborn as sns

# Descripción básica del DataFrame
print(df.describe())

# Distribución de la población
plt.figure(figsize=(10, 6))
sns.histplot(df['Population'], bins=30, kde=True)
plt.title('Distribución de la Población')
plt.xlabel('Población')
plt.ylabel('Frecuencia')
plt.show()

# Distribución del área
plt.figure(figsize=(10, 6))
sns.histplot(df['Area'], bins=30, kde=True)
plt.title('Distribución del Área')
plt.xlabel('Área (km²)')
plt.ylabel('Frecuencia')
plt.show()

# Relación entre población y área
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Area', y='Population')
plt.title('Relación entre Población y Área')
plt.xlabel('Área (km²)')
plt.ylabel('Población')
plt.show()