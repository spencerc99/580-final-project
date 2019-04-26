from algorithms.ace import ACE
from algorithms.utils import get_bot_tweet_data
import numpy as np
from sklearn.model_selection import train_test_split
SAMPLE_PERCENT = 0.05


def main():
    Ks = [1, 2, 3, 4, 5, 6]
    Ls = [20, 50, 100, 200]
    alphas = []
    for K in Ks:
        for L in Ls:
            for alpha in alphas:
                ace_alg = ACE(K, L, alpha)
                run_experiment(ace_alg)


def get_data():
    df = get_bot_tweet_data()
    num_rows = len(df)
    return df.sample(int(num_rows * SAMPLE_PERCENT)),


def run_experiment(ace_alg):
    # measure accuracy, recall, precision
    # gather_plotting_data(measured_data)
    data = get_data()
    train, test = train_test_split(data, test_size=0.2)
    ace_alg.preprocess(train)

    for test_sample in test:
        is_anomaly = ace_alg.query(test_sample)
        if is_anomaly:
            print(f"Sample: {test_sample} is an anomaly")
        else:
            print(f"Sample: {test_sample} is not an anomaly")
        # print("Sample is actually {anomaly or not anomaly}")


def gather_plotting_data(data):
    pass


if __name__ == '__main__':
    main()
