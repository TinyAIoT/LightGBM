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

const bool CHECK_QUANTIZATION = true;
namespace LightGBM {
  struct consumed_memory {
    int bits;
    bool new_threshold;
    bool new_feature;
    int tindex;
    int findex;
    int feature_bits;
  };

  struct ref_tree {
    int tree_id;
    std::vector<int> feature_ids;
    std::vector<int> thresholds;
  };
  std::ostream & operator << (std::ostream & outs, const ref_tree & ref_t) {
    outs << ref_t.tree_id << ": features: ";
    for (double feature : ref_t.feature_ids) {
      outs << feature << " ";
    }
    outs << "\n\tthresholds:\t";
    for (double threshold : ref_t.thresholds) {
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
  std::ostream & operator << (std::ostream & outs, const threshold_info & thres_inf) {
    outs << thres_inf.feature << ": thresholds: ";
    for (double threshold : thres_inf.thresholds_) {
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
    void InsertLeafInformation(double leaf_value) {
      est_leftover_memory -= sizeof(float);
      bool found = false, featurefound = false;
      int tcounter;
      for (int i = 0; i < threshold_per_feature.size(); i++) {
        if (threshold_per_feature[i].feature == 255) {
          featurefound = true;
          for (int j = 0; j < threshold_per_feature[i].thresholds_.size(); j++) {
            if (threshold_per_feature[i].thresholds_[j] == leaf_value) {
              found = true;
              tcounter = j;
      }}}}
#pragma omp critical
      ref_trees_[treecounter].feature_ids.push_back(255);
      if (found) {
#pragma omp critical
        ref_trees_[treecounter].thresholds.push_back(tcounter);
      } else {
#pragma omp critical
        thresholds_used_global_.push_back(leaf_value);
        if (!featurefound) {
#pragma omp critical
          threshold_per_feature.push_back({255, leaf_value, 16});
          ref_trees_[treecounter].thresholds.push_back(0);
        } else {
          for (int i = 0; i < threshold_per_feature.size(); i++) {
            if (threshold_per_feature[i].feature == 255) {
#pragma omp critical
              threshold_per_feature[i].thresholds_.push_back(leaf_value);
#pragma omp critical
              ref_trees_[treecounter].thresholds.push_back(threshold_per_feature[i].thresholds_.size()-1);
            }
          }
        }
      }
    }

    void UpdateMemoryForTree(Tree* tree) {
#pragma omp critical
      tree_size_.push_back(tree->getNumberNodes());
      ref_trees_.push_back({});
      treecounter++;
      ref_trees_[treecounter].tree_id = treecounter;
    }
    void InsertSplitInfo(const Tree *tree, const Dataset *train_data_) {
      const int last_node_id = tree->num_leaves_ - 2;
      const double threshold = RoundDecimals(tree->threshold_[last_node_id], this->precision);
      const uint32_t feature = tree->split_feature_[last_node_id];
      const BinMapper *bin_mapper = train_data_->FeatureBinMapper(feature);
      consumed_memory con_mem = {};
      CalculateSplitMemoryConsumption(con_mem, threshold, feature);
      int feature_to_insert;
      if (con_mem.new_feature) {
        feature_to_insert = feature;
        features_used_global_[fcounter] = (feature);
#pragma omp critical
        ref_trees_[treecounter].feature_ids.push_back(feature);
#pragma omp critical
        threshold_per_feature.push_back({static_cast<int>(feature)});
        fcounter++;
      } else {
        feature_to_insert = con_mem.findex;
#pragma omp critical
        ref_trees_[treecounter].feature_ids.push_back(feature);
      }
      if (con_mem.new_threshold) {
        int tsize;
        for (int i = 0; i < threshold_per_feature.size(); i++) {
          if (threshold_per_feature[i].feature == feature_to_insert) {
#pragma omp critical
            threshold_per_feature[i].thresholds_.push_back(threshold);
            tsize = threshold_per_feature[i].thresholds_.size() - 1;
          }
        }
#pragma omp critical
        thresholds_used_global_.push_back(threshold);
#pragma omp critical
        ref_trees_[treecounter].thresholds.push_back(tsize);
      } else {
#pragma omp critical
        ref_trees_[treecounter].thresholds.push_back(con_mem.tindex);
      }

      // Always the predict value adds to one double.
      est_leftover_memory -= con_mem.bits;
    }

    bool isAllInteger(const std::vector<double>& column) {
      bool isInteger = true;
      for (const auto& value : column) {
        if (std::floor(value) != value) { // Check if value is not an integer
          return false;
        }
      }
      return isInteger;
    }

    void CalculateSplitMemoryConsumption(consumed_memory &con_mem, double threshold, uint32_t feature) {
      con_mem.new_threshold = true;
      int currentsize = 0;
      for (int i = 0; i < threshold_per_feature.size(); i++) {
        if (threshold_per_feature[i].feature == feature) {
          currentsize = threshold_per_feature[i].thresholds_.size();
          for (int j = 0; j < threshold_per_feature[i].thresholds_.size(); j++) {
            if (threshold_per_feature[i].thresholds_[j] == threshold) {
              con_mem.new_threshold = false;
              con_mem.tindex = j;
              // Size of inserting Bit or Float
              // TODO: shouldnt this be (equal or) instead of (unequal and)?
              if (threshold != 0.0 && threshold != 1.0) {
                con_mem.bits += 1;
              } else { con_mem.bits += 32;}
              break;
            }}}}

      con_mem.bits += std::ceil(std::log2(currentsize + 1));

      if (con_mem.new_threshold) {
        // Check if current size +1 exceeds the next power of two
        if (CHECK_QUANTIZATION) {
          size_t next_power_of_two = static_cast<size_t>(std::pow(2, std::ceil(std::log2(currentsize + 1))));
          if (currentsize + 1 > next_power_of_two) {
            // Every feature reference in every tree would consume + 1 bit
            for (int i = 0; i < ref_trees_.size(); i++) {
              for (int j = 0; j < ref_trees_[i].feature_ids.size(); j++) {
                if (ref_trees_[i].feature_ids[j] == feature) {
                  con_mem.bits += 1;
                }}}}}
      }
      int sizef = features_used_global_.size();
      bool foundfeature = false;
      for (int i = 0; i < sizef; i++) {
        if (feature == features_used_global_[i]) {
          foundfeature = true;
          con_mem.findex = feature;
        }
      }
      // In case the feature is not used 8 bits are added for representing a bits_single and bits_ref.
      con_mem.bits += std::ceil(std::log2(features_used_global_.size() + 1));
      if (!foundfeature) {
        // TODO Check with Model.
        con_mem.bits += 4 + 1 + static_cast<int>(std::ceil(std::log2(this->tree_learner_->train_data_->num_features())));
        con_mem.new_feature = true;
        // Check if current size +1 exceeds the next power of two
        if (CHECK_QUANTIZATION){
          size_t next_power_of_two = static_cast<size_t>(std::pow(2, std::ceil(std::log2(features_used_global_.size() + 1))));
          if (features_used_global_.size() + 1 > next_power_of_two) {
            // Every feature reference in every tree would consume + 1 bit
            for (int i = 0; i < ref_trees_.size(); i++) {
              for (int j = 0; j < ref_trees_[i].feature_ids.size(); j++) {
                if (ref_trees_[i].feature_ids[j] != -1) {
                  con_mem.bits += 1;
        }}}}}
      }
    }

    double RoundDecimals(double number, double decimals) {
      double rounded = ((double)((int)(number * pow(10.0, decimals) + .5))) / pow(10.0, decimals);
      return rounded;
    }

    static bool IsEnable(const Config *config) {
      if (config->tinygbdt_forestsize == 0) {
        Log::Info("MemoryRestrictedForest disabled");
        return false;
      }
      if (config->num_iterations != 100 && config->max_depth > 0) {
        // TODO TinyGBT do we automatically want to set values if those are not set?
        // TODO I guess having one set is the easiest as we can eventually scale in the other direction.
      } else if (config->num_iterations != 100) {
      } else if (config->max_depth > 0) {
        // Assuming we have a fully covered binary tree get the maximum nodes in a single tree.
        // int max_nodes = static_cast<int>(pow(2, config->max_depth + 1) - 1);
      } else {
        // TODO TinyGBT none set we could either set a value assuming an average memory consumption for one if both but estimation will lead to a loss in accuracy.
      }
      return true;
    }

    void Init(const int treesize, const double precision, int max_depth_) {
      max_depth = max_depth_;
      ref_trees_.push_back({});
      ref_trees_[treecounter].tree_id = treecounter;
      est_leftover_memory = treesize;
      forestsize = treesize;      
      this->precision = precision;
      auto train_data = tree_learner_->train_data_;
      features_used_global_.resize(train_data->num_features());
    }
    void printForest() {
      int threshold_size = 0;
      int feature_size = threshold_per_feature.size();
      std::stringstream out;
      out << "Leftover memory : " << est_leftover_memory;
      out << "\n";
      // out << "features_used_global : " << features_used_global_.size()-std::count(features_used_global_.begin(), features_used_global_.end(), 0);
      // out << "\n";
      // out << "thresholds_used_global : " << thresholds_used_global_.size(); // -std::count(thresholds_used_global_.begin(), thresholds_used_global_.end(), 0); 
      // out << "\n";
      out << "features_used_global : " << fcounter;
      out << "features_used_global : " << features_used_global_.size()-std::count(features_used_global_.begin(), features_used_global_.end(), 0)+1; // subtract values of features not used except feature 0 itself 
      out << "\n";
      out << "thresholds_used_global : " << thresholds_used_global_.size(); // -std::count(thresholds_used_global_.begin(), thresholds_used_global_.end(), 0); 
      out << "\n";
      out << "#bits : " << forestsize-est_leftover_memory;
      out << "\n";
      for (int i = 0; i < ref_trees_.size()-1; i++) {
        out << ref_trees_[i];
      }
      out << "\n";
      for (int i = 0; i < threshold_per_feature.size(); i++) {
        out << threshold_per_feature[i];
        threshold_size += threshold_per_feature[i].thresholds_.size();
      }
      out << "\n";
      out << "#features : " << feature_size;
      out << "\n";
      out << "#thresholds : " << threshold_size;
      out << "\n";
      std::cout << out.str();
    }
    bool init_;
    int est_leftover_memory, max_depth, forestsize;
    double precision;
    const SerialTreeLearner *tree_learner_;
    /*! \brief count feature use; */
    /*! \brief record thresholds used for split; */
    std::vector<double> thresholds_used_global_;
    std::vector<int> tree_size_;
    std::vector<uint32_t> features_used_global_;
    int fcounter = 0;
    std::vector<ref_tree> ref_trees_;
    std::vector<threshold_info> threshold_per_feature;
    int treecounter = 0;
  };
}
#endif //LIGHTGBM_MEMORY_RESTRICTED_FOREST_H
