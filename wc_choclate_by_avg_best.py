import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
from scipy.ndimage import gaussian_gradient_magnitude
from fuzzywuzzy import fuzz

# Read the data
data = pd.read_csv('data/chocolate.csv')

# Function to merge similar characteristics
def merge_similar_characteristics(characteristics):
    merged = {}
    for char in characteristics:
        merged[char] = char
        for key in merged.keys():
            if char != key and fuzz.partial_ratio(char, key) >= 80:
                merged[char] = key
                break
    return merged

# Split multiple characteristics and explode into separate rows
data['most_memorable_characteristics'] = data['most_memorable_characteristics'].str.split(',')
data = data.explode('most_memorable_characteristics')

# Merge similar characteristics
similar_characteristics = merge_similar_characteristics(data['most_memorable_characteristics'].unique())
data['most_memorable_characteristics'] = data['most_memorable_characteristics'].map(similar_characteristics)

# Remove characteristics with less than 3 occurrences
data = data.groupby('most_memorable_characteristics').filter(lambda x: len(x) > 3)

# Calculate average rating for each characteristic
average_rating = data.groupby('most_memorable_characteristics')['rating'].mean().to_dict()

# Normalize ratings to range from 0 to 1
min_rating = min(average_rating.values())
max_rating = max(average_rating.values())
normalized_ratings = {word: (rating - min_rating) / (max_rating - min_rating) for word, rating in average_rating.items()}

mask = np.array(Image.open("img/ellipse.png"))

wc = WordCloud(max_words=2000, max_font_size=30, mask=mask, random_state=41,background_color='#f6eddb',colormap='viridis')

wc.generate_from_frequencies(normalized_ratings)

plt.figure(figsize=(12, 12))
plt.imshow(wc, interpolation="bilinear")
plt.axis('off')
plt.savefig('img/wordcloud_best_characteristics.png', dpi=600, bbox_inches='tight')