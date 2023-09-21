import matplotlib.pyplot as plt 


def make_histogram(df, input_map, xlabel="Value"):
    "Make a histogram of df, mapping over inputs in `input_map`."
    plt.figure(figsize=(6, 4))
    plt.title("Histogram of propensity score")
    plt.xlabel(xlabel)
    plt.ylabel("Density")
    plt.grid(True)

    for label, params in input_map.items():
        x = df.loc[params["mask"], "pscore"]
        # Create histograms for each group
        plt.hist(x, bins=20, density=True, alpha=0.7, color=params["color"], label=label)

        # Add legend
        plt.legend()

    # Display the plot
    plt.show()


def plot_balance(differences, title, xlabel):
    "Plot the balance before and after matching for differences in means or standard deviations"
    plt.figure(figsize=(6, 4))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Variable")

    names = list(differences.keys())
    post = [x[0] for x in differences.values()]
    pre = [x[1] for x in differences.values()]
    data = {"before matching": [pre, "orange"], "after matching": [post, "blue"]}

    for label, inputs in data.items():
        values, color = inputs
        plt.scatter(values, names, color=color, label=label)

        plt.legend()

    # Display the plot
    plt.axvline(0, color="grey")
    plt.show()


