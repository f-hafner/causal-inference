import pandas as pd 
import matplotlib.pyplot as plt 

def read_data(file): 
    return pd.read_stata("https://github.com/scunning1975/mixtape/raw/master/" + file)


def load_data():
    "Download the data from the book website and prepare a dataframe"
    nsw_dw = read_data('nsw_mixtape.dta')
    nsw_dw_cpscontrol = read_data('cps_mixtape.dta')

    # for differentiating groups later 
    nsw_dw["randomised"] = 1 
    nsw_dw_cpscontrol["randomised"] = 0

    nsw_stacked = pd.concat((nsw_dw_cpscontrol, nsw_dw))

    # unemployment 
    nsw_stacked[["unemp74", "unemp75"]] = 0
    nsw_stacked.loc[nsw_stacked.re74==0, 'unemp74'] = 1
    nsw_stacked.loc[nsw_stacked.re75==0, 'unemp75'] = 1

    # rename earnings
    nsw_stacked = nsw_stacked.rename(columns={"re74": "earn74", "re75": "earn75", "re78": "earn78"})

    return nsw_stacked



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

