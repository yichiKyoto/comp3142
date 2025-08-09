# Data Structures
## total_seeds_processed 
the amount of times run target was called to run a seed
## avg_bitmap_size 
the average amount of edges that were triggered by a seed
## avg_exec_size 
the average execution time of a seed

# Functions

## get_power_schedule(seed, avg_exec_us, avg_bitmap_size)
This function takes three parameters seed, avg_exec_us and avg_bitmap_size.
I calculated the perf_score by comparing the coverage and execution time of the seed
to the average coverage and execution time across all seeds processed. Then, I returned that perf_score.

## run_fuzzing
I modified this function by recomputing avg_bitmap_size and avg_exec_time every single
time the check_coverage(trace_bits) function is run, as shown below - 
avg_bitmap_size = calculate_new_avg(avg_bitmap_size, total_seeds_processed, coverage)
avg_exec_time = calculate_new_avg(avg_exec_time, total_seeds_processed, exec_time)
avg_bitmap_size/avg_exec_time represents the old average, total_seeds_processed represents
the original amount of seeds processed and coverage/exec_time represents the new value that affects the
computation of the new averages.

## calculate_new_avg(current_avg, size, new_value)
This function takes in the parameters current_avg, size and new_value to compute the new average.

