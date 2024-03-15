import pandas as pd
import plotly.express as px

# Charger le fichier de données
file_path = '/Users/benjamincordebar/Desktop/2A/S8/VBD/viz_project/data/chocolate.csv'
data = pd.read_csv(file_path)

# Afficher le nombre de lignes avant suppression
#print(f"Nombre de lignes avant suppression: {data.shape[0]}")

# Supprimer les lignes où la colonne 'ingredients' contient des valeurs manquantes
data_cleaned = data.dropna(subset=['ingredients'])

# Afficher le nombre de lignes après suppression
#print(f"Nombre de lignes après suppression: {data_cleaned.shape[0]}")

# À ce stade, data_cleaned contient votre jeu de données sans les lignes manquantes dans 'ingredients'


### -- Visualisation exemple : evolution of the notes according to the years -- ###

# Grouper les données par 'review_date' et calculer la moyenne des notes
data_grouped = data_cleaned.groupby('review_date')['rating'].mean().reset_index()

# Créer un graphique linéaire avec Plotly
fig = px.line(data_grouped, x='review_date', y='rating', title='Évolution moyenne des notes par année',
              labels={'review_date': 'Année', 'rating': 'Note moyenne'})

# Afficher le graphique
#fig.show()

# Enregistrer le graphique dans un fichier HTML
file_name = '/Users/benjamincordebar/Desktop/2A/S8/VBD/viz_project/dynamic_representations/ben/evolution_of_the_notes_according_to_the_years.html'
fig.write_html(file_name)
