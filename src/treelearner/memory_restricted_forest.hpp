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
    int bits(int size) {
      if (size == 0) return 1; // Special case for number 0
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
      }}}}
#pragma omp critical
      ref_trees_[treecounter].feature_ids.push_back(255);
      if (found) {
#pragma omp critical
        ref_trees_[treecounter].thresholds.push_back(tcounter);
      } else {
        // TODO: Insert Calculation for leaf reference bit consumptions.
        est_leftover_memory -= 32;
        memory_consumption.bits_float_leaf += 32;
#pragma omp critical
        thresholds_used_global_.push_back(leaf_value);
        if (!featurefound) {
#pragma omp critical
          threshold_per_feature.push_back({255, leaf_value, 32});
          ref_trees_[treecounter].thresholds.push_back(0);
        } else {
          int currentsize = 0;
          for (std::size_t i = 0; i < threshold_per_feature.size(); i++) {
            if (threshold_per_feature[i].feature == 255) {
              currentsize = threshold_per_feature[i].thresholds_.size();
          }}
          int next_power_of_two = nextPow2(currentsize + 1);
          if (currentsize > next_power_of_two) {
            int referencesinc = 0;
            for (ref_tree tree: ref_trees_) {
              for (double feature: tree.thresholds) {
                if (feature == 255) {
                  referencesinc += 1;
                }
              }
            }
            est_leftover_memory -= referencesinc;
            memory_consumption.bits_tree_refs += referencesinc;
          }
          memory_consumption.bits_tree_refs += bits(currentsize);
          est_leftover_memory -= bits(currentsize);
          for (std::size_t i = 0; i < threshold_per_feature.size(); i++) {
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
    /*
     *Calculates how much it cost us to add a feature
     *3 = 3 bit feature index, 3 bit size (1,2,3,4,6,8,16,32),
     *... 1 bit int/float, ceil(log2(#features)) bits needed to reference column,
     *... Check for bits needed for reference to global features
     */
    int CalculateFeatureMemoryConsumption(bool insert) {
      int needed_bits = 0;
      int unique_feature = bits(fcounter);
      needed_bits += 3 + 3 + 1 + bits(this->tree_learner_->train_data_->num_features()) + unique_feature;
      if (insert) {memory_consumption.bits_feature_threshold_mapping += needed_bits;}
      int next_power_of_two = nextPow2(fcounter + 1);
      // In case the power of two increases we have an increase for every reference in every tree and for the reference
      // in the feature mapping to the global threshold "array"
      if (CHECK_QUANTIZATION){
        if (fcounter + 1 > next_power_of_two) {
          if (unique_feature < bits(fcounter+1)) {
            // For each feature mapping the bitreference needs to be increased.
            needed_bits += threshold_per_feature.size();
            if (insert) {memory_consumption.bits_feature_threshold_mapping += threshold_per_feature.size();}
          }
          // Every feature reference in every tree would consume + 1 bit
          for (std::size_t i = 0; i < ref_trees_.size(); i++) {
            for (std::size_t j = 0; j < ref_trees_[i].feature_ids.size(); j++) {
              if (ref_trees_[i].feature_ids[j] != -1) {
                needed_bits += 1;
                if (insert) {memory_consumption.bits_tree_refs += 1;}
      }}}}}
      return needed_bits;
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
      // const BinMapper *bin_mapper = train_data_->FeatureBinMapper(feature);
      consumed_memory con_mem = {};
      CalculateSplitMemoryConsumption(con_mem, threshold, feature, true);
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

    void CalculateSplitMemoryConsumption(consumed_memory &con_mem, double threshold, uint32_t feature, bool insert = false) {
      con_mem.new_threshold = true;
      int currentsize = 0;
      for (std::size_t i = 0; i < threshold_per_feature.size(); i++) {
        if (threshold_per_feature[i].feature == feature) {
          currentsize = threshold_per_feature[i].thresholds_.size();
          for (std::size_t j = 0; j < threshold_per_feature[i].thresholds_.size(); j++) {
            if (threshold_per_feature[i].thresholds_[j] == threshold) {
              con_mem.new_threshold = false;
              con_mem.tindex = j;
              break;
      }}}}
      // Cost of reference in tree.
      con_mem.bits += bits(currentsize + 1);
      if (insert) {
        memory_consumption.bits_tree_refs += bits(currentsize + 1);
        memory_consumption.bits_tree_refs += bits(fcounter+1);
      }
      if (con_mem.new_threshold) {
        // Size of inserting bit or float for threshold
        if (threshold != 0.0 && threshold != 1.0) {
          con_mem.bits += 32;
          if (insert) {memory_consumption.bits_float_thres += 32;}
        } else {
          con_mem.bits += 1;
          if (insert) {memory_consumption.bits_bool_thres += 1;}
        }
        // Check if current size +1 exceeds the next power of two
        if (CHECK_QUANTIZATION) {
          int next_power_of_two = nextPow2(currentsize + 1);
          if (bits(currentsize + 1) > bits(max_num_threholds_per_feature)) {
            // We need to increase the size of the previous feature mappings as those depend on the number of threholds
            con_mem.bits += fcounter;
            if (insert) {
              memory_consumption.bits_feature_threshold_mapping += fcounter;
              max_num_threholds_per_feature = currentsize + 1;
            }
          }
          if (currentsize + 1 > next_power_of_two) {
            // Every feature reference in every tree would consume + 1 bit
            for (std::size_t i = 0; i < ref_trees_.size(); i++) {
              for (std::size_t j = 0; j < ref_trees_[i].feature_ids.size(); j++) {
                if (ref_trees_[i].feature_ids[j] == static_cast<int>(feature)) {
                  con_mem.bits += 1;
                  if (insert) {memory_consumption.bits_tree_refs += 1;}
                }}}}}
      }
      int sizef = fcounter;
      bool foundfeature = false;
      for (int i = 0; i < sizef; i++) {
        if (feature == features_used_global_[i]) {
          foundfeature = true;
          con_mem.findex = feature;
        }
      }
      // In case the feature is not used 8 bits are added for representing a bits_single and bits_ref.
      if (!foundfeature) {
        con_mem.new_feature = true;
        con_mem.bits += CalculateFeatureMemoryConsumption(insert);
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
      this->precision = precision;
      auto train_data = tree_learner_->train_data_;
      features_used_global_.resize(train_data->num_features());
    }
    void printForest() {
      std::stringstream out;
      out << "Leftover memory: " << est_leftover_memory;
      out << "\n";
      for (std::size_t i = 0; i < ref_trees_.size()-1; i++) {
        out << ref_trees_[i];
      }
      out << "\n";
      for (std::size_t i = 0; i < threshold_per_feature.size(); i++) {
        out << threshold_per_feature[i];
      }
      out << "\n";
      out << "Calculated Memory consumption:" << "\n";
      out << "\tBits Bool Thresholds: " << memory_consumption.bits_bool_thres << "\n";
      out << "\tBits float thresholds: " << memory_consumption.bits_float_thres << "\n";
      out << "\tBits References inside Trees: " << memory_consumption.bits_tree_refs << "\n";
      out << "\tBits Feature Threshold mapping: " << memory_consumption.bits_feature_threshold_mapping << "\n";
      out << "\tBits Feature float leaves: " << memory_consumption.bits_float_leaf << "\n";
      std::cout << out.str();
    }
    bool init_;
    int est_leftover_memory, max_depth;
    memory_separation memory_consumption;
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
    int treecounter = 0, max_num_threholds_per_feature = 0;
  };
}
#endif //LIGHTGBM_MEMORY_RESTRICTED_FOREST_H
