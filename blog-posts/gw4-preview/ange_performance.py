import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os


logo = "plots/logos/tottenham.png"

# Load the CSV data
csv_path = "blog-posts/gw4-preview/ange_data.csv"
df = pd.read_csv(csv_path)
df["Date"] = pd.to_datetime(df["Date"])

# Creating rolling averages for xG and xGA
df = df.dropna(subset=["xG"])
df['rolling_xG'] = df['xG'].rolling(window=5).mean()
df['rolling_xGA'] = df['xGA'].rolling(window=5).mean()

# Fitting a linear trend for xG
x = df.index
y_xG = df["rolling_xG"]
z_xG = np.polyfit(x, y_xG, 1)
p_xG = np.poly1d(z_xG)

# Fitting a linear trend for xGA
y_xGA = df["rolling_xGA"]
z_xGA = np.polyfit(x, y_xGA, 1)
p_xGA = np.poly1d(z_xGA)


# Apply the dark background style
plt.style.use("dark_background")

# Creating the line graph
fig, ax = plt.subplots(figsize=(10,6))
plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15)

# Plotting the data and trend line
ax.plot(x, df["rolling_xG"], label="Rolling xG Average", color="#FFFFFF") 
ax.plot(x, df["rolling_xGA"], label="Rolling xGA Average", color="#132257") 

ax.plot(x, p_xG(x), color="#FFFFFF", linestyle="--", label="Trend Line", alpha=1) 
ax.plot(x, p_xGA(x), color="#FFFFFF", linestyle="--", label="Trend Line", alpha=1) 

ax.axvline(x=39, color="white", linestyle="--", alpha=.65, label="24-25 Season", dashes=(6,6)) 

# Adding labels to plot
ax.text(39.5, 1.21, "24-25 Season", rotation=90,                        verticalalignment='center', color='white', 
         fontsize=7, fontdict={"fontweight": "bold"}, alpha=0.7)
trend_label_x_position = x[-1]
trend_label_y_position = p_xG(x[-1]) -.5

# Customizing appearance
sns.despine(left=True, bottom=True)
ax.grid(True, axis='y', color='gray')

# Adjust labels and ticks
ax.set_xlabel("")
ax.set_xticks([])

ax.set_ylabel("Rolling xG & xGA Average", color="white")

# Titles
ax.set_title("Tottenham's performances have varied under Ange Postecoglu", x=0.39, pad=40, fontdict={"fontsize": 14, "fontweight": "bold"})
fig.suptitle("xG & xGA rolling 5-game average | Premier League", x=0.268, y=.915, size=10, weight="bold", alpha=0.76 )

prem_logo = OffsetImage(plt.imread(logo), zoom=0.25)
ab = AnnotationBbox(prem_logo, xy=(0.95, 1.09), xycoords="axes fraction", frameon=False, box_alignment=(0.5, 0.5))
ax.add_artist(ab)

plt.show()

print(df.shape)
print(df["rolling_xG"].shape)
