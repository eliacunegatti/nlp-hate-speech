import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
folder_path = "results/"
my_list = os.listdir(folder_path)

hast = []
h = []
all_items = {}
for item in my_list:
    df = pd.read_csv(folder_path+item, sep=",",header=None)
    print(df)
    hate = df[2].to_list()
    h.append(np.mean(hate))
    for i in range(len(df)):
        all_items[df[0].iloc[i]] = df[2].iloc[i]


for i in range(len(my_list)):
    my_list[i] = my_list[i].replace(".csv","")



bars = my_list
y_pos = np.arange(len(bars))

# Create bars
plt.bar(y_pos, h)

# Create names on the x-axis
plt.xticks(y_pos, bars, rotation=90)

# Show graphic
plt.show()
import collections

all_items = dict(sorted(all_items.items(), key=lambda item: item[1],reverse=True))
print(all_items)

plt.figure(figsize=(4,6))
h = []
b = []
for key, value in all_items.items():
    b.append(key)
    h.append(value)


b = b[:20]
h = h[:20]
b = b[::-1]
h = h[::-1]
y_pos = np.arange(len(b))

# Create bars
plt.barh(y_pos, h, color="red")

# Create names on the x-axis
plt.yticks(y_pos, b)

# Show graphic
plt.show()