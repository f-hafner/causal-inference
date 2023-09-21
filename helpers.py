import pandas as pd 
from dataclasses import dataclass 
import numpy as np

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


@dataclass
class SumStat:
    """Summary statistic of a variable between two groups 0 and 1
    The summary statistics are the difference in means and the respective variances.
    """
    mu_diff: float = None 
    sigma1: float = None 
    sigma0: float = None

    def normdiff(self, denominator=None):
        "Returns normalized differences"
        if denominator is None:
            denominator = np.sqrt((self.sigma0 + self.sigma1)/2)
        return self.mu_diff / denominator
    
    def diff_logstd(self):
        "Returns difference in standard deviations"
        s1 = np.sqrt(self.sigma1)
        s0 = np.sqrt(self.sigma0)
        return np.log(s1 / s0) 
    

def compute_stats(df_1, df_0, xvar):
    "Compute statistics for overlap on `xvar` between df_1 and df_0"
    x1 = df_1.loc[:, xvar].copy()
    x0 = df_0.loc[:, xvar].copy()
    mu_diff = x1.mean() - x0.mean()
    return SumStat(mu_diff, x1.var(), x0.var())


def compute_balancing_stats(xvars, treated, control_prematch, control_postmatch): 
    "Compute balancing statistics for two dataframes, before and after matching"
    sumstats = {}

    for x in xvars:
        prematch = compute_stats(treated, control_prematch, x)
        postmatch = compute_stats(treated, control_postmatch, x)
        sumstats[x] = (postmatch, prematch)

    normalized_differences = {}
    diff_log_stds = {}
    for x, stats in sumstats.items():
        postmatch, prematch = stats
        denominator = np.sqrt((postmatch.sigma1 + postmatch.sigma0)/2)

        mudiff_post, mudiff_pre = (y.normdiff(denominator=denominator) for y in stats) 
        stddiff_post, stddiff_pre = (y.diff_logstd() for y in stats)
        
        normalized_differences[x] = (mudiff_post, mudiff_pre)
        diff_log_stds[x] = (stddiff_post, stddiff_pre)

    return normalized_differences, diff_log_stds