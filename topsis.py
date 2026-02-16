import pandas as pd
import numpy as np


# Validation Function
def validate_inputs(df, weights, impacts):

    # minimum column check
    if df.shape[1] < 3:
        raise Exception("Input file must contain at least three columns.")

    # numeric validation (2nd column onward)
    try:
        df.iloc[:, 1:] = df.iloc[:, 1:].astype(float)
    except:
        raise Exception("Columns from 2nd to last must contain numeric values only.")

    # weights & impacts length
    if len(weights) != len(impacts):
        raise Exception("Number of weights and impacts must be same.")

    if len(weights) != df.shape[1] - 1:
        raise Exception("Weights/Impacts count must match number of criteria columns.")

    # impacts validation
    for i in impacts:
        if i not in ['+', '-']:
            raise Exception("Impacts must be either '+' or '-'.")


# Core TOPSIS Algorithm
def calculate_topsis(df, weights, impacts):

    data = df.iloc[:, 1:].values.astype(float)

    # Step 1: Normalization
    norm_matrix = data / np.sqrt((data ** 2).sum(axis=0))

    # Step 2: Apply weights
    weights = np.array(weights)
    weighted_matrix = norm_matrix * weights

    # Step 3: Ideal Best & Worst
    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(np.max(weighted_matrix[:, i]))
            ideal_worst.append(np.min(weighted_matrix[:, i]))
        else:
            ideal_best.append(np.min(weighted_matrix[:, i]))
            ideal_worst.append(np.max(weighted_matrix[:, i]))

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    # Step 4: Distance calculation
    s_plus = np.sqrt(((weighted_matrix - ideal_best) ** 2).sum(axis=1))
    s_minus = np.sqrt(((weighted_matrix - ideal_worst) ** 2).sum(axis=1))

    # Step 5: TOPSIS Score
    score = s_minus / (s_plus + s_minus)

    # Step 6: Ranking
    rank = score.argsort()[::-1] + 1

    df['Topsis Score'] = score
    df['Rank'] = rank

    return df


# Public Function (Used by Flask)
def run_topsis(input_file, weights, impacts, output_file):
    """
    Runs TOPSIS on given input file.

    Parameters:
        input_file (str)
        weights (str) -> "1,1,1,1"
        impacts (str) -> "+,+,-,+"
        output_file (str)
    """

    # parse inputs
    weights = weights.split(',')
    impacts = impacts.split(',')

    try:
        weights = [float(w) for w in weights]
    except:
        raise Exception("Weights must be numeric.")

    # read file (CSV or Excel)
    try:
        if input_file.endswith('.csv'):
            df = pd.read_csv(input_file,low_memory=True))
        elif input_file.endswith('.xlsx'):
            df = pd.read_excel(input_file)
        else:
            raise Exception("Unsupported file format. Use CSV or XLSX.")
    except FileNotFoundError:
        raise Exception("Input file not found.")

    # validation
    validate_inputs(df, weights, impacts)

    # apply topsis
    result_df = calculate_topsis(df, weights, impacts)

    # save result
    result_df.to_csv(output_file, index=False)

    return output_file

import gc
gc.collect()
