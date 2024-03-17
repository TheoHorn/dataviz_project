import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
from scipy.ndimage import gaussian_gradient_magnitude

# Read the data
data = pd.read_csv('data/chocolate.csv')

choco_color = np.array(Image.open("img/cacao.jpg"))
choco_color = choco_color[::3, ::3]

# create mask of the image without the white background
choco_mask = choco_color.copy()
choco_mask[choco_mask.sum(axis=2) == 0] = 255

# we do edges detection to accentuate the edges
edges = np.mean([gaussian_gradient_magnitude(choco_color[:, :, i] / 255., 2) for i in range(3)], axis=0)
choco_mask[edges > .08] = 255

wc = WordCloud(max_words=2000, mask=choco_mask, max_font_size=40, random_state=42, background_color='#f6eddb')

# generate word cloud
wc.generate(' '.join(data['most_memorable_characteristics']))

# create coloring from image
image_colors = ImageColorGenerator(choco_color)
wc.recolor(color_func=image_colors)

plt.figure(figsize=(12, 12))
plt.imshow(wc, interpolation="bilinear")
plt.axis('off')

# Save the image with higher resolution (dpi)
plt.savefig('img/wordcloud_chocolate2.png', dpi=600, bbox_inches='tight')

