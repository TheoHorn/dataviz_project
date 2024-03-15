import pandas as pd
import plotly.express as px
file_path = '/Users/benjamincordebar/Desktop/2A/S8/VBD/viz_project/data/chocolate.csv'
data = pd.read_csv(file_path)   # return a dataframe

data_cleaned = data.dropna(subset=['ingredients'])

# Décoder les ingrédients
ingredients = {
    'B': 'Beans',
    'S': 'Sugar',
    'S*': 'Sweetener other than sugar',
    'C': 'Cocoa Butter',
    'V': 'Vanilla',
    'L': 'Lecithin',
    'Sa': 'Salt'
}

# Créer une copie indépendante pour éviter les avertissements lors de la modification
data_cleaned2 = data.dropna(subset=['ingredients']).copy()

for ingredient, full_name in ingredients.items():
    data_cleaned2[full_name] = data_cleaned2['ingredients'].apply(lambda x: 1 if ingredient in x else 0)

# Afficher les premières lignes du DataFrame nettoyé avec les nouvelles colonnes d'ingrédients
#print(data_cleaned2.head())
    
# Nous allons ajouter une nouvelle colonne qui compte le nombre d'ingrédients pour chaque chocolat
data_cleaned2['Num_Ingredients'] = data_cleaned2[['Beans', 'Sugar', 'Sweetener other than sugar', 'Cocoa Butter', 'Vanilla', 'Lecithin', 'Salt']].sum(axis=1)

    
# Grouper par année ('review_date') et calculer la moyenne du nombre d'ingrédients et la moyenne des notes
average_values_per_year = data_cleaned2.groupby('review_date').agg({'Num_Ingredients': 'mean', 'rating': 'mean'}).reset_index()

# Renommer les colonnes pour plus de clarté
average_values_per_year.rename(columns={'Num_Ingredients': 'Average_Ingredients', 'rating': 'Average_Rating'}, inplace=True)

# Afficher le résultat
# print(average_values_per_year)

# Définir les bins et les labels pour les catégories
bins = [0, 2, 3, 4, 5, 7]  
labels = ['0-2', '2-3', '3-4', '4-5', '5-7']

# Créer une nouvelle colonne 'Ingredients_Category'
average_values_per_year['Ingredients_Category'] = pd.cut(average_values_per_year['Average_Ingredients']