def adaptiveRepairAndDestroy(tour : list[int], matrix : list[list[float]], max_iterations : int):
    return 2
    # Setup counter for no improvements
    # Setup a threshold for how many iterations without improvement are okay
    # Calculate current cost of the tour

    # Main loop
        # Check if improvement is stagnating => iterations without improvement > threshold do:
            # Increase destruction size
            # Diverse repair function
        # Else
            # smaller destruction size
            # greedy repair
        
        # Do destroy(tour, city_cnt) -> partial_tour, removedCities
        # Do repair(partial_tour, removed_cities, matrix, repair_strategy) -> repaired_tour

        # Calculate new_cost = cost(repaired_tour)
        # if new_cost < best_cost
            # best_tour = repaired_tour
            # best_cost = new_cost
            # improvement counter = 0
        # else
            # improvement counter ++
        
        # if timeout
            # break
    # return best_tour, best_cost

