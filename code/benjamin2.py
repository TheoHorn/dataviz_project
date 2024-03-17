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
average_values_per_year['Ingredients_Category'] = pd.cut(average_values_per_year['Average_Ingredients'], bins=bins, labels=labels, right=False)


fig = px.scatter(average_values_per_year, x="review_date", y="Average_Rating", color="Ingredients_Category", 
                 marginal_y="violin", marginal_x="box", trendline="ols", template="simple_white")

fig.update_layout(plot_bgcolor='#f6eddb', paper_bgcolor='#DA8A56')

# Enregistrer le graphique 
fig.write_html("/Users/benjamincordebar/Desktop/2A/S8/VBD/viz_project/dynamic_representations/average_rating_per_year_per_ingredients.html")


### ---------------------------------------- ###

# Créer un graphique linéaire pour visualiser l'évolution du nombre d'ingrédients par année
fig = px.line(average_values_per_year, x='review_date', y='Average_Ingredients', title='Évolution du nombre d\'ingrédients par année',
              labels={'review_date': 'Année', 'Average_Ingredients': 'Nombre d\'ingrédients'},color_discrete_sequence=['#2b0808'])

fig.update_layout(plot_bgcolor='#f6eddb', paper_bgcolor='lightgray')

# Enregistrer le graphique 
fig.write_html("/Users/benjamincordebar/Desktop/2A/S8/VBD/viz_project/dynamic_representations/average_ingredient_per_year.html")

# Commentaire : clairement le nombre d'ingrédiants diminue avec le temps


### ---------------------------------------- ###

# Créer un graphique linéaire pour visualiser l'évolution de la note moyenne par année
fig = px.line(average_values_per_year, x='review_date', y='Average_Rating', title='Évolution de la note moyenne par année',
              labels={'review_date': 'Année', 'Average_Rating': 'Note moyenne'},color_discrete_sequence=['#2b0808'])

fig.update_layout(plot_bgcolor='#f6eddb', paper_bgcolor='lightgray')

# Enregistrer le graphique
#fig.write_html("/Users/benjamincordebar/Desktop/2A/S8/VBD/viz_project/dynamic_representations/average_rating_per_year.html")


### ---------------------------------------- ###

# Calculer le coefficient de corrélation de Pearson (coefficent de corrélation de Pearson) entre le nombre d'ingrédients et la note moyenne
correlation = average_values_per_year['Average_Ingredients'].corr(average_values_per_year['Average_Rating'])

# print("Le coefficient de corrélation de Pearson est :", correlation)
# Commentaire : prudance dans l'interprétation, la corrélation n'implique pas causalité


### ---------------------------------------- ###

## -- seaborn -- ##

#imshow pour visualiser la matrice de corrélation
import seaborn as sns
import matplotlib.pyplot as plt

# Calculer la matrice de corrélation
correlation_matrix = average_values_per_year[['Average_Ingredients', 'Average_Rating']].corr()

# Renommage des colonnes dans la matrice de corrélation pour des étiquettes plus descriptives
correlation_matrix = correlation_matrix.rename(index={'Average_Ingredients': 'Nombre moyen d\'ingrédients', 'Average_Rating': 'Note Moyenne'},
                                               columns={'Average_Ingredients': 'Nombre moyen d\'ingrédients', 'Average_Rating': 'Note Moyenne'})


# Utiliser la fonction heatmap de seaborn pour visualiser la matrice de corrélation
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', cbar=True)

## -- seaborn -- ##


## -- plotly -- ##
# Définir une échelle de couleurs personnalisée en marron
brown_scale = [
    [0, 'rgb(255,248,220)'],  # Cornsilk color
    [0.5, 'rgb(210,180,140)'],  # Tan color
    [1, '#96421D']  # Brown color
]
# imshow avec plotly
fig = px.imshow(correlation_matrix, color_continuous_scale=brown_scale, text_auto=True, 
                title='Matrice de corrélation entre le nombre d\'ingrédients et la note moyenne')
# Mise à jour du titre et de l'étiquette de la barre de couleurs
fig.update_layout(
    coloraxis_colorbar=dict(
        title='Coefficient de corrélation de Pearson',
    )
)
fig.show()

## -- plotly -- ##

