# Charb-Auto-Dealer-Manufacturing-and-Distribution-plan-

Welcome to Charb-Auto, an international car manufacturer that has manufacturing plants and dealerships throughout North America. Charb-Auto has automobile manufacturing plants scattered over the US, CA, and MX. They view their operations as “continental” and any vehicle manufactured in any country can be sold at any of their dealerships through out North America.  Of course they must consider transportation costs from the manufacturing plant to the dealership.  Additionally, due to the absence of trading agreements on automobiles between some countries, there are tariffs imposed that must be included in the distribution chain.  Not all cars are manufactured at all plants.  Help Charb-Auto develop a distribution plan for the upcoming year that minimizes total cost (manufacture, tariff, and transportation).

The following soft constraints need to be incorporated into the model: 
- Charb-Auto would like a plant to limit retooling to no more than 2 times per year, the believe the wear and tear on the machinery during retooling results in $250,000 (amortized over the life of the machinery) if it is retooled more than twice a year.
- Due to political pressures in the US, Charb-Auto would like to make sure that 70% of the cars sold in the US are built in the US.  Note: For this formulation we didn’t track from which country a car originated once it is in the staging area, assume that 75% of all cars in US based staging areas are built in the US and that no cars in staging areas in CA and MX were made in the US
- Charb-Auto would like staging areas to not exceed 80% capacity in any month.  It requires additional security officers to staff the lots.  It costs Charb-Auto $3,500 per month each time they exceed 80%
- Charb-Auto really does not want to exceed 90% per month at its lots because then they need to bring in an extra security guard (a second one on top of what they needed when they exceeded 80%), and due to union rules, they also need to bring in a security manager.  The cost for the extra security officer is $3,500 and the cost for the additional manager is $4,000.  

The following files are needed for use in the development of this model:
- dealer_demand.csv: The annual demand for each car type (dealer name, car type, annual demand)
- dealer_inforamtion.csv:  The information associated with each dealership (name, city, country, location, annual demand per vehicle type)
- manufacture_data.csv:  The cost to manufacture each vehicle in each country (plant name, car type, hours to manufacture each car, cost to manufacture each car)
- plant_data.csv: The information associated with each manufacturing plant (name, city, country, location, and total manufacturing capacity in hours)
- road_transportation_costs.csv:  The information associated with transporting vehicles from manufacturer to dealership (origin country, destination country, cost/vehicle/mile) 
- tariffs.csv: the country to country tariffs for each vehicle type (origin country, destination country, cost/vehicle)

The code will: 
- Load the raw data (inputs) into a mysqsl database. Use scripts to both create the database and to populate them 
- Build a Gurobi optimization model by reading in the data from the database and formulating a feasible model that minimizes the cost for Charb-Auto
- Write the solution to a table in the database as well as output the solution to the screen 
