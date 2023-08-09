import matplotlib.pyplot as plt

data = [('before discover plt.xkcd', 1), ('after discover plt.xkcd', 3)]
keys, values = list(zip(*data))
with plt.xkcd():
    fig = plt.figure(figsize = (10, 6))
    plt.bar(keys, values, color ='black', width = 0.5)
    plt.xlabel("discover plt.xkcd")
    plt.ylabel("general life happiness")
    plt.title("Influence of discover plt.xkcd to general life happiness")
    plt.show()
