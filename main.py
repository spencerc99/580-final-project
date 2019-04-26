from algorithms.ace import ACE
from algorithms.utils import get_bot_tweet_data, get_normal_tweet_data
import numpy as np
from sklearn.model_selection import train_test_split

SAMPLE_PERCENT = 0.05
SAMPLE_NUMBER = 50000
TEST_SAMPLE_NUMBER = 1000


def main():
    # Ks = [1, 2, 3, 4, 5, 6]
    # Ls = [20, 50, 100, 200]
    # alphas = []
    Ks = [5]
    Ls = [20]
    for K in Ks:
        for L in Ls:
            ace_alg = ACE(K, L, None)
            run_experiment(ace_alg)


def get_data():
    df = get_bot_tweet_data()
    df2 = get_normal_tweet_data()
    num_rows = len(df)
    # return df.sample(int(num_rows * SAMPLE_PERCENT))
    return df.sample(SAMPLE_NUMBER), df2.sample(TEST_SAMPLE_NUMBER)


def run_experiment(ace_alg):
    # measure accuracy, recall, precision
    # gather_plotting_data(measured_data)
    data, normal_user_data = get_data()
    train, test = train_test_split(data, test_size=0.02)
    ace_alg.preprocess(train)
    fp = 0
    tp = 0
    tn = 0
    fn = 0
    alphas = [0.05, 0.1, 0.25, 0.5, .75, 1]
    total_test_num = len(test) + len(normal_user_data)
    print("TOTAL TEST:", total_test_num)
    for alpha in alphas:
        with open(f"results_alpha={alpha}.csv", "w") as f:
            print("id,content,is_anomaly", file=f)
            # go through non-anomalies (bot tweets)
            for _, test_sample in test.iterrows():
                is_anomaly = ace_alg.query(test_sample, alpha)
                if is_anomaly:
                    print(
                        f"{test_sample.tweet_id}, {test_sample.content},1", file=f)
                    fp += 1
                else:
                    print(
                        f"{test_sample.tweet_id}, {test_sample.content},0", file=f)
                    tn += 1
            # go through anomalies (regular tweets)
            for _, test_sample in normal_user_data.iterrows():
                is_anomaly = ace_alg.query(test_sample, alpha)
                if is_anomaly:
                    print(
                        f"{test_sample.tweet_id}, {test_sample.content},1", file=f)
                    tp += 1
                else:
                    print(
                        f"{test_sample.tweet_id}, {test_sample.content},0", file=f)
                    fn += 1
            print(f"EXPERIMENT RESULTS FOR ALPHA={alpha}")
            print("FP:", fp)
            print("TP:", tp)
            print("TN:", tn)
            print("FN:", fn)
            accuracy = (tp+tn) / total_test_num
            precision = tp / (tp + fp)
            recall = tp / (tp + fn)
            f1 = 2 * (precision * recall) / (precision + recall)
            print("Accuracy:", accuracy)
            print("precision:", precision)
            print("recall:", recall)
            print("f1:", f1)
            fp = 0
            tp = 0
            tn = 0
            fn = 0


def gather_plotting_data(data):
    pass


if __name__ == '__main__':
    main()
