from pyomo.environ import *
infinity = float('inf')

model = AbstractModel()

# Goods
model.G = Set()
# Profit
model.P = Set()
# Days
model.D = Set()
# Volume
model.V = Set()

# Volume
model.v = Param(model.V, model.G, within=PositiveReals)

# Production
model.p = Param(model.D, model.G, within=PositiveReals)

# Demand
model.d = Param(model.D, model.G, within=PositiveReals)

# Lower and upper bound demand on Goods
model.GDmin = Param(model.D, model.G, within=NonNegativeReals, default=0.0)
model.GDmax = Param(model.D, model.G, within=NonNegativeReals, default=infinity)

# Lower and upper bound productivity on Goods
model.GPmin = Param(model.D, model.G, within=NonNegativeReals, default=0.0)
model.GPmax = Param(model.D, model.G, within=NonNegativeReals, default=infinity)

# Lower and upper agreement's bound on Goods
model.GAmin = Param(model.D, model.G, within=NonNegativeReals)
model.GAmax = Param(model.D, model.G, within=NonNegativeReals, default=infinity)

# Lower and upper bound volume on Goods
model.GVmin = Param(model.D, model.G, within=NonNegativeReals, default=0.0)
model.GVmax = Param(model.D, model.G, within=NonNegativeReals, default=infinity)

# Agreements
model.a = Param(model.D, model.G, within=PositiveReals)

# Generate max profit
model.x = Var(model.G, model.P, within=NonNegativeIntegers)

# Maximize profi of production
def profit_rule(model):
    return sum(model.P[i]*model.x[i] for i in model.G)
model.profit = Objective(rule=profit_rule)

# Limit demand for goods
def demand_rule(model, j):
    value = sum(model.d[i,j]*model.x[i] for i in model.G) * Model.D
    return inequality(model.GDmin[j], value, model.GDmax[j])
model.demand_limit = Constraint(model.G, rule=demand_rule)

# Limit production for goods
def produce_rule(model, j):
    value = sum(model.p[i,j]*model.x[i] for i in model.G) 
    return inequality(model.GPmin[j], value, model.GPmax[j])
model.produce_limit = Constraint(model.G, rule=produce_rule)

# Limit agreements for goods
def agreement_rule(model, j):
    value = sum(model.a[i,j]*model.x[i] for i in model.G) * Model.D
    return inequality(model.GAmin[j], value, model.GAmax[j])
model.agreement_limit = Constraint(model.G, rule=agreement_rule)

# Limit volume for goods
def volume_rule(model, j):
    value = sum(model.a[i,j]*model.x[i] for i in model.G) * 1000
    return inequality(value, model.GVmax[j])
model.volume_limit = Constraint(model.G, rule=volume_rule)