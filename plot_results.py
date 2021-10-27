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
    if item ==".DS_Store":
        my_list.remove(item)
for item in my_list:
    df = pd.read_csv(folder_path+item, sep=",",header=None)
    hate = df[2].to_list()
    h.append(np.mean(hate))
    for i in range(len(df)):
        all_items[df[0].iloc[i]] = df[2].iloc[i]


for i in range(len(my_list)):
    my_list[i] = my_list[i].replace(".csv","").lower()



h = [float(i)/sum(h) for i in h]

df = pd.DataFrame()
df["h"] = h
df["b"] = my_list

df = df.sort_values(by="h", ascending=False)
print(df)

bars = df["b"]
h = df["h"]

bars = bars[::-1]
h = h[::-1]
y_pos = np.arange(len(bars))

# Create bars
plt.barh(y_pos, h)

# Create names on the x-axis
plt.yticks(y_pos, bars)
plt.title("Hate Speech by category",size=16)
# Show graphic
plt.show()
import collections

all_items = dict(sorted(all_items.items(), key=lambda item: item[1],reverse=True))
print(all_items)

plt.figure(figsize=(4,6))
h = []
b = []
for key, value in all_items.items():
    b.append(key.lower())
    h.append(value)




h = [float(i)/sum(h) for i in h]
b = b[:20]
h = h[:20]
b = b[::-1]
h = h[::-1]
y_pos = np.arange(len(b))

# Create bars
plt.barh(y_pos, h, color="red")

# Create names on the x-axis
plt.yticks(y_pos, b)
plt.title("Top Hate Speech #",size=16)
# Show graphic
plt.show()


my_list = os.listdir(folder_path)
for item in my_list:
    if item ==".DS_Store":
        my_list.remove(item)

for item in my_list:
    cat_items = {}
    df = pd.read_csv(folder_path+item, sep=",",header=None)
    hate = df[2].to_list()
    for i in range(len(df)):
        cat_items[df[0].iloc[i]] = df[2].iloc[i]
    cat_items = dict(sorted(cat_items.items(), key=lambda item: item[1],reverse=True))
    print(cat_items)
    b = []
    h = []
    for key, value in cat_items.items():
        b.append(key)
        h.append(value)
    h = [float(i)/sum(h) for i in h]

    b = b[:10]
    h = h[:10]

    b = b[::-1]
    h = h[::-1]

    h1 = []
    b1 = []
    for i in range(len(h)):
        if h[i] >0:
            h1.append(h[i])
            b1.append(b[i])
    
    print(h)
    
    y_pos = np.arange(len(b1))

    # Create 1bars
    plt.barh(y_pos, h1, color="orange")

    # Create names on the x-axis
    plt.yticks(y_pos, b1)

    # Show graphic
    item = item.replace(".csv","")
    item = item.upper()
    plt.title(item)
    plt.show()