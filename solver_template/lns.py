import misc as m
#TODO finish LNS implementation
def lns( stopage: int, matrix: list[list[float]], solution: list[int]) ->list[list[int],int]:
    s = solution
    best_s = s
    best_cost = m.calculateCost(best_s,matrix)

    for i in range(stopage):
        #destroy
        #repair
        #2-opt
        #new cost
        #update
        #solution acceptance
        pass
    return best_s, best_cost