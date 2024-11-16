#include <vector>
namespace LightGBM {
double PredictTree0(const double* arr) { 
  const std::vector<uint32_t> cat_threshold = {};
  double fval = 0.0f;
  fval = arr[3];
  if (std::isnan(fval))
    fval = 0.0;
  if (fval <= 1.3215000000000001) {
    fval = arr[3];
    if (std::isnan(fval))
      fval = 0.0;
    if (fval <= 0.67850000000000021) {
      fval = arr[2];
        if (std::isnan(fval))
          fval = 0.0;
        if (fval <= 1.0050000000000001) {
          return 0.13613284176676857;
        } else {
          return 0.18374629883871124;
        }
      } else {
        fval = arr[3];
        if (std::isnan(fval))
          fval = 0.0;
        if (fval <= 0.97250000000000003) {
           return 0.1843627934650568;
        } else {
          return 0.1558119197516;
        }
      }
   } else {
    fval = arr[2];
    if (std::isnan(fval))
      fval = 0.0;
  if (fval <= -0.46349999999999997) {
    fval = arr[1];
  if (std::isnan(fval))
    fval = 0.0;
  if (fval <= 0.91850000000000021) {
    return 0.15512928476442844;
   } else {
     return 0.088782415049715693;
   }
  } else {
    fval = arr[1];
    if (std::isnan(fval))
      fval = 0.0;
  if (fval <= 1.3590000000000002) {
    return 0.086502383304101732;
   } else {
     return 0.14477503138758252;
   }
  }
  }
}
double PredictTree0ByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};
  double fval = 0.0f;
   fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.3215000000000001) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.67850000000000021) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.0050000000000001) {return 0.13613284176676857;
   } else { return 0.18374629883871124;
   } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.97250000000000003) {return 0.1843627934650568;
   } else { return 0.1558119197516;
   } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= -0.46349999999999997) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.91850000000000021) {return 0.15512928476442844;
   } else { return 0.088782415049715693;
   } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.3590000000000002) {return 0.086502383304101732;
   } else { return 0.14477503138758252;
   } } } }

double PredictTree1(const double* arr) { const std::vector<uint32_t> cat_threshold = {};
  double fval = 0.0f;
   fval = arr[2];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= -1.3464999999999996) {fval = arr[0];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.58350000000000002) {fval = arr[1];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.29350000000000004) {return 0.00082984523989101217;
   } else { return -0.052335946519671106;
   } } else { fval = arr[0];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.69550000000000012) {return 0.09805080037907915;
   } else { return 0.032463116421055802;
   } } } else { fval = arr[2];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.37600000000000006) {fval = arr[0];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.7210000000000003) {return -0.0074916630638941096;
   } else { return -0.05672408094758026;
   } } else { fval = arr[1];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= -0.38749999999999996) {return -0.018255171237935786;
   } else { return 0.020890315426783553;
   } } } }
double PredictTree1ByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};
  double fval = 0.0f;
   fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= -1.3464999999999996) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.58350000000000002) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.29350000000000004) {return 0.00082984523989101217;
   } else { return -0.052335946519671106;
   } } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.69550000000000012) {return 0.09805080037907915;
   } else { return 0.032463116421055802;
   } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.37600000000000006) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.7210000000000003) {return -0.0074916630638941096;
   } else { return -0.05672408094758026;
   } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= -0.38749999999999996) {return -0.018255171237935786;
   } else { return 0.020890315426783553;
   } } } }

double PredictTree2(const double* arr) { const std::vector<uint32_t> cat_threshold = {};
  double fval = 0.0f;
   fval = arr[3];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.3215000000000001) {fval = arr[3];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.67850000000000021) {fval = arr[1];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.3590000000000002) {return -0.0084696669610969891;
   } else { return 0.045993109842173252;
   } } else { fval = arr[3];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.97250000000000003) {return 0.030819771458572565;
   } else { return 0.0049186127663863009;
   } } } else { fval = arr[3];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.6275000000000002) {fval = arr[0];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.95350000000000013) {return -0.034635369362649576;
   } else { return 0.0079729946037441126;
   } } else { fval = arr[0];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.44450000000000006) {return -0.0032959361707692171;
   } else { return -0.058916426411046476;
   } } } }
double PredictTree2ByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};
  double fval = 0.0f;
   fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.3215000000000001) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.67850000000000021) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.3590000000000002) {return -0.0084696669610969891;
   } else { return 0.045993109842173252;
   } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.97250000000000003) {return 0.030819771458572565;
   } else { return 0.0049186127663863009;
   } } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.6275000000000002) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.95350000000000013) {return -0.034635369362649576;
   } else { return 0.0079729946037441126;
   } } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.44450000000000006) {return -0.0032959361707692171;
   } else { return -0.058916426411046476;
   } } } }

double (*PredictTreePtr[])(const double*) = { PredictTree0 , PredictTree1 , PredictTree2 };
  

void GBDT::PredictRaw(const double* features, double *output, const PredictionEarlyStopInstance* early_stop) const {
	int early_stop_round_counter = 0;
  
	std::memset(output, 0, sizeof(double) * num_tree_per_iteration_);
  
	for (int i = 0; i < num_iteration_for_pred_; ++i) {
		for (int k = 0; k < num_tree_per_iteration_; ++k) {
		  output[k] += (*PredictTreePtr[i * num_tree_per_iteration_ + k])(features);
		}
		++early_stop_round_counter;
  
		if (early_stop->round_period == early_stop_round_counter) {
			if (early_stop->callback_function(output, num_tree_per_iteration_))
				return;
			early_stop_round_counter = 0;
		}
	}
}

double (*PredictTreeByMapPtr[])(const std::unordered_map<int, double>&) = { PredictTree0ByMap , PredictTree1ByMap , PredictTree2ByMap };
  

void GBDT::PredictRawByMap(const std::unordered_map<int, double>& features, double* output, const PredictionEarlyStopInstance* early_stop) const {
	int early_stop_round_counter = 0;
  
	std::memset(output, 0, sizeof(double) * num_tree_per_iteration_);
  
	for (int i = 0; i < num_iteration_for_pred_; ++i) {
		for (int k = 0; k < num_tree_per_iteration_; ++k) {
			output[k] += (*PredictTreeByMapPtr[i * num_tree_per_iteration_ + k])(features);
		}
		++early_stop_round_counter;
  
		if (early_stop->round_period == early_stop_round_counter) {
			if (early_stop->callback_function(output, num_tree_per_iteration_))
				return;
			early_stop_round_counter = 0;
		}
	}
}

void GBDT::Predict(const double* features, double *output, const PredictionEarlyStopInstance* early_stop) const {
	PredictRaw(features, output, early_stop);
  
	if (average_output_) {
		for (int k = 0; k < num_tree_per_iteration_; ++k) {
			output[k] /= num_iteration_for_pred_;
		}
	}
	if (objective_function_ != nullptr) {
		objective_function_->ConvertOutput(output, output);
	}
}

void GBDT::PredictByMap(const std::unordered_map<int, double>& features, double* output, const PredictionEarlyStopInstance* early_stop) const {
	PredictRawByMap(features, output, early_stop);
  
	if (average_output_) {
		for (int k = 0; k < num_tree_per_iteration_; ++k) {
			output[k] /= num_iteration_for_pred_;
		}
	}
	if (objective_function_ != nullptr) {
		objective_function_->ConvertOutput(output, output);
  
	}
}

double PredictTree0Leaf(const double* arr) { const std::vector<uint32_t> cat_threshold = {};
  double fval = 0.0f;
   fval = arr[3];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.3215000000000001) {fval = arr[3];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.67850000000000021) {fval = arr[2];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.0050000000000001) {return 0;
   } else { return 4;
   } } else { fval = arr[3];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.97250000000000003) {return 3;
   } else { return 5;
   } } } else { fval = arr[2];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= -0.46349999999999997) {fval = arr[1];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.91850000000000021) {return 1;
   } else { return 6;
   } } else { fval = arr[1];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.3590000000000002) {return 2;
   } else { return 7;
   } } } }
double PredictTree0LeafByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};
  double fval = 0.0f;
   fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.3215000000000001) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.67850000000000021) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.0050000000000001) {return 0;
   } else { return 4;
   } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.97250000000000003) {return 3;
   } else { return 5;
   } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= -0.46349999999999997) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.91850000000000021) {return 1;
   } else { return 6;
   } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.3590000000000002) {return 2;
   } else { return 7;
   } } } }

double PredictTree1Leaf(const double* arr) { const std::vector<uint32_t> cat_threshold = {};
  double fval = 0.0f;
   fval = arr[2];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= -1.3464999999999996) {fval = arr[0];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.58350000000000002) {fval = arr[1];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.29350000000000004) {return 0;
   } else { return 7;
   } } else { fval = arr[0];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.69550000000000012) {return 2;
   } else { return 6;
   } } } else { fval = arr[2];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.37600000000000006) {fval = arr[0];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.7210000000000003) {return 1;
   } else { return 5;
   } } else { fval = arr[1];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= -0.38749999999999996) {return 3;
   } else { return 4;
   } } } }
double PredictTree1LeafByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};
  double fval = 0.0f;
   fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= -1.3464999999999996) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.58350000000000002) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.29350000000000004) {return 0;
   } else { return 7;
   } } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.69550000000000012) {return 2;
   } else { return 6;
   } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.37600000000000006) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.7210000000000003) {return 1;
   } else { return 5;
   } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= -0.38749999999999996) {return 3;
   } else { return 4;
   } } } }

double PredictTree2Leaf(const double* arr) { const std::vector<uint32_t> cat_threshold = {};
  double fval = 0.0f;
   fval = arr[3];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.3215000000000001) {fval = arr[3];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.67850000000000021) {fval = arr[1];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.3590000000000002) {return 0;
   } else { return 3;
   } } else { fval = arr[3];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.97250000000000003) {return 2;
   } else { return 4;
   } } } else { fval = arr[3];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.6275000000000002) {fval = arr[0];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.95350000000000013) {return 1;
   } else { return 6;
   } } else { fval = arr[0];
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.44450000000000006) {return 5;
   } else { return 7;
   } } } }
double PredictTree2LeafByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};
  double fval = 0.0f;
   fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.3215000000000001) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.67850000000000021) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.3590000000000002) {return 0;
   } else { return 3;
   } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.97250000000000003) {return 2;
   } else { return 4;
   } } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 1.6275000000000002) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.95350000000000013) {return 1;
   } else { return 6;
   } } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;
  if (std::isnan(fval)) fval = 0.0;
  if (fval <= 0.44450000000000006) {return 5;
   } else { return 7;
   } } } }

double (*PredictTreeLeafPtr[])(const double*) = { PredictTree0Leaf , PredictTree1Leaf , PredictTree2Leaf };
  

void GBDT::PredictLeafIndex(const double* features, double *output) const {
	int total_tree = num_iteration_for_pred_ * num_tree_per_iteration_;
	for (int i = 0; i < total_tree; ++i) {
		output[i] = (*PredictTreeLeafPtr[i])(features);
	}
}
double (*PredictTreeLeafByMapPtr[])(const std::unordered_map<int, double>&) = { PredictTree0LeafByMap , PredictTree1LeafByMap , PredictTree2LeafByMap };
  

void GBDT::PredictLeafIndexByMap(const std::unordered_map<int, double>& features, double* output) const {
	int total_tree = num_iteration_for_pred_ * num_tree_per_iteration_;
  
	for (int i = 0; i < total_tree; ++i) {
		output[i] = (*PredictTreeLeafByMapPtr[i])(features);
	}
}
}  // namespace LightGBM

#else
#include "gbdt.h"
#include <LightGBM/utils/common.h>
#include <LightGBM/objective_function.h>
#include <LightGBM/metric.h>
#include <LightGBM/prediction_early_stop.h>
#include <ctime>
#include <sstream>
#include <chrono>
#include <string>
#include <vector>
#include <utility>
namespace LightGBM {
double PredictTree0(const double* arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3215000000000001) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.67850000000000021) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0050000000000001) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {return 0.16463120630842426; } else { return 0.12941770989201062; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return 0.13051987325015743; } else { return 0.2150988508977224; } } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {return 0.19412755787311264; } else { return 0.11770766250571899; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 0.12037714066750925; } else { return 0.16846719799591814; } } } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.46349999999999997) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.91850000000000021) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {return 0.17989320742405163; } else { return 0.13166872645531175; } } else { return 0.088782415049715693; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return 0.065417075149327653; } else { return 0.10896282025157844; } } else { return 0.14477503138758252; } } } }
double PredictTree0ByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3215000000000001) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.67850000000000021) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0050000000000001) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {return 0.16463120630842426; } else { return 0.12941770989201062; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return 0.13051987325015743; } else { return 0.2150988508977224; } } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {return 0.19412755787311264; } else { return 0.11770766250571899; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 0.12037714066750925; } else { return 0.16846719799591814; } } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.46349999999999997) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.91850000000000021) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {return 0.17989320742405163; } else { return 0.13166872645531175; } } else { return 0.088782415049715693; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return 0.065417075149327653; } else { return 0.10896282025157844; } } else { return 0.14477503138758252; } } } }

double PredictTree1(const double* arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.58350000000000002) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.29350000000000004) {return 0.0003602127303862756; } else { return -0.053095989380366908; } } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.69550000000000012) {return 0.096880283065025274; } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.7210000000000003) {return 0.019644546475441487; } else { return 0.073984191485800793; } } } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.37600000000000006) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.7210000000000003) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {return -0.0022890488501028238; } else { return -0.027108552484686008; } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.46349999999999997) {return -0.024202108029286871; } else { return -0.090411095174611919; } } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.58350000000000002) {return -0.059254456922979162; } else { return -0.0056641278744428416; } } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.81950000000000001) {return -0.0013526024368063876; } else { return 0.036037325632524951; } } } } }
double PredictTree1ByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.58350000000000002) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.29350000000000004) {return 0.0003602127303862756; } else { return -0.053095989380366908; } } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.69550000000000012) {return 0.096880283065025274; } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.7210000000000003) {return 0.019644546475441487; } else { return 0.073984191485800793; } } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.37600000000000006) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.7210000000000003) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {return -0.0022890488501028238; } else { return -0.027108552484686008; } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.46349999999999997) {return -0.024202108029286871; } else { return -0.090411095174611919; } } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.58350000000000002) {return -0.059254456922979162; } else { return -0.0056641278744428416; } } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.81950000000000001) {return -0.0013526024368063876; } else { return 0.036037325632524951; } } } } }

double PredictTree2(const double* arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3215000000000001) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.67850000000000021) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {return 0.0039831947685073973; } else { return -0.019538184235772652; } } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.81950000000000001) {return 0.028535675382039119; } else { return 0.059081083526932511; } } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {return 0.039705559542200224; } else { return -0.029461628465378177; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {return -0.014001625666722037; } else { return 0.023517688702393843; } } } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.81950000000000001) {return -0.026872711955790426; } else { return -0.0662771696502618; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {return 0.02633999584966917; } else { return -0.011990486116195832; } } } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.44450000000000006) {return -0.0014685800564293713; } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.58350000000000002) {return -0.13669744813079715; } else { return -0.043876779396146023; } } } } }
double PredictTree2ByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3215000000000001) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.67850000000000021) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {return 0.0039831947685073973; } else { return -0.019538184235772652; } } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.81950000000000001) {return 0.028535675382039119; } else { return 0.059081083526932511; } } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {return 0.039705559542200224; } else { return -0.029461628465378177; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {return -0.014001625666722037; } else { return 0.023517688702393843; } } } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.81950000000000001) {return -0.026872711955790426; } else { return -0.0662771696502618; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {return 0.02633999584966917; } else { return -0.011990486116195832; } } } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.44450000000000006) {return -0.0014685800564293713; } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.58350000000000002) {return -0.13669744813079715; } else { return -0.043876779396146023; } } } } }

double PredictTree3(const double* arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3215000000000001) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.67850000000000021) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0050000000000001) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 0.013615393134442478; } else { return -0.020151675428117112; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return -0.015684367311432492; } else { return 0.056614337457799813; } } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {return 0.035894028799261533; } else { return -0.026472137114284568; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return -0.024507959075333929; } else { return 0.014925238109953909; } } } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.46349999999999997) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.91850000000000021) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {return 0.02799551487347875; } else { return -0.011520749150309357; } } else { return -0.049580358624934526; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return -0.071032938731476564; } else { return -0.034224477613582126; } } else { return -0.0011536042643459248; } } } }
double PredictTree3ByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3215000000000001) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.67850000000000021) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0050000000000001) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 0.013615393134442478; } else { return -0.020151675428117112; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return -0.015684367311432492; } else { return 0.056614337457799813; } } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {return 0.035894028799261533; } else { return -0.026472137114284568; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return -0.024507959075333929; } else { return 0.014925238109953909; } } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.46349999999999997) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.91850000000000021) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {return 0.02799551487347875; } else { return -0.011520749150309357; } } else { return -0.049580358624934526; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return -0.071032938731476564; } else { return -0.034224477613582126; } } else { return -0.0011536042643459248; } } } }

double PredictTree4(const double* arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3215000000000001) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.67850000000000021) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0050000000000001) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.44450000000000006) {return 0.036268332557411034; } else { return -0.015432015801802321; } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.35150000000000003) {return 0.063420407732955666; } else { return 0.013432399642247917; } } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {return 0.015220000413674776; } else { return 0.037329446754014013; } } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.1035000000000001) {return 0.01230790139029753; } else { return -0.016907153965805447; } } } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3445000000000003) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {return -0.016608695564214345; } else { return 0.035629760784563994; } } else { return -0.039490803452157025; } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return -0.060047176723865517; } else { return -0.0069944017917369207; } } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.69550000000000012) {return -0.040638511276661488; } else { return -0.085762450665229584; } } } } }
double PredictTree4ByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3215000000000001) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.67850000000000021) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0050000000000001) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.44450000000000006) {return 0.036268332557411034; } else { return -0.015432015801802321; } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.35150000000000003) {return 0.063420407732955666; } else { return 0.013432399642247917; } } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {return 0.015220000413674776; } else { return 0.037329446754014013; } } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.1035000000000001) {return 0.01230790139029753; } else { return -0.016907153965805447; } } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3445000000000003) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {return -0.016608695564214345; } else { return 0.035629760784563994; } } else { return -0.039490803452157025; } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return -0.060047176723865517; } else { return -0.0069944017917369207; } } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.69550000000000012) {return -0.040638511276661488; } else { return -0.085762450665229584; } } } } }

double PredictTree5(const double* arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.52550000000000019) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.35150000000000003) {return 0.039635303116057466; } else { return -0.01643199424832973; } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.37600000000000006) {return -0.047311956542047076; } else { return 0.029076011014951664; } } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {return 0.036746013179469669; } else { return 0.011787644270851943; } } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.7210000000000003) {return 0.0040114333185465667; } else { return -0.039298930184943862; } } } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.86649999999999994) {return -0.01238649248322294; } else { return 0.028064700654757604; } } else { return -0.011776204334883047; } } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.69550000000000012) {return -0.06844921811938201; } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {return -0.12129750663997976; } else { return -0.079583001410180543; } } } } }
double PredictTree5ByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.52550000000000019) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.35150000000000003) {return 0.039635303116057466; } else { return -0.01643199424832973; } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.37600000000000006) {return -0.047311956542047076; } else { return 0.029076011014951664; } } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {return 0.036746013179469669; } else { return 0.011787644270851943; } } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.7210000000000003) {return 0.0040114333185465667; } else { return -0.039298930184943862; } } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.86649999999999994) {return -0.01238649248322294; } else { return 0.028064700654757604; } } else { return -0.011776204334883047; } } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.69550000000000012) {return -0.06844921811938201; } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {return -0.12129750663997976; } else { return -0.079583001410180543; } } } } }

double PredictTree6(const double* arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.52550000000000019) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.37600000000000006) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {return 0.01176088358130095; } else { return -0.021664605054192765; } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.35150000000000003) {return 0.022291081207991132; } else { return -0.007089378621555154; } } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.91850000000000021) {return 0.019006549965627999; } else { return -0.0065311726097844122; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return -0.017244264416826392; } else { return 0.010715348653688164; } } } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 0.024667561317552572; } else { return -0.058443150334739916; } } else { return 0.036934602676187867; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return -0.094155372742663432; } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return -0.021051892519011167; } else { return -0.099806949144537291; } } } } }
double PredictTree6ByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.52550000000000019) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.37600000000000006) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {return 0.01176088358130095; } else { return -0.021664605054192765; } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.35150000000000003) {return 0.022291081207991132; } else { return -0.007089378621555154; } } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.91850000000000021) {return 0.019006549965627999; } else { return -0.0065311726097844122; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return -0.017244264416826392; } else { return 0.010715348653688164; } } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 0.024667561317552572; } else { return -0.058443150334739916; } } else { return 0.036934602676187867; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return -0.094155372742663432; } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return -0.021051892519011167; } else { return -0.099806949144537291; } } } } }

double PredictTree7(const double* arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.52550000000000019) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.37600000000000006) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {return 0.010593900126234833; } else { return -0.019486258782518119; } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.35150000000000003) {return 0.020119037076877812; } else { return -0.0063762961157063577; } } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3215000000000001) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {return 0.012123450003548442; } else { return -0.013013855068258504; } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {return 0.0056466368704490132; } else { return -0.023232333750476102; } } } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 0.022215685895858577; } else { return -0.052563937673530008; } } else { return 0.033259200693294036; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return -0.085567822488160847; } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return -0.018996667631956031; } else { return -0.09054086732558439; } } } } }
double PredictTree7ByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.52550000000000019) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.37600000000000006) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {return 0.010593900126234833; } else { return -0.019486258782518119; } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.35150000000000003) {return 0.020119037076877812; } else { return -0.0063762961157063577; } } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3215000000000001) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {return 0.012123450003548442; } else { return -0.013013855068258504; } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {return 0.0056466368704490132; } else { return -0.023232333750476102; } } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 0.022215685895858577; } else { return -0.052563937673530008; } } else { return 0.033259200693294036; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return -0.085567822488160847; } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return -0.018996667631956031; } else { return -0.09054086732558439; } } } } }

double PredictTree8(const double* arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.29350000000000004) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.1455000000000002) {return 0.054330181816411909; } else { return -0.020398544414867326; } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.81500000000000006) {return -0.021770488589339422; } else { return 0.0032867559595745584; } } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.29350000000000004) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.46349999999999997) {return 0.004916108930527738; } else { return -0.0099471891777270661; } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0050000000000001) {return 0.0025793697401086204; } else { return 0.03910259857066576; } } } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 0.020011661530788434; } else { return -0.047351996577623734; } } else { return 0.029966278168876162; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return -0.078005312322232304; } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return -0.017141067179613789; } else { return -0.082444597034502284; } } } } }
double PredictTree8ByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.29350000000000004) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.1455000000000002) {return 0.054330181816411909; } else { return -0.020398544414867326; } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.81500000000000006) {return -0.021770488589339422; } else { return 0.0032867559595745584; } } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.29350000000000004) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.46349999999999997) {return 0.004916108930527738; } else { return -0.0099471891777270661; } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0050000000000001) {return 0.0025793697401086204; } else { return 0.03910259857066576; } } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 0.020011661530788434; } else { return -0.047351996577623734; } } else { return 0.029966278168876162; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return -0.078005312322232304; } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return -0.017141067179613789; } else { return -0.082444597034502284; } } } } }

double PredictTree9(const double* arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.52550000000000019) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.37600000000000006) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {return 0.0082501750114474543; } else { return -0.017498708925320232; } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.35150000000000003) {return 0.017970524861225422; } else { return -0.0059631659405114416; } } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.29350000000000004) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.46349999999999997) {return 0.018863846833872135; } else { return -0.011090470740368107; } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.86649999999999994) {return -0.014923340955332402; } else { return 0.022631404811595039; } } } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 0.018028732682257558; } else { return -0.042705982561566463; } } else { return 0.027009847505253107; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return -0.071263401191998574; } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return -0.015465314192416492; } else { return -0.075270458649968772; } } } } }
double PredictTree9ByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.52550000000000019) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.37600000000000006) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {return 0.0082501750114474543; } else { return -0.017498708925320232; } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.35150000000000003) {return 0.017970524861225422; } else { return -0.0059631659405114416; } } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.29350000000000004) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.46349999999999997) {return 0.018863846833872135; } else { return -0.011090470740368107; } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.86649999999999994) {return -0.014923340955332402; } else { return 0.022631404811595039; } } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 0.018028732682257558; } else { return -0.042705982561566463; } } else { return 0.027009847505253107; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return -0.071263401191998574; } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return -0.015465314192416492; } else { return -0.075270458649968772; } } } } }

double (*PredictTreePtr[])(const double*) = { PredictTree0 , PredictTree1 , PredictTree2 , PredictTree3 , PredictTree4 , PredictTree5 , PredictTree6 , PredictTree7 , PredictTree8 , PredictTree9 };

void GBDT::PredictRaw(const double* features, double *output, const PredictionEarlyStopInstance* early_stop) const {
	int early_stop_round_counter = 0;
	std::memset(output, 0, sizeof(double) * num_tree_per_iteration_);
	for (int i = 0; i < num_iteration_for_pred_; ++i) {
		for (int k = 0; k < num_tree_per_iteration_; ++k) {
			output[k] += (*PredictTreePtr[i * num_tree_per_iteration_ + k])(features);
		}
		++early_stop_round_counter;
		if (early_stop->round_period == early_stop_round_counter) {
			if (early_stop->callback_function(output, num_tree_per_iteration_))
				return;
			early_stop_round_counter = 0;
		}
	}
}

double (*PredictTreeByMapPtr[])(const std::unordered_map<int, double>&) = { PredictTree0ByMap , PredictTree1ByMap , PredictTree2ByMap , PredictTree3ByMap , PredictTree4ByMap , PredictTree5ByMap , PredictTree6ByMap , PredictTree7ByMap , PredictTree8ByMap , PredictTree9ByMap };

void GBDT::PredictRawByMap(const std::unordered_map<int, double>& features, double* output, const PredictionEarlyStopInstance* early_stop) const {
	int early_stop_round_counter = 0;
	std::memset(output, 0, sizeof(double) * num_tree_per_iteration_);
	for (int i = 0; i < num_iteration_for_pred_; ++i) {
		for (int k = 0; k < num_tree_per_iteration_; ++k) {
			output[k] += (*PredictTreeByMapPtr[i * num_tree_per_iteration_ + k])(features);
		}
		++early_stop_round_counter;
		if (early_stop->round_period == early_stop_round_counter) {
			if (early_stop->callback_function(output, num_tree_per_iteration_))
				return;
			early_stop_round_counter = 0;
		}
	}
}

void GBDT::Predict(const double* features, double *output, const PredictionEarlyStopInstance* early_stop) const {
	PredictRaw(features, output, early_stop);
	if (average_output_) {
		for (int k = 0; k < num_tree_per_iteration_; ++k) {
			output[k] /= num_iteration_for_pred_;
		}
	}
	if (objective_function_ != nullptr) {
		objective_function_->ConvertOutput(output, output);
	}
}

void GBDT::PredictByMap(const std::unordered_map<int, double>& features, double* output, const PredictionEarlyStopInstance* early_stop) const {
	PredictRawByMap(features, output, early_stop);
	if (average_output_) {
		for (int k = 0; k < num_tree_per_iteration_; ++k) {
			output[k] /= num_iteration_for_pred_;
		}
	}
	if (objective_function_ != nullptr) {
		objective_function_->ConvertOutput(output, output);
	}
}

double PredictTree0Leaf(const double* arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3215000000000001) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.67850000000000021) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0050000000000001) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {return 0; } else { return 10; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return 4; } else { return 5; } } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {return 3; } else { return 7; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 6; } else { return 8; } } } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.46349999999999997) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.91850000000000021) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {return 1; } else { return 11; } } else { return 9; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return 2; } else { return 13; } } else { return 12; } } } }
double PredictTree0LeafByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3215000000000001) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.67850000000000021) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0050000000000001) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {return 0; } else { return 10; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return 4; } else { return 5; } } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {return 3; } else { return 7; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 6; } else { return 8; } } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.46349999999999997) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.91850000000000021) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {return 1; } else { return 11; } } else { return 9; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return 2; } else { return 13; } } else { return 12; } } } }

double PredictTree1Leaf(const double* arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.58350000000000002) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.29350000000000004) {return 0; } else { return 12; } } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.69550000000000012) {return 2; } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.7210000000000003) {return 9; } else { return 10; } } } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.37600000000000006) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.7210000000000003) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {return 1; } else { return 11; } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.46349999999999997) {return 5; } else { return 8; } } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.58350000000000002) {return 3; } else { return 7; } } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.81950000000000001) {return 4; } else { return 6; } } } } }
double PredictTree1LeafByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.58350000000000002) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.29350000000000004) {return 0; } else { return 12; } } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.69550000000000012) {return 2; } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.7210000000000003) {return 9; } else { return 10; } } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.37600000000000006) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.7210000000000003) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {return 1; } else { return 11; } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.46349999999999997) {return 5; } else { return 8; } } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.58350000000000002) {return 3; } else { return 7; } } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.81950000000000001) {return 4; } else { return 6; } } } } }

double PredictTree2Leaf(const double* arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3215000000000001) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.67850000000000021) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {return 0; } else { return 11; } } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.81950000000000001) {return 3; } else { return 14; } } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {return 2; } else { return 5; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {return 4; } else { return 6; } } } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.81950000000000001) {return 1; } else { return 12; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {return 10; } else { return 13; } } } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.44450000000000006) {return 7; } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.58350000000000002) {return 8; } else { return 9; } } } } }
double PredictTree2LeafByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3215000000000001) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.67850000000000021) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {return 0; } else { return 11; } } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.81950000000000001) {return 3; } else { return 14; } } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {return 2; } else { return 5; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {return 4; } else { return 6; } } } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.81950000000000001) {return 1; } else { return 12; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {return 10; } else { return 13; } } } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.44450000000000006) {return 7; } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.58350000000000002) {return 8; } else { return 9; } } } } }

double PredictTree3Leaf(const double* arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3215000000000001) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.67850000000000021) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0050000000000001) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 0; } else { return 9; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return 4; } else { return 5; } } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {return 3; } else { return 7; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 6; } else { return 8; } } } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.46349999999999997) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.91850000000000021) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {return 1; } else { return 13; } } else { return 10; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return 2; } else { return 12; } } else { return 11; } } } }
double PredictTree3LeafByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3215000000000001) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.67850000000000021) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0050000000000001) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 0; } else { return 9; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return 4; } else { return 5; } } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {return 3; } else { return 7; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 6; } else { return 8; } } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.46349999999999997) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.91850000000000021) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {return 1; } else { return 13; } } else { return 10; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return 2; } else { return 12; } } else { return 11; } } } }

double PredictTree4Leaf(const double* arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3215000000000001) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.67850000000000021) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0050000000000001) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.44450000000000006) {return 0; } else { return 5; } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.35150000000000003) {return 4; } else { return 10; } } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {return 3; } else { return 11; } } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.1035000000000001) {return 6; } else { return 8; } } } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3445000000000003) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {return 1; } else { return 14; } } else { return 13; } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return 2; } else { return 9; } } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.69550000000000012) {return 7; } else { return 12; } } } } }
double PredictTree4LeafByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3215000000000001) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.67850000000000021) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0050000000000001) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.44450000000000006) {return 0; } else { return 5; } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.35150000000000003) {return 4; } else { return 10; } } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {return 3; } else { return 11; } } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.1035000000000001) {return 6; } else { return 8; } } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3445000000000003) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {return 1; } else { return 14; } } else { return 13; } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return 2; } else { return 9; } } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.69550000000000012) {return 7; } else { return 12; } } } } }

double PredictTree5Leaf(const double* arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.52550000000000019) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.35150000000000003) {return 0; } else { return 6; } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.37600000000000006) {return 4; } else { return 5; } } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {return 3; } else { return 9; } } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.7210000000000003) {return 7; } else { return 8; } } } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.86649999999999994) {return 1; } else { return 13; } } else { return 12; } } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.69550000000000012) {return 2; } else { fval = arr[0];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {return 10; } else { return 11; } } } } }
double PredictTree5LeafByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.52550000000000019) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.35150000000000003) {return 0; } else { return 6; } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.37600000000000006) {return 4; } else { return 5; } } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {return 3; } else { return 9; } } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.7210000000000003) {return 7; } else { return 8; } } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.86649999999999994) {return 1; } else { return 13; } } else { return 12; } } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.69550000000000012) {return 2; } else { fval = arr.count(0) > 0 ? arr.at(0) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.95350000000000013) {return 10; } else { return 11; } } } } }

double PredictTree6Leaf(const double* arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.52550000000000019) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.37600000000000006) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {return 0; } else { return 10; } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.35150000000000003) {return 9; } else { return 11; } } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.91850000000000021) {return 5; } else { return 8; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return 6; } else { return 7; } } } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 1; } else { return 4; } } else { return 3; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return 2; } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return 12; } else { return 13; } } } } }
double PredictTree6LeafByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.52550000000000019) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.37600000000000006) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {return 0; } else { return 10; } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.35150000000000003) {return 9; } else { return 11; } } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.97250000000000003) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.91850000000000021) {return 5; } else { return 8; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return 6; } else { return 7; } } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 1; } else { return 4; } } else { return 3; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return 2; } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return 12; } else { return 13; } } } } }

double PredictTree7Leaf(const double* arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.52550000000000019) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.37600000000000006) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {return 0; } else { return 10; } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.35150000000000003) {return 9; } else { return 11; } } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3215000000000001) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {return 5; } else { return 7; } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {return 6; } else { return 8; } } } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 1; } else { return 4; } } else { return 3; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return 2; } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return 12; } else { return 13; } } } } }
double PredictTree7LeafByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.52550000000000019) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.37600000000000006) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {return 0; } else { return 10; } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.35150000000000003) {return 9; } else { return 11; } } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3215000000000001) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.3590000000000002) {return 5; } else { return 7; } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {return 6; } else { return 8; } } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 1; } else { return 4; } } else { return 3; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return 2; } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return 12; } else { return 13; } } } } }

double PredictTree8Leaf(const double* arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.29350000000000004) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.1455000000000002) {return 0; } else { return 7; } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.81500000000000006) {return 6; } else { return 11; } } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.29350000000000004) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.46349999999999997) {return 5; } else { return 10; } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0050000000000001) {return 8; } else { return 9; } } } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 1; } else { return 4; } } else { return 3; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return 2; } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return 12; } else { return 13; } } } } }
double PredictTree8LeafByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.29350000000000004) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.1455000000000002) {return 0; } else { return 7; } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.81500000000000006) {return 6; } else { return 11; } } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.29350000000000004) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.46349999999999997) {return 5; } else { return 10; } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0050000000000001) {return 8; } else { return 9; } } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 1; } else { return 4; } } else { return 3; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return 2; } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return 12; } else { return 13; } } } } }

double PredictTree9Leaf(const double* arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.52550000000000019) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.37600000000000006) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {return 0; } else { return 10; } } else { fval = arr[3];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.35150000000000003) {return 9; } else { return 11; } } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.29350000000000004) {fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.46349999999999997) {return 5; } else { return 7; } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.86649999999999994) {return 6; } else { return 8; } } } } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 1; } else { return 4; } } else { return 3; } } else { fval = arr[1];if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return 2; } else { fval = arr[2];if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return 12; } else { return 13; } } } } }
double PredictTree9LeafByMap(const std::unordered_map<int, double>& arr) { const std::vector<uint32_t> cat_threshold = {};double fval = 0.0f; fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.6275000000000002) {fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.52550000000000019) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.37600000000000006) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -1.3464999999999996) {return 0; } else { return 10; } } else { fval = arr.count(3) > 0 ? arr.at(3) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.35150000000000003) {return 9; } else { return 11; } } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.29350000000000004) {fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.46349999999999997) {return 5; } else { return 7; } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.86649999999999994) {return 6; } else { return 8; } } } } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 1.0000000180025095e-35) {fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.72299999999999986) {return 1; } else { return 4; } } else { return 3; } } else { fval = arr.count(1) > 0 ? arr.at(1) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= -0.38749999999999996) {return 2; } else { fval = arr.count(2) > 0 ? arr.at(2) : 0.0f;if (std::isnan(fval)) fval = 0.0;if (fval <= 0.68350000000000011) {return 12; } else { return 13; } } } } }

double (*PredictTreeLeafPtr[])(const double*) = { PredictTree0Leaf , PredictTree1Leaf , PredictTree2Leaf , PredictTree3Leaf , PredictTree4Leaf , PredictTree5Leaf , PredictTree6Leaf , PredictTree7Leaf , PredictTree8Leaf , PredictTree9Leaf };

void GBDT::PredictLeafIndex(const double* features, double *output) const {
	int total_tree = num_iteration_for_pred_ * num_tree_per_iteration_;
	for (int i = 0; i < total_tree; ++i) {
		output[i] = (*PredictTreeLeafPtr[i])(features);
	}
}
double (*PredictTreeLeafByMapPtr[])(const std::unordered_map<int, double>&) = { PredictTree0LeafByMap , PredictTree1LeafByMap , PredictTree2LeafByMap , PredictTree3LeafByMap , PredictTree4LeafByMap , PredictTree5LeafByMap , PredictTree6LeafByMap , PredictTree7LeafByMap , PredictTree8LeafByMap , PredictTree9LeafByMap };

void GBDT::PredictLeafIndexByMap(const std::unordered_map<int, double>& features, double* output) const {
	int total_tree = num_iteration_for_pred_ * num_tree_per_iteration_;
	for (int i = 0; i < total_tree; ++i) {
		output[i] = (*PredictTreeLeafByMapPtr[i])(features);
	}
}
}  // namespace LightGBM
#endif
