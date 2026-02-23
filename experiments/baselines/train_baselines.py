import lightgbm as lgb
from tqdm import tqdm
# import matplotlib.pyplot as plt
from sklearn.datasets import load_svmlight_file
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
import numpy as np
import pandas as pd
import argparse
import os


# in nested ensemble count all predictions not None or null
def count_leaves(ensemble):
    # number of leaves equals number of nodes that make predictions, i.e. prediction != None or prediction != null
    count = 0
    for model in ensemble.models:
        for node in model.nodes:
            if node.prediction is not None:
                count += 1
    return count

# replace int64 values with int values for json serialization
def convert_int64(obj):
    if isinstance(obj, dict):
        return {k: convert_int64(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_int64(v) for v in obj]
    elif isinstance(obj, np.int64):
        return int(obj)
    else:
        return obj

# counts number of nodes (internal + leaves) in a sklearn ensemble model
def count_nodes(model):
    count = 0
    if isinstance(model, (GradientBoostingClassifier, GradientBoostingRegressor)):
        for estimator in model.estimators_:
            for tree in estimator:
                    count += tree.tree_.node_count
    if isinstance(model, lgb.Booster):
        model_json = model.dump_model()
        for tree in model_json['tree_info']:
            count += tree['num_leaves'] * 2 - 1
    return count

def evaluate_model(model, X_test, y_test, task):
    if(isinstance(model, lgb.Booster)):
        y_pred = model.predict(X_test.toarray())#, predict_disable_shape_check=True)
        if task == "multiclass":
            y_pred = np.argmax(y_pred, axis=1)
    else:
        y_pred = model.predict(X_test)
    if task in "binary":
        test_acc = accuracy_score(y_test, np.where(y_pred > 0.5, 1, 0))
    elif task == "regression":
        test_acc = mean_squared_error(y_test, y_pred)
    elif task == "multiclass":
        test_acc = accuracy_score(y_test, y_pred)
    else:
        raise ValueError(f"Unknown task: {task}")
    return test_acc

def load_data(dir,dataset_name):
    """
    Load dataset by name. Supported names:.
    Returns (X_train, y_train), (X_test, y_test)"""
    # TODO: adapt to other paths
    return load_svmlight_file('{}/{}.train'.format(dir,dataset_name)), load_svmlight_file('{}/{}.test'.format(dir,dataset_name)),load_svmlight_file('{}/{}.val'.format(dir,dataset_name))

def quantize(in_path, out_path, data_type="float16"):
    """
    Quantize numbers in lines starting with 'threshold=' or 'leaf_value='
    to the specified numpy data type, while preserving string length
    by padding with zeros if needed.

    Parameters
    ----------
    in_path : str
        Path to the input text file.
    out_path : str
        Path to the output text file.
    data_type : str
        NumPy data type (e.g., 'float16', 'float32').
    """
    with open(in_path, "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith("threshold=") or line.startswith("leaf_value="):
            key, values_str = line.split("=")
            values = values_str.strip().split()
            converted = []
            for v in values:
                # Convert to desired dtype
                # cover values out of range for int8; recover initial v length
                if data_type == "int8":
                    if float(v) < -128:
                        v = "-128." + "0" * (len(v) - 5)
                    elif float(v) > 127:
                        v = "127." + "0" * (len(v) - 4)
                qv = np.dtype(data_type).type(float(v))
                # convert to float again to have decimal point in string representation
                qv_str = str(float(qv))

                # Preserve original string length as lightgbm knows number of characters per tree (tree_sizes)
                if len(qv_str) < len(v):
                    qv_str = qv_str + "0" * (len(v) - len(qv_str))
                elif len(qv_str) > len(v):
                    # If quantized string is longer, truncate
                    qv_str = qv_str[:len(v)]

                converted.append(qv_str)

            new_line = f"{key}=" + " ".join(converted) + "\n"
            new_lines.append(new_line)
        else:
            new_lines.append(line)  # ensure space before newline

    with open(out_path, "w") as f:
        f.writelines(new_lines)

def train_model(data_dir, model_type, dataset, max_trees, max_depth, alpha, seed=1, result_dir="./"):
    datasets={
        "breastcancer": ("breastcancer", "binary", 1),
        "kr-vs-kp": ("kr-vs-kp", "binary", 1),
        "covtype": ("covtype", "binary", 1),
        "mushroom": ("mushroom", "binary", 1),
        "california_housing": ("california_housing", "regression", 1),
        "kin8nm": ("kin8nm", "regression", 1),
        "wine": ("wine", "multiclass", 7),
        "covtype_multi": ("covtype_multi", "multiclass", 7)
    }
    if dataset in datasets:
        d, task, num_classes = datasets[dataset]
    else:
        raise ValueError(f"Dataset {dataset} not implemented.")
    result_file = os.path.join(result_dir, 'results.csv')
    if not os.path.exists(result_file):
        with open(result_file, "w") as f:
            f.write("model,dataset,max_trees,no_trees,depth,alpha,train_loss,test_accuracy,val_acc,nodes\n")

    data_dir = data_dir+f'{seed}'
    (X_train, y_train), (X_test, y_test), (X_val, y_val)= load_data(data_dir, dataset)
    if model_type == "lgbm_quant":
        if alpha != 0.0:
            return
        data = lgb.Dataset(X_train, label=y_train)
        model = lgb.train({'objective': task, 'max_depth': max_depth, 'num_trees': max_trees, 'num_classes': num_classes}, data)
        estimators = model.num_trees()
        train_score = evaluate_model(model, X_train, y_train, task)
        nodes = count_nodes(model)
        # already save results to enable quantization step
        test_acc = evaluate_model(model, X_test, y_test, task)
        val_accuracy = evaluate_model(model, X_val, y_val, task)

        with open(result_file, "a") as f:
            name = "lgbm_base"
            f.write(f"{name},{dataset},{max_trees},{estimators},{max_depth},{alpha},{train_score},{test_acc},{val_accuracy},{nodes}\n")

        # quantize
        model.save_model('model.txt')
        quantize('model.txt', 'model_quantized.txt', data_type="float16")
        model.model_from_string(open('model_quantized.txt').read())
        train_score = evaluate_model(model, X_train, y_train, task)

    elif model_type == "cegb":
        data = lgb.Dataset(X_train, label=y_train)
        # TODO: think about evaluating further parameters like cegb_tradeoff and different costs for features, e.g. binary vs. continuous
        model = lgb.train({'objective': task, 'max_depth': max_depth, 'num_trees': max_trees, 'num_classes': num_classes, 'cegb_penalty_feature_coupled': np.ones(X_train.shape[1]), 'cegb_tradeoff': 1.0, 'cegb_penalty_split': alpha}, data)
        estimators = model.num_trees()
        train_score = evaluate_model(model, X_train, y_train, task)
        nodes = count_nodes(model)
        test_acc = evaluate_model(model, X_test, y_test, task)
        val_accuracy = evaluate_model(model, X_val, y_val, task)

    elif model_type == "ccp":
        if task == "regression":
            model = GradientBoostingRegressor(n_estimators=max_trees, max_depth=max_depth, ccp_alpha=alpha)
        else:
            model = GradientBoostingClassifier(n_estimators=max_trees, max_depth=max_depth, ccp_alpha=alpha)
        model.fit(X_train, y_train)
        nodes = count_nodes(model)
        train_score = model.train_score_[-1]
        estimators = len(model.estimators_)
    else:
        # TODO: implement other models
        return

    test_acc = evaluate_model(model, X_test, y_test, task)
    val_accuracy = evaluate_model(model, X_val, y_val, task)

    # write in new line of csv file
    with open(result_file, "a") as f:
        f.write(f"{model_type},{dataset},{max_trees},{estimators},{max_depth},{alpha},{train_score},{test_acc},{val_accuracy},{nodes}\n")




def main():
    parser = argparse.ArgumentParser(description='Benchmark different tree models on datasets.')
    parser.add_argument('--datasets_dir', required=True, help='Directory to datasets.')
    parser.add_argument('--model', default="ccp", help='Model to train.')
    parser.add_argument('--dataset', default="breastcancer", help='Dataset to use.')
    parser.add_argument('--max_trees', type=int, default=10, help='Maximum number of trees.')
    parser.add_argument('--max_depth', type=int, default=5, help='Maximum depth of trees.')
    parser.add_argument('--alpha', type=float, default=0.0, help='Complexity parameter for pruning (ccp).')
    parser.add_argument('--result_dir', default="", help='File where results should be written to.')
    parser.add_argument('--randomseed', type=int, default=1, help='randomseedtouse')
    args = parser.parse_args()

    train_model(args.datasets_dir, args.model, args.dataset, args.max_trees, args.max_depth, args.alpha, seed=args.randomseed, result_dir=args.result_dir)

if __name__=="__main__":
    main()
