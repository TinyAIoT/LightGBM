import onnxruntime
import lightgbm as lgb
import matplotlib.pyplot as plt
from sklearn.datasets import load_svmlight_file
import sklearn.ensemble
import onnxmltools
import fastinference.Loader

# load lightgbm tree booster from txt file
booster = lgb.Booster(model_file='C:/Users/Jan Stenkamp/Documents/Arbeit/Boosted Trees/code/win/LightGBM/experiments/models/covtype/data-covtypems-64000-fp-0.03125-tp-0.03125-tree-5-depth-3.txt')
# booster = lgb.Booster(model_file='C:/Users/Jan Stenkamp/Documents/Arbeit/Boosted Trees/code/win/LightGBM/experiments/models/california_housing/data-california_housingms-64000-fp-1.0-tp-32.0-tree-5-depth-3.txt')
# dump = booster.dump_model()

# import json
# with open('model.json', 'w') as fp:
#     json.dump(dump, fp)

# convert to onnx
# TODO: what does this type do? FloatTensorType([None, 54]): first dimension is batch size, second dimension is number of features?
# onnx_model = onnxmltools.convert_lightgbm(booster, initial_types=[('float_input', onnxmltools.convert.common.data_types.FloatTensorType([None, 54]))])
# onnxmltools.utils.save_model(onnx_model, 'model.onnx')

X_train, y_train = load_svmlight_file('C:/Users/Jan Stenkamp/Documents/Arbeit/Boosted Trees/code/win/LightGBM/experiments/data/breastcancer.train')

# skmodel = lgb.LGBMClassifier(predict_disable_shape_check=True)
# skmodel.fit(X_train, y_train, init_model=booster)#, predict_disable_shape_check=True)
skmodel = sklearn.ensemble.GradientBoostingClassifier(init='zero')
# TODO: try HistGradientBoostingClassifier -> probably not supported by fastinference model loader 
skmodel.fit(X_train, y_train)

# load libsvm data for training as numpy array
X_test, y_test = load_svmlight_file('C:/Users/Jan Stenkamp/Documents/Arbeit/Boosted Trees/code/win/LightGBM/experiments/data/breastcancer.test')

print(skmodel.predict(X_test))
print(y_test)

# ensemble = fastinference.Loader.model_from_sklearn(skmodel)
# ensemble = fastinference.Loader.model_from_sklearn(skmodel, name="model", accuracy=None)
ensemble = fastinference.Loader.model_from_sklearn(skmodel, name="model", accuracy=None)
