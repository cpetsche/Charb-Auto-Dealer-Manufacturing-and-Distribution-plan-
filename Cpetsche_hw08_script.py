# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 14:16:34 2021

@author: cpetsche
"""

import sqlite3
import gurobipy as grb
import os


os.getcwd()

my_conn = sqlite3.Connection(r'../database/charb_auto.db')
my_cursor = my_conn.cursor()


##Indexes

#plants (1,6)
sql_string = """
SELECT facility_id
FROM tbl_facility_information
WHERE facility_type = 1
"""

plants = my_cursor.execute(sql_string).fetchall()
plants = [p[0] for p in plants]

#lines
lines = [1,2]

#dealers (1,171)
sql_string = """
SELECT facility_id
FROM tbl_facility_information
WHERE facility_type = 2
"""

dealers = my_cursor.execute(sql_string).fetchall()
dealers = [d[0] for d in dealers]

#cars (1,9)
sql_string = """
SELECT car_id
FROM tbl_lkup_car
"""
cars = my_cursor.execute(sql_string).fetchall()
cars = set([c[0] for c in cars])

#staging centers (1,20)
sql_string = """
SELECT facility_id
FROM tbl_facility_information
WHERE facility_type = 3
"""

centers = my_cursor.execute(sql_string).fetchall()
centers = [s[0] for s in centers]

#months
sql_string = """
SELECT month_id
FROM tbl_dealer_demand
"""

months = my_cursor.execute(sql_string).fetchall()
months = set([m[0] for m in months])


#Manufacturing cost - Mc,p,l
sql_string = """
SELECT car_id, facility_id, line_id, cost
FROM tbl_production_line_data
"""

raw_data = my_cursor.execute(sql_string).fetchall()
manu_cost = {(c,p,l):cost for c,p,l,cost in raw_data}
print(len(manu_cost))

sql_string = """
SELECT facility_id, line_id, car_id
FROM tbl_production_line_data
"""
raw_data = my_cursor.execute(sql_string).fetchall()
build_cost = grb.tuplelist(raw_data)

#Rail rate - Rp,s
sql_string = """
SELECT p.facility_id, s.facility_id, t.rate
FROM tbl_facility_information p, tbl_facility_information s, tbl_transportation_data t
WHERE p.facility_type == 1 AND s.facility_type == 3 AND t.origin_id == p.facility_country AND t.destination_id == s.facility_country AND t.mode_id == 2
"""
raw_data = my_cursor.execute(sql_string).fetchall()
print(raw_data)

rail_rate = {(p,s):rate for p,s,rate in raw_data}

#Road rate - Os,d
sql_string = """
SELECT s.facility_id, d.facility_id, t.rate
FROM tbl_facility_information s, tbl_facility_information d, tbl_transportation_data t
WHERE s.facility_type == 3 AND d.facility_type == 2 AND t.origin_id == s.facility_country AND t.destination_id == d.facility_country AND t.mode_id == 1
"""
raw_data = my_cursor.execute(sql_string).fetchall()
print(raw_data)

road_rate_sd = {(s,d):rate for s,d,rate in raw_data}

#Road rate - Op,d
sql_string = """
SELECT p.facility_id, d.facility_id, t.rate
FROM tbl_facility_information p, tbl_facility_information d, tbl_transportation_data t
WHERE p.facility_type == 1 AND d.facility_type == 2 AND t.origin_id == p.facility_country AND t.destination_id == d.facility_country AND t.mode_id == 1
"""

raw_data = my_cursor.execute(sql_string).fetchall()
print(raw_data)

road_rate_pd = {(p,d):rate for p,d,rate in raw_data}

#Distance between facilities - 
#From plant to staging center - Np,s
sql_string = """
SELECT p.facility_id, s.facility_id, t.distance
FROM tbl_facility_information p, tbl_facility_information s, tbl_distance t
WHERE p.facility_type == 1 AND s.facility_type == 3 AND p.facility_id == t.origin_id AND s.facility_id == t.destination_id
"""

raw_data = my_cursor.execute(sql_string).fetchall()
print(raw_data)

distance_ps = {(p,s):distance for p,s,distance in raw_data}
print(distance_ps)

#From staging center to dealer - Ns,d
sql_string = """
SELECT s.facility_id, d.facility_id, t.distance
FROM tbl_facility_information s, tbl_facility_information d, tbl_distance t
WHERE s.facility_type == 3 AND d.facility_type == 2 AND s.facility_id == t.origin_id AND d.facility_id == t.destination_id
"""
raw_data = my_cursor.execute(sql_string).fetchall()
print(raw_data)

distance_sd = {(s,d):distance for s,d,distance in raw_data}

#From plant to dealer - Np,d
sql_string = """
SELECT p.facility_id, d.facility_id, t.distance
FROM tbl_facility_information p, tbl_facility_information d, tbl_distance t
WHERE p.facility_type == 1 AND d.facility_type == 2 AND p.facility_id == t.origin_id AND d.facility_id == t.destination_id
"""
raw_data = my_cursor.execute(sql_string).fetchall()
print(raw_data)

distance_pd = {(p,d):distance for p,d,distance in raw_data}

#Tariff cost Tc,p,d
sql_string = """
SELECT t.car_id, p.facility_id, d.facility_id, t.tariff
FROM tbl_facility_information p, tbl_facility_information d, tbl_tariff_data t
WHERE p.facility_type == 1 AND d.facility_type == 2 AND p.facility_country == t.origin_id AND d.facility_country == t.destination_id
"""
raw_data = my_cursor.execute(sql_string).fetchall()
print(len(raw_data))
#print(raw_data)

tariff_pd = {(c,p,d):tariff for c,p,d,tariff in raw_data}


#Tariff cost Tc,s,d
sql_string = """
SELECT t.car_id, s.facility_id, d.facility_id, t.tariff
FROM tbl_facility_information s, tbl_facility_information d, tbl_tariff_data t
WHERE s.facility_type == 3 AND d.facility_type == 2 AND s.facility_country == t.origin_id AND d.facility_country == t.destination_id
"""
raw_data = my_cursor.execute(sql_string).fetchall()
print(len(raw_data))
print(raw_data)

tariff_sd = {(c,s,d):tariff for c,s,d,tariff in raw_data}
print(tariff_sd)
print(len(tariff_sd))


#Retool cost - Bp,l
sql_string = """
SELECT factory_id, production_line, retool_cost
FROM tbl_factory_data
"""
raw_data = my_cursor.execute(sql_string).fetchall()
print(raw_data)

retool_cost = {(p,l):cost for p,l,cost in raw_data}

#Retool time - Fp,l
sql_string = """
SELECT factory_id, production_line, retool_time
FROM tbl_factory_data
"""
raw_data = my_cursor.execute(sql_string).fetchall()
print(raw_data)

retool_time = {(p,l):time for p,l,time in raw_data}

#Staging rate for staging center s - Gs
sql_string = """
SELECT staging_id, storage_rate
FROM tbl_staging_data
"""
raw_data = my_cursor.execute(sql_string).fetchall()
print(raw_data)

staging_rate_s = {s:rate for s,rate in raw_data}
print(staging_rate_s)

#Storage rate dealer d - Gd
sql_string = """
SELECT dealer_id, staging_rate
FROM tbl_dealer_data
"""
raw_data = my_cursor.execute(sql_string).fetchall()
print(raw_data)

staging_rate_d = {d:rate for d,rate in raw_data}

#capacities
#dealer storage capacity - Jd
sql_string = """
SELECT dealer_id, capacity
FROM tbl_dealer_data
"""
raw_data = my_cursor.execute(sql_string).fetchall()
print(raw_data)

capacity_d = {d:c for d,c in raw_data}

#staging center storage capacity - Js
sql_string = """
SELECT staging_id, capacity
FROM tbl_staging_data
"""
raw_data = my_cursor.execute(sql_string).fetchall()
print(raw_data)

capacity_s = {s:c for s,c in raw_data}

#plant production capacity - Hp,l
sql_string = """
SELECT factory_id, production_line, capacity
FROM tbl_factory_data
"""
raw_data = my_cursor.execute(sql_string).fetchall()
print(raw_data)

capacity_pl = {(p,l):c for p,l,c in raw_data}

#Dealer demand = Ed,c,m 
sql_string = """
SELECT *
FROM tbl_dealer_demand
"""

raw_data = my_cursor.execute(sql_string).fetchall()
print(raw_data)

demand = {(d,c,m):demand for d,c,m,demand in raw_data}

#initial inventory - dealers Id,c,0
sql_string = """
SELECT i.facility_id, i.car_id, i.on_hand
FROM tbl_initial_inventory i, tbl_facility_information f
WHERE i.facility_id = f.facility_id AND f.facility_type = 2
"""
raw_data = my_cursor.execute(sql_string).fetchall()
print(raw_data)
print(len(raw_data))

init_inv_d = {(d,c):o for d,c,o in raw_data}

#initial inventory - staging centers Is,c,0
sql_string = """
SELECT i.facility_id, i.car_id, i.on_hand
FROM tbl_initial_inventory i, tbl_facility_information f
WHERE i.facility_id = f.facility_id AND f.facility_type = 3
"""
raw_data = my_cursor.execute(sql_string).fetchall()
print(raw_data)
print(len(raw_data))

init_inv_s = {(s,c):o for s,c,o in raw_data}
print(init_inv_s)

#only plant/line combos that exist 

sql_string = """
SELECT DISTINCT facility_id, line_id
FROM tbl_production_line_data
"""
raw_data = my_cursor.execute(sql_string).fetchall()
print(len(raw_data))
print(raw_data)

pl_tuple = grb.tuplelist(raw_data)


#create model 
charb_auto = grb.Model()
charb_auto.modelSense = grb.GRB.MINIMIZE
charb_auto.update()

#Create the variables 
#Xc,p,l,s,m
#Tuplelist

sql_string = """
SELECT p.car_id, p.facility_id, p.line_id, s.staging_id
FROM tbl_production_line_data p, tbl_staging_data s
"""
raw_data = my_cursor.execute(sql_string).fetchall()
Xtuple = grb.tuplelist(raw_data)
print(len(Xtuple))


Xflow = {}
X_edges = []

for c in cars:
    for p,l in pl_tuple:
        for s in centers:
            for m in months:
                try:
                    build_cost = manu_cost[c,p,l]
                except:
                    build_cost = 1000000
                X_edges.append((c,p,l,s,m))
                total_cost = build_cost + rail_rate[p,s]*distance_ps[p,s]
                Xflow[c,p,l,s,m] = charb_auto.addVar(obj = total_cost,
                                                 vtype = grb.GRB.INTEGER,
                                                 name = f"Xflow({c},{p},{l},{s},{m})")

charb_auto.update() 
X_edges = grb.tuplelist(X_edges)

#Yc,s,d,m


Yflow = {}
Y_edges = []

for c in cars:
    for s in centers:
        for d in dealers:
            for m in months:
                try:
                    tariff_cost = tariff_sd[c,s,d]
                except:
                    tariff_cost = 0
                Y_edges.append((c,s,d,m))
                total_cost = road_rate_sd[s,d]*distance_sd[s,d] + tariff_cost
                Yflow[c,s,d,m] = charb_auto.addVar(obj = total_cost,
                                           vtype = grb.GRB.INTEGER,
                                           name = f"Yflow({c},{s},{d},{m})")
charb_auto.update() 
Y_edges = grb.tuplelist(Y_edges)     
         
#Zc,p,l,d,m
sql_string = """
SELECT DISTINCT p.car_id, p.facility_id, p.line_id, d.dealer_id
FROM tbl_production_line_data p, tbl_dealer_demand d
WHERE p.car_id == d.car_id
"""

raw_data = my_cursor.execute(sql_string).fetchall()
print(len(raw_data))
Ztuple = grb.tuplelist(raw_data)
print(len(Ztuple))


Zflow = {}
Z_edges = []

for c in cars:
    for p,l in pl_tuple:
        for d in dealers:
            for m in months:
                try:
                    build_cost = manu_cost[c,p,l]
                except:
                    build_cost = 1000000
                try:
                    tariff_cost = tariff_pd[c,p,d]
                except:
                    tariff_cost = 0 
                Z_edges.append((c,p,l,d,m))
                total_cost = build_cost + road_rate_pd[p,d]*distance_pd[p,d] + tariff_cost
                Zflow[c,p,l,d,m] = charb_auto.addVar(obj = total_cost,
                                                 vtype = grb.GRB.INTEGER,
                                                 name = f"Zflow({c},{p},{l},{d},{m})")
            
charb_auto.update() 
Z_edges = grb.tuplelist(Z_edges)                 

#ISc,s,m

InvS = {}
Is_edges = []

for c in cars:
    for s in centers:
        for m in months:
            Is_edges.append((c,s,m))
            InvS[c,s,m] = charb_auto.addVar(obj = staging_rate_s[s],
                                            vtype = grb.GRB.INTEGER, 
                                            name = f"Inventory_Center_({c},{s},{m})")

charb_auto.update() 
Is_edges = grb.tuplelist(Is_edges)     

        
#IDc,d,m
InvD = {}
Id_edges = []

for c in cars:
    for d in dealers:
        for m in months:
            Id_edges.append((c,d,m))
            InvD[c,d,m] = charb_auto.addVar(obj = staging_rate_d[d],
                                            vtype = grb.GRB.INTEGER, 
                                            name = f"Inventory_Dealer_({c},{d},{m})")
        
charb_auto.update() 
Id_edges = grb.tuplelist(Id_edges)  

#Ac,p,l,m
A_var = {}
A_edges = []

for c in cars:
    for p,l in pl_tuple:
        for m in months:
            A_edges.append((c,p,l,m))
            A_var[c,p,l,m] = charb_auto.addVar(obj = 0,
                                           vtype = grb.GRB.BINARY, 
                                           name = f"Production({c},{p},{l},{m})")
                                                                             
charb_auto.update() 
A_edges = grb.tuplelist(A_edges)                                           
        

#Tp,l,m
T_var = {}
T_edges = []

for p,l in pl_tuple:
    for m in months:
        try:
            retool = retool_cost[p,l]
        except:
            retool = 1000000
        T_edges.append((p,l,m))
        T_var[p,l,m] = charb_auto.addVar(obj = retool,
                                           vtype = grb.GRB.BINARY, 
                                           name = f"Retool({p},{l},{m})")
                                                                             
charb_auto.update() 
T_edges = grb.tuplelist(T_edges)                                           


##Constraints 

my_constrs = {}

#Inventory and Dealer Demand

sql_string = """
SELECT car_id, dealer_id, month_id 
FROM tbl_dealer_demand
"""

raw_data = my_cursor.execute(sql_string).fetchall()

demand_cdm = grb.tuplelist(raw_data)

for c,d,m in demand_cdm:
    try:
        Inventory = InvD[c,d,m-1]
    except:
        Inventory = init_inv_d[d,c]
    c_name = f"dealer_demand({c},{d},{m})"
    my_constrs[c_name] = charb_auto.addConstr(
                grb.quicksum(Yflow[c,s,d,m] for c,s,d,m in Y_edges.select(c,'*',d,m)) +  
                grb.quicksum(Zflow[c,p,l,d,m] for c,p,l,d,m in Z_edges.select(c,'*','*',d,m)) + Inventory
                             == demand[d,c,m] + InvD[c,d,m], name = c_name)

charb_auto.update()   

#Staging Center Inventory 
for c,s,m in Is_edges:
    try:
        Inventory = InvS[c,d,m-1]
    except:
        Inventory = init_inv_s[s,c]
    c_name = f"Center_Inventory({c},{s},{m})"
    my_constrs[c_name] = charb_auto.addConstr(grb.quicksum(Xflow[c,p,l,s,m] for c,p,l,s,m in X_edges.select(c,'*','*',s,m)) + Inventory == 
                                              grb.quicksum(Yflow[c,s,d,m] for c,s,d,m in Y_edges.select(c,s,'*',m)) + InvS[c,s,m], name = c_name)

charb_auto.update()  

#Pay retooling cost 

for c,p,l,m in A_edges:
    try:
        A_initial = A_var[c,p,l,m-1]
    except:
        A_initial = 0
    try:
        T_initial = T_var[p,l,m]
    except:
        T_initial = 0
    c_name = f"Pay_retool_cost({c},{p},{l},{m})"
    my_constrs[c_name] = charb_auto.addConstr(A_var[c,p,l,m]-A_initial <= T_initial, name = c_name)

charb_auto.update() 

#Only make one car per line per month 
for p,l,m in T_edges:
    c_name = f"Only_make_one_car_per_month({c},{p},{l},{m})"
    my_constrs[c_name] = charb_auto.addConstr(grb.quicksum(A_var[c,p,l,m] for c,p,l,m in A_edges.select('*',p,l,m)) <= 1, name = c_name)

charb_auto.update() 

#Can only produce car that line is tooled for 
for c in cars:
    for p,l in pl_tuple:
        for m in months:
            c_name = f"produce_car_line_is_tooled_for({c},{p},{l},{m})"
            my_constrs[c_name] = charb_auto.addConstr(grb.quicksum(Xflow[c,p,l,s,m] for c,p,l,s,m in X_edges.select(c,p,l,'*',m)) + 
                                                grb.quicksum(Zflow[c,p,l,d,m] for c,p,l,d,m in Z_edges.select(c,p,l,'*',m))
                                              <= capacity_pl[p,l]*A_var[c,p,l,m], name = c_name)

charb_auto.update() 

#Plant capacity/retool time 

for p,l in pl_tuple:
    for c in cars:
        for m in months:
            c_name = f"retool_time({p},{l},{m})"
            my_constrs[c_name] = charb_auto.addConstr(grb.quicksum(Xflow[c,p,l,s,m] for c,p,l,s,m in X_edges.select(c,p,l,'*',m)) + 
                                             grb.quicksum(Zflow[c,p,l,d,m] for c,p,l,d,m in Z_edges.select(c,p,l,'*',m)) <= 
                                             capacity_pl[p,l]*((1-retool_time[p,l])*T_var[p,l,m]), name = c_name)
    
charb_auto.update()   

#Dealer storage capacity 
for d in dealers:
    for m in months:
        c_name = f"dealer_capacity({d},{m})"
        my_constrs[c_name] = charb_auto.addConstr(grb.quicksum(InvD[c,d,m] for c,d,m in Id_edges.select('*',d,m)) <= capacity_d[d], name = c_name)
        
charb_auto.update()   
                                                  

#Staging center storage capacity 
for s in centers:
    for m in months:
        c_name = f"staging_center_capacity({s},{m})"
        my_constrs[c_name] = charb_auto.addConstr(grb.quicksum(InvS[c,s,m] for c,s,m in Is_edges.select('*',s,m)) <= capacity_s[s], name = c_name)
           
charb_auto.update()    

##Soft constraints

#limit retooling to 2x per year 
Pen01 = {}
for p in plants:
    for l in lines:
        Pen01[p,l] = charb_auto.addVar(obj = 250000, 
                                       vtype = grb.GRB.INTEGER,
                                       name = f"Penalty_01_({p},{l})")

charb_auto.update() 

for p in plants:
    for l in lines:
        c_name = f"SC_01_limit_retooling_({p},{l})"
        my_constrs[c_name] = charb_auto.addConstr(grb.quicksum(T_var[p,l,m] for p,l,m in T_edges.select(p,l,'*')) <= 
                                                 2 + Pen01[p,l], 
                                                 name = c_name)
charb_auto.update()                                                  

#70% of cars sold in the US are built in the US 
#create Wc,s,d,m = cars moved from US staging centers to US dealers
sql_string = """
SELECT c.car_id, s.facility_id, d.facility_id
FROM tbl_lkup_car c, tbl_facility_information s, tbl_facility_information d
WHERE s.facility_type = 3 AND d.facility_type = 2 AND s.facility_country = 1 AND d.facility_country = 1
"""

raw_data = my_cursor.execute(sql_string).fetchall()
Wtuple = grb.tuplelist(raw_data)

W_edges = []
Wflow = {}

for c,s,d in Wtuple:
    for m in months:
        try:
            tariff = tariff_sd[c,s,d]
        except:
            tariff = 0
        W_edges.append((c,s,d,m))
        total_cost = road_rate_sd[s,d]*distance_sd[s,d] + tariff
        Wflow[c,s,d,m] = charb_auto.addVar(obj = total_cost,
                                           vtype = grb.GRB.INTEGER,
                                           name = f"Wflow({c},{s},{d},{m})")
        
charb_auto.update() 
W_edges = grb.tuplelist(W_edges) 

        
#create Vc,p,l,d,m = cars moved from US plants to US dealers    
sql_string = """
SELECT c.car_id, p.facility_id, l.production_line, d.facility_id
FROM tbl_lkup_car c, tbl_facility_information p, tbl_factory_data l, tbl_facility_information d
WHERE p.facility_id = l.factory_id AND p.facility_type = 1 AND d.facility_type = 2 AND p.facility_country = 1 AND d.facility_country = 1
""" 
 
raw_data = my_cursor.execute(sql_string).fetchall()   

Vtuple = grb.tuplelist(raw_data)

V_edges = []
Vflow = {}

for c,p,l,d in Vtuple:
    for m in months:
        V_edges.append((c,p,l,d,m))
        try:
            build_cost = manu_cost[c,p,l]
        except:
            build_cost = 0 
        total_cost = build_cost + road_rate_pd[p,d]*distance_pd[p,d] + tariff
        Vflow[c,p,l,d,m] = charb_auto.addVar(obj = total_cost,
                                                 vtype = grb.GRB.INTEGER,
                                                 name = f"Vflow({c},{p},{l},{d},{m})")

charb_auto.update() 
V_edges = grb.tuplelist(V_edges) 


Pen02 = {}
Pen02 = charb_auto.addVar(ub = .70,
                          obj = 1000000,
                          vtype = grb.GRB.CONTINUOUS, 
                          name = "Penalty_02")

try:
    dealer_demand = demand[c,d,m]
except:
    dealer_demand = 1
c_name = "SC_02_US_cars"
my_constrs[c_name] = charb_auto.addConstr((.75*grb.quicksum(Wflow[c,s,d,m] for c,s,d,m in W_edges.select('*','*','*','*')) + 
                                          grb.quicksum(Vflow[c,p,l,d,m] for c,p,l,d,m in V_edges.select('*','*','*','*','*')) +
                                          .75*grb.quicksum(InvD[c,d,m] for c,d,m in Id_edges.select('*','*',0)) /
                                          dealer_demand) >= .7-Pen02, 
                                          name = c_name)

charb_auto.update() 

#limit staging center capacity to 80%
Pen03 = {}
for s in centers:
    for m in months:
        Pen03[s,m] = charb_auto.addVar(obj = 3500,
                                       vtype = grb.GRB.BINARY,
                                       name = f"Penalty_03_({s},{m})")
        
charb_auto.update() 

for s in centers:
    for m in months:
        c_name = f"SC_03_staging_capacity_80({s},{m})"
        my_constrs[c_name] = charb_auto.addConstr(grb.quicksum(Xflow[c,p,l,s,m] for c,p,l,s,m in X_edges.select('*','*','*',s,m)) - 
                                                  grb.quicksum(Yflow[c,s,d,m] for c,s,d,m in Y_edges.select('*',s,'*',m)) + 
                                                  grb.quicksum(InvS[c,d,m-1] for c,d,m in Is_edges.select('*',d,m))
                                                  <= capacity_s[s]*(.8 + .2*Pen03[s,m]))
charb_auto.update() 

#limit staging center capacity to 90%
Pen04 = {}
for s in centers:
    for m in months:
        Pen04[s,m] = charb_auto.addVar(obj = 7500,
                                       vtype = grb.GRB.BINARY,
                                       name = f"Penalty_04_{s},{m}")
charb_auto.update() 

for s in centers:
    for m in months:
        c_name = f"SC_04_staging_capacity_90({s},{m})"
        my_constrs[c_name] = charb_auto.addConstr(grb.quicksum(Xflow[c,p,l,s,m] for c,p,l,s,m in X_edges.select('*','*','*',s,m)) - 
                                                  grb.quicksum(Yflow[c,s,d,m] for c,s,d,m in Y_edges.select('*',s,'*',m)) + 
                                                  grb.quicksum(InvS[c,d,m-1] for c,d,m in Is_edges.select('*',d,m))
                                                  <= capacity_s[s]*(.9 + .1*Pen04[s,m]))
charb_auto.update()                                         


#charb_auto.read('Perfect_solution.mst')
charb_auto.setParam('MIPFocus',1)
charb_auto.setParam('TimeLimit',172800)

charb_auto.write("charb_auto.lp")

charb_auto.optimize()
charb_auto.write('Perfect_solution.mst')

print(Xflow.items())

print(Yflow.items())

print(charb_auto.status())

status = print(charb_auto.status())


X_sol = []
Y_sol = []
Z_sol = []
A_sol = []
T_sol = []
for k,v in Xflow.items():
    if v.x != 0:
        X_sol.append((str(k),v.x))
for k,v in Yflow.items():
    if v.x != 0:
        Y_sol.append((str(k),v.x))
for k,v in Zflow.items():
    if v.x != 0:
        Z_sol.append((str(k),v.x))
for k,v in A_var.items():
    if v.x == 1:
        A_sol.append((str(k), v.x))
for k,v in T_var.items():
    if v.x == 1:
        T_sol.append((str(k),v.x))       
            
        
sql_string = """
        CREATE TABLE IF NOT EXISTS X_solutions (
        cplsm_combo text,
        cplsm_quantity int
        );
        """
my_cursor.execute(sql_string)
my_conn.commit()

sql_string = "DELETE FROM X_solutions;"
my_cursor.execute(sql_string)

my_cursor.executemany("INSERT INTO X_solutions VALUES (?,?);", X_sol)
my_conn.commit()

sql_string = """
        CREATE TABLE IF NOT EXISTS Y_solutions (
        csdm_combo text,
        csdm_quantity int
        );
        """
my_cursor.execute(sql_string)
my_conn.commit()

sql_string = "DELETE FROM Y_solutions;"
my_cursor.execute(sql_string)

my_cursor.executemany("INSERT INTO Y_solutions VALUES (?,?);", Y_sol)
my_conn.commit()

sql_string = """
        CREATE TABLE IF NOT EXISTS Z_solutions (
        cpldm_combo text,
        cpldm_quantity int
        );
        """
my_cursor.execute(sql_string)
my_conn.commit()

sql_string = "DELETE FROM Z_solutions;"
my_cursor.execute(sql_string)

my_cursor.executemany("INSERT INTO Z_solutions VALUES (?,?);", Z_sol)
my_conn.commit()

#A means car c is produced on line l in month m 
sql_string = """
        CREATE TABLE IF NOT EXISTS A_var_solutions (
        cplm_combo_exists text,
        cplm_value int
        );
        """
my_cursor.execute(sql_string)
my_conn.commit()

sql_string = "DELETE FROM A_var_solutions;"
my_cursor.execute(sql_string)

my_cursor.executemany('INSERT INTO A_var_solutions VALUES (?,?);', A_sol)
my_conn.commit()


#T means plant p, line l is retooled in month m 
sql_string = """
        CREATE TABLE IF NOT EXISTS T_solutions (
        plm_combo text,
        plm_value int
        );
        """
my_cursor.execute(sql_string)
my_conn.commit()

sql_string = "DELETE FROM T_solutions;"
my_cursor.execute(sql_string)

my_cursor.executemany('INSERT INTO T_solutions VALUES (?,?);', T_sol)
my_conn.commit()




