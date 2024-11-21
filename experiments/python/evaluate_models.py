import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import lightgbm as lgb
from sklearn.metrics import accuracy_score, roc_auc_score, mean_squared_error

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
			if key == 'objective':
				ret = line.split(key+'=')[-1]
			elif sum_up:
				ret += float(line.split(key+'=')[-1])
			else:
				ret = float(line.split(key+'=')[-1])
		elif key + ': ' in line and key != 'num_leaves':
			try:
				ret = float(line.split(key+': ')[-1][:-2])
			except:
				ret = line.split(key+': ')[-1][:-2]
	return ret

def calcAccuracy(model_path, data_path, classes=1, label_column=None):
	print(model_path)
	model = lgb.Booster(model_file=model_path)

	if data_path.endswith('.csv'):
		df = pd.read_csv(data_path, header=None)
		test_data = lgb.Dataset(df.iloc[:,:int(label_column)], label=df.iloc[:,int(label_column)], free_raw_data=False)
	else:
		test_data = lgb.Dataset(data_path, free_raw_data=False)
	test_data.construct()

	y_pred = model.predict(test_data.get_data(), predict_disable_shape_check=True)

	
	if classes == 0: # regression
		roc_auc = 0
		accuracy = mean_squared_error(test_data.get_label(), y_pred)
	elif classes > 1:	
		roc_auc = roc_auc_score(test_data.get_label(), y_pred, multi_class='ovo')	
		accuracy = accuracy_score(test_data.get_label(), np.argmax(y_pred, axis=1))
	else:
		roc_auc = roc_auc_score(test_data.get_label(), y_pred)
		accuracy = accuracy_score(test_data.get_label(), (y_pred > 0.5).astype(int))
	
	return accuracy, roc_auc
 

def plotMetrics(keyword, log_scale=False, dataset=None, dont_plot=False, get_baseline=True):
	print("Plotting: ", keyword)
	sorted_dir = sorted(os.listdir("../models"), key=lambda x: (float(x.split(".")[1]), float("0."+x.split(".")[2])))
	print(sorted_dir)
	setting_value = []
	accuracies = []
	logloss = []
	rmse = []
	no_features = []
	no_thresholds = []
	no_leaves = []
	no_trees = []
	our_bits = []
	lgb_bits = []
	tinygbdt_penalty_feature = []
	tinygbdt_penalty_split = []
	num_iterations = 0
	max_depth = 0
	# tinygbdt_penalty_feature = 0
	# tinygbdt_penalty_split = 0
	tinygbdt_forestsize = 0
	tinygbdt_precision = 0
	num_classes = 0
	objective = ""
	data = ""

	for fn in sorted_dir:
		if fn.endswith(keyword+".out") or (get_baseline and fn.endswith("baseline.out")):
			logloss.append(GetValueFromOut('../models/'+fn, 'logloss'))
			rmse.append(GetValueFromOut('../models/'+fn, 'rmse'))
			no_features.append(GetValueFromOut('../models/'+fn, '#features'))
			no_thresholds.append(GetValueFromOut('../models/'+fn, '#thresholds'))
			our_bits.append(GetValueFromOut('../models/'+fn, '#bits'))
		if fn.endswith(keyword+".txt") or (get_baseline and fn.endswith("baseline.txt")):
			no_trees.append(GetValueFromTXT('../models/'+fn, 'Tree'))
			setting_value.append(GetValueFromTXT('../models/'+fn, keyword))
			# no_features.append(GetValueFromTXT('../models/'+fn, 'tt_feature_count'))
			# no_thresholds.append(GetValueFromTXT('../models/'+fn, 'tt_threshold_count'))
			no_leaves.append(GetValueFromTXT('../models/'+fn, 'num_leaves', sum_up=True))
			lgb_bits.append(GetValueFromTXT('../models/'+fn, 'model_size', sum_up=True))
			num_iterations = GetValueFromTXT('../models/'+fn, 'num_iterations')
			max_depth =  GetValueFromTXT('../models/'+fn, 'max_depth')
			tinygbdt_penalty_feature.append(GetValueFromTXT('../models/'+fn, 'tinygbdt_penalty_feature'))
			tinygbdt_penalty_split.append(GetValueFromTXT('../models/'+fn, 'tinygbdt_penalty_split'))
			tinygbdt_forestsize =  GetValueFromTXT('../models/'+fn, 'tinygbdt_forestsize')
			tinygbdt_precision =  GetValueFromTXT('../models/'+fn, 'tinygbdt_precision')
			num_classes =  GetValueFromTXT('../models/'+fn, 'num_class')
			valid_data = GetValueFromTXT('../models/'+fn, 'valid')
			label_column = GetValueFromTXT('../models/'+fn, 'label_column')
			objective =  GetValueFromTXT('../models/'+fn, 'objective')
			if objective == 'multiclass':
				accuracy, roc = calcAccuracy('../models/'+fn, '../'+valid_data, classes=num_classes)
			elif objective == 'binary':
				accuracy, roc = calcAccuracy('../models/'+fn, '../'+valid_data, classes=num_classes)
			elif objective == 'regression':
				accuracy, roc = calcAccuracy('../models/'+fn, '../'+valid_data, classes=0, label_column=label_column)
			accuracies.append(accuracy)	
			data = GetValueFromTXT('../models/'+fn, 'data')
		else:
			continue
	
	# lbg_bits = lgb_floats*32 + lgb_ints*16
	# print(len(setting_value), len(no_trees), len(no_features), len(no_thresholds), len(no_leaves), len(our_bits), len(lgb_bits), len(logloss), len(rmse), len(accuracies))

	df = pd.DataFrame({
		keyword: setting_value,
		'no_trees': no_trees,
		'no_features': no_features,
		'no_thresholds': no_thresholds,
		'no_leaves': no_leaves,
		'our_bits': our_bits,
		'lgb_bits': lgb_bits,
		'logloss': logloss,
		'rmse': rmse,
		'accuracy': accuracies,
		'tinygbdt_penalty_feature': tinygbdt_penalty_feature,
		'tinygbdt_penalty_split': tinygbdt_penalty_split
	})

	df_filename = (keyword
			+'_'+str(objective)
			+'_'+str(data[5:])
			+'_penF'+str(tinygbdt_penalty_split[-1])
			+'_penT'+str(tinygbdt_penalty_split[-1])
			+'_maxtrees'+str(num_iterations)
			+'_maxdepth'+str(max_depth)
			+ '_maxsize'+str(tinygbdt_forestsize)
			+'_precision'+str(tinygbdt_precision)
			+'_logscale'+str(log_scale)
			+'.csv')
	
	df.to_csv('../results/'+
		df_filename
		, index=False
		)
	
	if not dont_plot:

		plt.ioff()

		fig1, ax1 = plt.subplots()

		color = 'tab:red'
		ax1.set_xlabel(keyword)
		if log_scale:
		# 	ax2.set_yscale('log')
			ax1.set_xscale('log')	
		if len(logloss) > 0:
			if logloss[-1] != 0:
				ax1.set_ylabel('Logloss')
				ax1.plot(setting_value, logloss, color=color, label='Logloss')
		if len(rmse) > 0:
			if rmse[-1] != 0:
				ax1.set_ylabel('RMSE')
				ax1.plot(setting_value, rmse, color=color, label='RMSE')
		ax1.plot(setting_value, accuracies, color='tab:purple', label='Accuracy/MSE')
		plt.legend(loc='lower center')
		ax1.tick_params(axis='y', labelcolor=color)
		print(setting_value)

		ax2 = ax1.twinx()  # instantiate a second Axes that shares the same x-axis


		ax2.set_ylabel('count')  # we already handled the x-label with ax1
		# if log_scale:
		# 	ax2.set_yscale('log')
		# ax2.set_yscale('log')
		ax2.plot(setting_value, no_thresholds, label="no. thresholds")
		ax2.plot(setting_value, no_leaves, label="no. leaves")
		plt.legend(loc='lower left')
		

		ax4 = ax1.twinx()  # instantiate a second Axes that shares the same x-axis
		ax4.yaxis.set_label_position("left")
		ax4.yaxis.tick_left()
		ax4.set_ylabel('bit count')
		ax4.plot(setting_value, our_bits, color='tab:pink', label="no. bits")
		ax4.plot(setting_value, lgb_bits, color='tab:brown', label="no. bits LGBM")
		plt.legend(loc='lower right')


		color = 'tab:green'
		ax3 = ax1.twinx()  # instantiate a third Axes that shares the same x-axis
		ax3.tick_params(axis='y', labelcolor=color)
		ax3.plot(setting_value, no_features, label="no. features", color=color)

		fig1.tight_layout()  # otherwise the right y-label is slightly clipped
		plt.legend(loc='upper left')

		plt.savefig(
			'../plots/'+keyword
			+'_'+str(data[5:])
			+'_penF'+str(tinygbdt_penalty_feature[-1])
			+'_penT'+str(tinygbdt_penalty_split[-1])
			+'_maxtrees'+str(num_iterations)
			+'_maxdepth'+str(max_depth)
			+ '_maxsize'+str(tinygbdt_forestsize)
			+'_precision'+str(tinygbdt_precision)
			+'_logscale'+str(log_scale)
			+'.png'
			)

		plt.show()
	
	return df_filename

log_scale = False

# TODO: value at x=0 goes to -inf because of log scale
def plotAccuracyByPenalty(dataframe_filename, keyword, plot_accuracy=True, plot_nodeLeafCount=False, xlog=True, xlabel='penalty'):
	print(dataframe_filename)
	df = pd.read_csv('../results/'+dataframe_filename)

	fig1, ax1 = plt.subplots()

	if xlabel == 'Feature Penalty' or xlabel == 'Both penalties':
		keyword = 'tinygbdt_penalty_feature'
	if xlabel == 'Threshold Penalty':
		keyword = 'tinygbdt_penalty_split'

	# color = 'tab:red'
	ax1.set_xlabel(xlabel)
	if xlog:
		ax1.set_xscale('log')

	if plot_accuracy:
		color='tab:orange'
		if df['logloss'].iloc[1] == 0.0:
			label='RMSE'
		else:
			label='Accuracy'
		ax1.plot(df[keyword], df['accuracy'], '--o', color=color, label=label)
		locs, labels = plt.xticks()

		ax1.set_ylabel(label)
		ax1.tick_params(axis='y', labelcolor=color)
		plt.legend(loc='lower left')
	# ax1.tick_params(axis='y', labelcolor=color)

	ax2 = ax1.twinx()  # instantiate a second Axes that shares the same x-axis
	ax2.set_ylabel('Count')  
	
	if xlabel == 'Feature Penalty':
		color = 'tab:green'
		ax2.plot(df[keyword], df['no_features'], 'o--', label="Features", color=color)
	if xlabel == 'Threshold Penalty':
		color = 'tab:blue'
		ax2.plot(df[keyword], df['no_thresholds'], 'o--', label="# thresholds and leaf values", color=color)
		if plot_nodeLeafCount:
			ax2.plot(df[keyword], (df['no_leaves']*2-1), 'o--', label="# nodes and leaves", color='tab:red')
			ax1.plot(df[keyword], ((df['no_leaves']*2-1)/df['no_thresholds']), 'o--', label="reuse factor", color='tab:green')

	plt.legend()

	fig1.tight_layout()  # otherwise the right y-label is slightly clipped

	plt.savefig(
		'../plots/'+'AccBY'+dataframe_filename[:-4]+'.png'
		)

	plt.show()

def plot_memories():
	lgbm_df_path = plotMetrics('num_iterations', dont_plot=True)
	tinygbdt_df_path = plotMetrics('0.tinygbdt_forestsize', dont_plot=True)
	tinygbdt_penalty_df_path = plotMetrics('penalties.1.tinygbdt_forestsize', dont_plot=True)

	lgbm_df = pd.read_csv('../results/'+lgbm_df_path)
	tinygbdt_df = pd.read_csv('../results/'+tinygbdt_df_path)
	tinygbdt_penalty_df = pd.read_csv('../results/'+tinygbdt_penalty_df_path)

	x = ["1KB", "8KB", "32KB"]
	# create an index for each tick position
	xi = list(range(len(x)))
	# TODO: make baseline model evaluation plotMetrics() parameter instead of starting at value 1
	plt.plot(xi, lgbm_df['accuracy'][1:], marker='o', linestyle='--', color='r', label='Default LightGBM') 
	plt.plot(xi, tinygbdt_df['accuracy'][1:], marker='o', linestyle='--', color='b', label='ToD Compression')
	plt.plot(xi, tinygbdt_penalty_df['accuracy'][1:], marker='o', linestyle='--', color='g', label='ToD Compression with Penalty')
	plt.xlabel('Memory')
	plt.ylabel('Accuracy') 
	plt.xticks(xi, x)
	plt.legend() 
	plt.savefig(
		'../plots/'+'modeltypes_bymemory_'+x[0]+x[1]+x[2]+'.png'
		)
	# plt.tight_layout()
	plt.show()

# plot_memories()

# plotMetrics('num_iterations', get_baseline=False)
# # plotMetrics('max_depth', log_scale = log_scale)
# plotMetrics('0.tinygbdt_forestsize', get_baseline=False)
# plotMetrics('1.tinygbdt_forestsize', get_baseline=False)
fp_df_path = plotMetrics('tinygbdt_penalty_feature', log_scale = True)
tp_df_path = plotMetrics('tinygbdt_penalty_split', log_scale = True)
both_df_path = plotMetrics('tinygbdt_penalty_feature', log_scale = True)

plot_nodeLeafCount = True
plotAccuracyByPenalty(fp_df_path, 'tinygbdt_penalty_feature', xlog=True, xlabel='Feature Penalty', plot_nodeLeafCount=plot_nodeLeafCount)
plotAccuracyByPenalty(tp_df_path, 'tinygbdt_penalty_split', xlog=True, xlabel='Threshold Penalty', plot_nodeLeafCount=plot_nodeLeafCount)
plotAccuracyByPenalty(both_df_path, 'bothpenalties.tinygbdt_penalty_split', xlog=True, xlabel='Both penalties', plot_nodeLeafCount=plot_nodeLeafCount)


