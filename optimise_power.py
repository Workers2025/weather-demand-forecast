from scipy.optimize import linprog

def optimise_power_procurement(predicted_demand, solar_available, grid_cost, solar_cost):
    # Objective: Minimize total cost
    c = [solar_cost, grid_cost]
    
    # Constraints: 
    # x1 (solar) + x2 (grid) >= predicted_demand
    A = [[-1, -1]]
    b = [-predicted_demand]
    
    bounds = [(0, solar_available), (0, None)]  # Solar limit, grid no limit
    
    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
    return res.x  # Optimal (solar power used, grid power used)
