import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from collections import defaultdict


def gather_experiments_data():
    K_errs = {'mean': [], 'top_mean': [], 'query': []}
    K_xs = sorted(K_mean_data.keys())
    K_ys = {'mean': [], 'top_mean': [], 'query': []}
    L_errs = {'mean': [], 'top_mean': [], 'query': []}
    L_xs = sorted(L_mean_data.keys())
    L_ys = {'mean': [], 'top_mean': [], 'query': []}
    for k in K_xs:
        K_errs['mean'].append(np.std(K_mean_data[k]))
        K_errs['top_mean'].append(np.std(K_top_mean_data[k]))
        K_errs['query'].append(np.std(K_query_time_data[k]))
        K_ys['mean'].append(np.mean(K_mean_data[k]))
        K_ys['top_mean'].append(np.mean(K_top_mean_data[k]))
        K_ys['query'].append(np.mean(K_query_time_data[k]))
    for l in L_xs:
        L_errs['mean'].append(np.std(L_mean_data[l]))
        L_errs['top_mean'].append(np.std(L_top_mean_data[l]))
        L_errs['query'].append(np.std(L_query_time_data[l]))
        L_ys['mean'].append(np.mean(L_mean_data[l]))
        L_ys['top_mean'].append(np.mean(L_top_mean_data[l]))
        L_ys['query'].append(np.mean(L_query_time_data[l]))
    plot_mean_and_std_sim_and_query(K_xs, K_ys, K_errs, 'K')
    plot_mean_and_std_sim_and_query(L_xs, L_ys, L_errs, 'L')
    plot_mean_and_std_sim_and_query(alpha_xs, alpha_ys, alpha_errs, 'alpha')
    plt.show()


def plot_mean_and_std_sim_and_query(xs, ys, errs, val_str):
    fig, axes = plt.subplots(2, 2, figsize=(20, 10))
    axes[0, 0].set_title(
        f"Error (for {val_str})")
    axes[0, 0].set_ylabel("Jaccard similarity")
    axes[0, 0].set_xlabel(f"{val_str} value")
    axes[0, 0].errorbar(xs, ys['mean'], yerr=errs['mean'], fmt='-o')
    axes[0, 1].set_title(
        f"Mean and std similarities of top 10 retrieved results of queries (for {val_str})")
    axes[0, 1].set_ylabel("Jaccard similarity")
    axes[0, 1].set_xlabel(f"{val_str} value")
    axes[0, 1].errorbar(xs, ys['top_mean'],
                        yerr=errs['top_mean'], fmt='-o')
    axes[1, 0].set_title(f"Mean and std query times (for {val_str})")
    axes[1, 0].set_ylabel("Seconds")
    axes[1, 0].set_xlabel(f"{val_str} value")
    axes[1, 0].errorbar(xs, ys['query'], yerr=errs['query'], fmt='-o')
    fig.savefig(f"{val_str}_experiment_values.jpg")
