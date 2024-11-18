import os
import re 
import numpy as np
import matplotlib.pyplot as plt

import lightgbm as lgb
from sklearn.metrics import accuracy_score, roc_auc_score

def GetValueFromOut(filename, key):
	input = open(filename, "r")
	ret = 0.0
	for line in input.readlines():
		if key + ' :' in line:
			ret = float(line.split(key+' :')[-1])
	return ret

def GetValueFromTXT(filename, key, sum_up=False):
	input = open(filename, "r")
	ret = 0.0
	for line in input.readlines():
		if key + '=' in line:
			if sum_up:
				ret += float(line.split(key+'=')[-1])
			else:
				ret = float(line.split(key+'=')[-1])
		elif key + ': ' in line and key != 'num_leaves':
			if key == 'data':
				ret = line.split(key+': ')[-1][:-2]
			else:
				ret = float(line.split(key+': ')[-1][:-2])
	return ret

def calcAccuracy(model_path, data_path, classes=1):
	model = lgb.Booster(model_file=model_path)

	test_data = lgb.Dataset(data_path)
	test_data.construct()

	y_pred = model.predict(data_path, predict_disable_shape_check=True)

	if classes > 1:	
		roc_auc = roc_auc_score(test_data.get_label(), y_pred, multi_class='ovo')	
		accuracy = accuracy_score(test_data.get_label(), np.argmax(y_pred, axis=1))
	else:
		roc_auc = roc_auc_score(test_data.get_label(), y_pred)
		accuracy = accuracy_score(test_data.get_label(), (y_pred > 0.5).astype(int))
	
	return accuracy, roc_auc
 

def plotMetrics(keyword, log_scale=False):
	sorted_dir = sorted(os.listdir("../results"), key=lambda x: (int(x.split(".")[1]), int(x.split(".")[2])))
	setting_value = []
	accuracies = []
	logloss = []
	no_features = []
	no_thresholds = []
	no_leaves = []
	no_trees = []
	our_bits = []
	lgb_bits = []
	num_iterations = 0
	max_depth = 0
	tinygbdt_penalty_feature = 0
	tinygbdt_penalty_split = 0
	tinygbdt_forestsize = 0
	tinygbdt_precision = 0
	num_classes = 0
	data = ""

	for fn in sorted_dir:
		if fn.endswith(keyword+".out"):
			logloss.append(GetValueFromOut('../results/'+fn, 'logloss'))
			no_features.append(GetValueFromOut('../results/'+fn, '#features'))
			no_thresholds.append(GetValueFromOut('../results/'+fn, '#thresholds'))
			our_bits.append(GetValueFromOut('../results/'+fn, '#bits'))
		if fn.endswith(keyword+".txt"):
			no_trees.append(GetValueFromTXT('../results/'+fn, 'Tree'))
			setting_value.append(GetValueFromTXT('../results/'+fn, keyword))
			# no_features.append(GetValueFromTXT('../results/'+fn, 'tt_feature_count'))
			# no_thresholds.append(GetValueFromTXT('../results/'+fn, 'tt_threshold_count'))
			no_leaves.append(GetValueFromTXT('../results/'+fn, 'num_leaves', sum_up=True))
			lgb_bits.append(GetValueFromTXT('../results/'+fn, 'model_size', sum_up=True))
			num_iterations = GetValueFromTXT('../results/'+fn, 'num_iterations')
			max_depth =  GetValueFromTXT('../results/'+fn, 'max_depth')
			tinygbdt_penalty_feature =  GetValueFromTXT('../results/'+fn, 'tinygbdt_penalty_feature')
			tinygbdt_penalty_split =  GetValueFromTXT('../results/'+fn, 'tinygbdt_penalty_split')
			tinygbdt_forestsize =  GetValueFromTXT('../results/'+fn, 'tinygbdt_forestsize')
			tinygbdt_precision =  GetValueFromTXT('../results/'+fn, 'tinygbdt_precision')
			num_classes =  GetValueFromTXT('../results/'+fn, 'num_class')
			if num_classes > 1:
				accuracy, roc = calcAccuracy('../results/'+fn, '../covtype.test', classes=num_classes)
			else:
				accuracy, roc = calcAccuracy('../results/'+fn, '../covtype.libsvm.binary.test', classes=num_classes)
			accuracies.append(accuracy)	
			data = GetValueFromTXT('../results/'+fn, 'data')
		else:
			continue
	
	# lbg_bits = lgb_floats*32 + lgb_ints*16

	fig1, ax1 = plt.subplots()

	color = 'tab:red'
	ax1.set_xlabel(keyword)
	ax1.set_ylabel('Logloss')
	ax1.plot(setting_value, logloss, color=color, label='Logloss')
	ax1.plot(setting_value, accuracies, color='tab:purple', label='Accuracy')
	plt.legend(loc='lower center')
	ax1.tick_params(axis='y', labelcolor=color)

	ax2 = ax1.twinx()  # instantiate a second Axes that shares the same x-axis


	ax2.set_ylabel('count')  # we already handled the x-label with ax1
	if log_scale:
		ax2.set_yscale('log')
	# ax2.set_yscale('log')
	ax2.plot(setting_value, no_thresholds, label="no. thresholds")
	ax2.plot(setting_value, no_leaves, label="no. leaves")
	ax2.plot(setting_value, our_bits, color='tab:pink', label="no. bits")
	ax2.plot(setting_value, lgb_bits, color='tab:brown', label="no. bits LGBM")
	plt.legend(loc='lower right')

	color = 'tab:green'
	ax3 = ax1.twinx()  # instantiate a third Axes that shares the same x-axis
	ax3.tick_params(axis='y', labelcolor=color)
	ax3.plot(setting_value, no_features, label="no. features", color=color)

	fig1.tight_layout()  # otherwise the right y-label is slightly clipped
	plt.legend(loc='upper left')

	plt.savefig(
		'../plots/'+keyword
		+'_'+str(data)
		+'_maxtrees'+str(num_iterations)
		+'_maxdepth'+str(max_depth)
		+'_penF'+str(tinygbdt_penalty_feature)
		+'_penT'+str(tinygbdt_penalty_split)
		+ '_maxsize'+str(tinygbdt_forestsize)
		+'_precision'+str(tinygbdt_precision)
		+'_logscale'+str(log_scale)
		+'.png'
		)

	plt.show()

log_scale = False

plotMetrics('num_iterations', log_scale = log_scale)
plotMetrics('max_depth', log_scale = log_scale)
plotMetrics('tinygbdt_forestsize', log_scale = log_scale)
plotMetrics('tinygbdt_penalty_feature', log_scale = log_scale)
plotMetrics('tinygbdt_penalty_split', log_scale = log_scale)

