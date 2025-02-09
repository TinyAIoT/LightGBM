/*!
 * Copyright (c) 2019 Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License. See LICENSE file in the project root for
 * license information.
 */

#ifndef LIGHTGBM_MEMORY_RESTRICTED_FOREST_H
#define LIGHTGBM_MEMORY_RESTRICTED_FOREST_H

#include <LightGBM/config.h>
#include <LightGBM/dataset.h>
#include <LightGBM/utils/log.h>
#include <vector>
#include <fstream>

namespace LightGBM {
  struct split_info {
    int bits;
    bool new_threshold;
    bool new_feature;
    int tindex;
    int findex;
    int feature_bits;
  };

  struct memory_separation {
    int bits_bool_thres = 0;
    int bits_float_thres = 0;
    int bits_float_leaf = 0;
    int bits_feature_threshold_mapping = 0;
    int bits_tree_refs = 0;
  };

  struct ref_tree {
    int tree_id;
    std::vector<int> feature_ids;
    std::vector<int> thresholds;
  };

  std::ostream &operator <<(std::ostream &outs, const ref_tree &ref_t) {
    outs << ref_t.tree_id << ": features: ";
    std::vector<int> featureids = ref_t.feature_ids;
    for (int feature: ref_t.feature_ids) {
      outs << feature << " ";
    }
    outs << "\n\tthresholds:\t";
    for (int threshold: ref_t.thresholds) {
      outs << threshold << " ";
    }
    outs << "\n";
    return outs;
  }

  struct threshold_info {
    std::vector<double> thresholds_;
    uint32_t feature;
    int bits;

    threshold_info(int featureid) {
      feature = featureid;
    }

    threshold_info(int featureid, double threshold, double bits_) {
      feature = featureid;
      thresholds_.push_back(threshold);
      bits = bits_;
    }
  };

  std::ostream &operator <<(std::ostream &outs, const threshold_info &thres_inf) {
    outs << thres_inf.feature << ": thresholds: ";
    for (double threshold: thres_inf.thresholds_) {
      outs << threshold << " ";
    }
    outs << "\n";
    return outs;
  }

  class MemoryRestrictedForest {
  public:
    explicit MemoryRestrictedForest(const SerialTreeLearner *tree_learner)
      : init_(false), tree_learner_(tree_learner) {
    }

    /* Returns the bits to represent a number */
    int bits(int size) {
      if (size == 0) return 1; // Special case for number 0
      if (size < 0) return 1;
      int bits = 0;
      while (size) {
        bits++;
        size >>= 1; // Right shift the number by 1 bit
      }
      return bits;
    }

    int nextPow2(int number) {
      if (number == 0) return 1;
      if ((number & (number - 1)) == 0) return number;
      number--;
      number |= number >> 1;
      number |= number >> 2;
      number |= number >> 4;
      number |= number >> 8;
      number |= number >> 16;
      number++;

      return number;
    }

    void InsertLeafInformation(double leaf_value) {
      bool found = false, featurefound = false;
      int tcounter;
      for (std::size_t i = 0; i < threshold_per_feature.size(); i++) {
        if (threshold_per_feature[i].feature == 255) {
          featurefound = true;
          for (std::size_t j = 0; j < threshold_per_feature[i].thresholds_.size(); j++) {
            if (threshold_per_feature[i].thresholds_[j] == leaf_value) {
              found = true;
              tcounter = j;
            }
          }
        }
      }
#pragma omp critical
      ref_trees_.back().feature_ids.push_back(255);
      if (found) {
#pragma omp critical
        ref_trees_.back().thresholds.push_back(tcounter);
      } else {
#pragma omp critical
        thresholds_used_global_.push_back(leaf_value);
        if (!featurefound) {
#pragma omp critical
          threshold_per_feature.push_back({255, leaf_value, 32});
          ref_trees_.back().thresholds.push_back(0);
        } else {
          for (std::size_t i = 0; i < threshold_per_feature.size(); i++) {
            if (threshold_per_feature[i].feature == 255) {
#pragma omp critical
              threshold_per_feature[i].thresholds_.push_back(leaf_value);
#pragma omp critical
              ref_trees_.back().thresholds.push_back(threshold_per_feature[i].thresholds_.size() - 1);
            }
          }
        }
      }
    }

    void UpdateMemoryForTree(Tree *tree) {
#pragma omp critical
      ref_trees_.push_back({});
      ref_trees_.back().tree_id = ref_trees_.size() - 1;
    }

    void InsertSplitInfo(const Tree *tree) {
      size_t last_node_id = tree->num_leaves_ - 2;
      const double threshold = tree->threshold_[last_node_id];
      const uint32_t feature = tree->split_feature_[last_node_id];
      split_info split_inf = {};
      CalculateSplitMemoryConsumption(split_inf, threshold, feature);
      int feature_to_insert;
      if (split_inf.new_feature) {
        feature_to_insert = feature;
        features_used_global_.push_back(feature);
#pragma omp critical
        ref_trees_.back().feature_ids.push_back(feature);
#pragma omp critical
        threshold_per_feature.push_back({static_cast<int>(feature)});
      } else {
        feature_to_insert = split_inf.findex;
#pragma omp critical
        ref_trees_.back().feature_ids.push_back(feature);
      }
      if (split_inf.new_threshold) {
        int tsize;
        for (std::size_t i = 0; i < threshold_per_feature.size(); i++) {
          if (static_cast<int>(threshold_per_feature[i].feature) == feature_to_insert) {
#pragma omp critical
            threshold_per_feature[i].thresholds_.push_back(threshold);
            tsize = threshold_per_feature[i].thresholds_.size() - 1;
          }
        }
#pragma omp critical
        thresholds_used_global_.push_back(threshold);
#pragma omp critical
        ref_trees_.back().thresholds.push_back(tsize);
      } else {
#pragma omp critical
        ref_trees_.back().thresholds.push_back(split_inf.tindex);
      }
      est_leftover_memory -= split_inf.bits;
      est_leftover_memory -= 32; // new leaf
    }

    bool isAllInteger(const std::vector<double> &column) {
      bool isInteger = true;
      for (const auto &value: column) {
        if (std::floor(value) != value) {
          // Check if value is not an integer
          return false;
        }
      }
      return isInteger;
    }

    void CalculateSplitMemoryConsumption(split_info &split_inf, double threshold, uint32_t feature) {
      split_inf.new_threshold = true;
      int currentsize = 0;
      for (std::size_t i = 0; i < threshold_per_feature.size(); i++) {
        if (threshold_per_feature[i].feature == feature) {
          currentsize = threshold_per_feature[i].thresholds_.size();
          for (std::size_t j = 0; j < threshold_per_feature[i].thresholds_.size(); j++) {
            if (threshold_per_feature[i].thresholds_[j] == threshold) {
              split_inf.new_threshold = false;
              split_inf.tindex = j;
              break;
            }
          }
        }
      }
      split_inf.bits += bits(currentsize - 1) + bits(features_used_global_.size());
      if (split_inf.new_threshold) {
        if (threshold != 0.0 && threshold != 1.0 && threshold > 1e-34) {
          split_inf.bits += 32;
        } else {
          split_inf.bits += 1;
        }
        if (bits(currentsize) > bits(max_num_threholds_per_feature - 1)) {
          split_inf.bits += features_used_global_.size();
          max_num_threholds_per_feature = currentsize + 1;
        }

        if (bits(currentsize) > bits(currentsize - 1)) {
          // Every feature reference in every tree would consume + 1 bit
          for (std::size_t i = 0; i < ref_trees_.size(); i++) {
            for (std::size_t j = 0; j < ref_trees_[i].feature_ids.size(); j++) {
              if (ref_trees_[i].feature_ids[j] == static_cast<int>(feature)) {
                split_inf.bits += 1;
              }
            }
          }
        }
      }
      bool foundfeature = false;
      for (int i = 0; i < features_used_global_.size(); i++) {
        if (feature == features_used_global_[i]) {
          foundfeature = true;
          split_inf.findex = feature;
        }
      }
      // In case the feature is not used 8 bits are added for representing a bits_single and bits_ref.
      if (!foundfeature) {
        split_inf.new_feature = true;
        split_inf.bits += CalculateFeatureMemoryConsumption();
      }
    }

    int CalculateFeatureMemoryConsumption() {
      int needed_bits = 0;
      int bit_num_thres = bits(max_num_threholds_per_feature - 1);
      needed_bits += 3 + 1 + bits(this->tree_learner_->train_data_->num_features() - 1) + bit_num_thres;
      if (bits(features_used_global_.size() + 1) > bits(features_used_global_.size())) {
        // Every feature reference in every tree would consume + 1 bit
        for (std::size_t i = 0; i < ref_trees_.size(); i++) {
          for (std::size_t j = 0; j < ref_trees_[i].feature_ids.size(); j++) {
            if (ref_trees_[i].feature_ids[j] != -1) {
              needed_bits += 1;
            }
          }
        }
      }
      return needed_bits;
    }

    static bool IsEnable(const Config *config) {
      if (config->tinygbdt_forestsize == 0) {
        Log::Info("MemoryRestrictedForest disabled");
        return false;
      }
      return true;
    }

    void Init(const int forestsize_, int max_depth_) {
      max_depth = max_depth_;
      if (ref_trees_.empty()) {
        ref_trees_.push_back({});
        ref_trees_.back().tree_id = ref_trees_.size() - 1;
      }
      est_leftover_memory = forestsize_;
      forestsize = forestsize_;
    }
    void printMemory() {
      std::stringstream out;
      memory_separation control = CalcMemoryAtTheEnd();

      out << "Calculated Memory consumption:" << "\n";
      out << "\tBits Bool Thresholds: " << control.bits_bool_thres << "\n";
      out << "\tBits float thresholds: " << control.bits_float_thres << "\n";
      out << "\tBits References inside Trees: " << control.bits_tree_refs << "\n";
      out << "\tBits Feature Threshold mapping: " << control.bits_feature_threshold_mapping << "\n";
      out << "\tBits Feature float leaves: " << control.bits_float_leaf << "\n";

      std::cout << out.str();
    }

    void printForest() {
      int threshold_size = 0;
      int feature_size = threshold_per_feature.size();
      std::stringstream out;
      out << "Leftover memory : " << est_leftover_memory << "\n";
      // subtract values of features not used except feature 0 itself
      out << "features_used_global : " << features_used_global_.size() << "\n";
      out << "thresholds_used_global : " << thresholds_used_global_.size() << "\n";
      for (std::size_t i = 0; i < ref_trees_.size() - 1; i++) {
        out << ref_trees_[i];
      }
      out << "\n";
      for (std::size_t i = 0; i < threshold_per_feature.size(); i++) {
        out << threshold_per_feature[i];
        threshold_size += threshold_per_feature[i].thresholds_.size();
      }
      out << "\n";
      memory_separation control = CalcMemoryAtTheEnd();

      out << "#features : " << feature_size << "\n";
      out << "#thresholds : " << threshold_size << "\n";
      out << "Calculated Memory consumption:" << "\n";
      out << "\tBits Bool Thresholds: " << control.bits_bool_thres << "\n";
      out << "\tBits float thresholds: " << control.bits_float_thres << "\n";
      out << "\tBits References inside Trees: " << control.bits_tree_refs << "\n";
      out << "\tBits Feature Threshold mapping: " << control.bits_feature_threshold_mapping << "\n";
      out << "\tBits Feature float leaves: " << control.bits_float_leaf << "\n";

      std::cout << out.str();
    }

    memory_separation CalcMemoryAtTheEnd() {
      memory_separation memory = {};
      for (threshold_info t_f_info: threshold_per_feature) {
        for (double threshold: t_f_info.thresholds_) {
          if (t_f_info.feature == 255) {
            memory.bits_float_leaf += 32;
          } else {
            if (threshold != 0.0 && threshold != 1.0 && threshold > 1e-34) {
              memory.bits_float_thres += 32;
            } else {
              memory.bits_bool_thres += 1;
            }
          }
        }
      }
      int bit_num_thres = bits(max_num_threholds_per_feature);
      memory.bits_feature_threshold_mapping += features_used_global_.size() * (
        4 + bits(this->tree_learner_->train_data_->num_features() - 1) + bit_num_thres);
      int leavesize = 0;
      for (threshold_info t_f_info: threshold_per_feature) {
        if (t_f_info.feature == 255) {
          leavesize = t_f_info.thresholds_.size();
        }
      }
      int leaves = static_cast<int>(pow(2, max_depth));
      int numNodes = static_cast<int>(pow(2, max_depth)) - 1;
      for (ref_tree tree: ref_trees_) {
        if (tree.feature_ids.size() == 0) { break; }
        memory.bits_tree_refs += bits(leavesize - 1) * leaves;
        memory.bits_tree_refs += bits(features_used_global_.size()-1) * numNodes;
        for (int feature: tree.feature_ids) {
          if (feature != 255) {
            for (threshold_info t_f_info: threshold_per_feature) {
              if (t_f_info.feature == feature) {
                int size = t_f_info.thresholds_.size() - 1;
                if (size == 0) { size = 1; }
                memory.bits_tree_refs += bits(size);
              }
            }
          }
        }
      }
      return memory;
    }

    bool init_;
    int est_leftover_memory, max_depth, forestsize;
    const SerialTreeLearner *tree_learner_;
    std::vector<double> thresholds_used_global_;
    std::vector<uint32_t> features_used_global_;
    std::vector<ref_tree> ref_trees_;
    std::vector<threshold_info> threshold_per_feature;
    int max_num_threholds_per_feature = 1;
  };
}
#endif //LIGHTGBM_MEMORY_RESTRICTED_FOREST_H
