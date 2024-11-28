def num_trees_for_memory(max_depth=3, memory=8000):
    num_tress = 0
    bits_per_tree = 3 * 16 * (2**max_depth - 1) + 32 * (2**max_depth - 1) + 32 * 2**max_depth # 16 bit left_child + 16 bit right_child + 16 bit split_feature + 32 bit leave_value + 32 bit threshold
    print(bits_per_tree)
    while (memory-bits_per_tree) > 0:
        memory -= bits_per_tree
        num_tress += 1
    return num_tress

print(num_trees_for_memory(3, 4000))
