# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 22:46:08 2019

@author: Linh Pham Thi

"""
import datetime
from pvAsset import PVasset
import numpy as np

import random
from simulation import Simulation
import warnings
warnings.filterwarnings("ignore")


# =============================================================================
# Variables to change
# =============================================================================
""" Car and charging related """
slowcharge_ulim = 3         # kW charging upper limit
fastcharge_ulim = 7         # kW charging upper limit
rapidcharge_ulim = 50       # kW charging upper limit
end_SOC_req = 0.8           # The achievable SOC at leaving below which car is given charging priority
priority_limit = 0.8        
carnumber = 66              # cars/day
buschargelength = 0.25      # hour of charging for 1 bus
busnumber = 17              # bus / day, 17 corresponds to 1 bus/hour
vnumber = carnumber + busnumber     # Number of vehicles
""" Simulation related """
starttime = datetime.datetime(2020,1,1,6,0,0)        # Selected date for simulation, start time of simulation
endtime = datetime.datetime(2020,12,31,23,0)         # End time of simulation
time_increment = 24                              # [hours]
""" P&R operation related """
opentime = 6        # Opening time, hour
closetime = 23      # Closing time, hour
""" Finance related """
# Price of electricity, GPB per kWh
base=14.7
red_energy_cost = (base + 5.363)/100         # Base rate + DUOS charge           
amber_energy_cost = (base + 0.57)/100
green_energy_cost = (base + 0.452)/100
""" PV related (Nicole's code)"""
# Fixed values
pv_area = 1.956 * 0.992   # Area of one panel        
# Variable parameters
dt = 60/60              # Time period (hr)
pv_efficiency =0.18   # Efficiency of one panel (max 0.18, degrades with time)
pv_losses = 0.14        # Losses from wires/inverters/etc; 0.14 recommended by PVGIS
num_pv_bays=100
pv_number = num_pv_bays*15        # Total number of panels (max 4995, given 15 panels per 3-bay unit, 1000 bays total) 
# Generating an instance 
pv_capacity = pv_efficiency * pv_area #at max efficiency this is 0.35kW as manufacturer states
pv_site1 = PVasset(pv_capacity * pv_number * (1 - pv_losses))
#Initialise variables
grid_energy_needed = 0
pv_leftover_energy = 0
red_band_energy = 0
amber_band_energy = 0
green_band_energy = 0
pv_energy_available = 0
grid_energy_needed_day = 0
unused_pv_energy_day = 0
total_sold_energy = 0
total_PV_energy = 0
SOC_before_plot = list()
SOC_after_plot = list()
x_axis = list()     # An x axis containing the timestamps of the simulation
longs_x_axis = list() # An x axis containing the days for long simulations
grid_energy = list()
unused_pv_energy = list()
daily_grid_energy = list()
daily_unused_pv_energy = list()

def variable(eff,bays,dt):
    global time_increment,pv_site1,pv_capacity,pv_number,daily_unused_pv_energy,daily_grid_energy,unused_pv_energy,grid_energy,longs_x_axis,x_axis,SOC_after_plot,num_pv_bays,pv_efficiency, grid_energy_needed,pv_leftover_energy,pv_leftover_energy,red_band_energy,amber_band_energy,green_band_energy,pv_energy_available,grid_energy_needed_day,unused_pv_energy_day,total_sold_energy,total_PV_energy,SOC_before_plot

    pv_efficiency=eff
    num_pv_bays=bays
    pv_number = num_pv_bays*15        # Total number of panels (max 4995, given 15 panels per 3-bay unit, 1000 bays total) 
    # Generating an instance 
    pv_capacity = pv_efficiency * pv_area #at max efficiency this is 0.35kW as manufacturer states
    pv_site1 = PVasset(pv_capacity * pv_number * (1 - pv_losses))
    time_increment = dt
    grid_energy_needed = 0
    pv_leftover_energy = 0
    red_band_energy = 0
    amber_band_energy = 0
    green_band_energy = 0
    pv_energy_available = 0
    grid_energy_needed_day = 0
    unused_pv_energy_day = 0
    total_sold_energy = 0
    total_PV_energy = 0
    SOC_before_plot = list()
    SOC_after_plot = list()
    x_axis = list()     # An x axis containing the timestamps of the simulation
    longs_x_axis = list() # An x axis containing the days for long simulations
    grid_energy = list()
    unused_pv_energy = list()
    daily_grid_energy = list()
    daily_unused_pv_energy = list()
    
    return 



# =============================================================================
# From Charge Rate Balance
# =============================================================================
def chargeRateBalance (evbatt, simulation, solar_profile):
    global pv_leftover_energy
    # =========================================================================
    # Initialising variables
    # =========================================================================
    pv_energy_profile = solar_profile[simulation.PVrange_begin : simulation.PVrange_end]
    
    pv_energy_available = pv_energy_profile[simulation.current_hour]
    
    for n in range (1, vnumber + 1):
        evbatt["EV{0}".format(n)].chargerate = 0

    # =========================================================================
    # Determining chargerates
    # =========================================================================

    # Reset chargerate to zero if SOC is 1 or car left the site
    for n in range (1, vnumber + 1):
        if evbatt["EV{0}".format(n)].SOC >= 1 or evbatt["EV{0}".format(n)].present == 0:
            evbatt["EV{0}".format(n)].chargerate = 0
            evbatt["EV{0}".format(n)].rel_weigh = 0


    while pv_energy_available > 0:
        total_weigh = 0
        # =====================================================================
        # Terms for the weighted average
        # =====================================================================     
        for n in range (1, vnumber + 1):
            
            # If the charging port is already at its limit, give no weight, otherwise use parameters to determine weighting
            if evbatt["EV{0}".format(n)].chargerate == evbatt["EV{0}".format(n)].crlimit:
                evbatt["EV{0}".format(n)].rel_weigh = 0
            else:
                evbatt["EV{0}".format(n)].rel_weigh = evbatt["EV{0}".format(n)].fill / evbatt["EV{0}".format(n)].time

            # Set chargerate to zero if SOC is 1 or if car is not present at the site
            if evbatt["EV{0}".format(n)].SOC >= 1 or evbatt["EV{0}".format(n)].present == 0:
                evbatt["EV{0}".format(n)].chargerate = 0
                evbatt["EV{0}".format(n)].rel_weigh = 0

        x = 0
        y = 0
        for n in range (1, vnumber + 1):
            if evbatt["EV{0}".format(n)].present == 1 and evbatt["EV{0}".format(n)].need_maxcharge == 1\
               and evbatt["EV{0}".format(n)].SOC < 1:
                x += evbatt["EV{0}".format(n)].crlimit

            
        if x <= priority_limit * pv_energy_profile[simulation.current_hour]:
            if evbatt["EV{0}".format(n)].present == 1 and evbatt["EV{0}".format(n)].need_maxcharge == 1\
               and evbatt["EV{0}".format(n)].SOC < 1:
                evbatt["EV{0}".format(n)].chargerate = evbatt["EV{0}".format(n)].crlimit
                evbatt["EV{0}".format(n)].rel_weigh = 0
            
        for n in range (1, vnumber + 1):
            y += evbatt["EV{0}".format(n)].chargerate
            total_weigh = total_weigh + evbatt["EV{0}".format(n)].rel_weigh
            
        pv_energy_available = pv_energy_profile[simulation.current_hour] - y                

        total_weigh = total_weigh + evbatt["EV{0}".format(n)].rel_weigh
            
            
        # =====================================================================
        # Break out of the while loop if all of the charging ports can't be charging or is at their limit
        # =====================================================================         
        if total_weigh == 0 :
            # Integrate leftover PV energy during the day by using trapezoidal rule
            pv_leftover_energy += pv_energy_available * simulation.t_inc 

            pv_energy_available = pv_energy_profile[simulation.current_hour]
            for n in range (1, vnumber + 1):
                pv_energy_available = pv_energy_available - evbatt["EV{0}".format(n)].chargerate            
            
            break
            
        # =====================================================================
        # Calculating charging rates
        # =====================================================================  
        for n in range (1, vnumber + 1):
            # Calculating the chargerate with the weighted division on energy available
            evbatt["EV{0}".format(n)].chargerate = evbatt["EV{0}".format(n)].chargerate + (pv_energy_available * evbatt["EV{0}".format(n)].rel_weigh / total_weigh)
            
            # Implement restrictions on charging rates imposed by charging type
            evbatt["EV{0}".format(n)].chargerate = np.clip(evbatt["EV{0}".format(n)].chargerate, 0, evbatt["EV{0}".format(n)].crlimit)

            

        # =====================================================================
        # Calculating leftover energy after the clip
        # =====================================================================  
        total_chargerate = 0
        for n in range (1, vnumber + 1):
            total_chargerate += evbatt["EV{0}".format(n)].chargerate
        
        pv_energy_available = pv_energy_profile[simulation.current_hour] - total_chargerate
        
 
    return evbatt

# =============================================================================
# Datagen
# =============================================================================

def datagen(simulation):
    # Initializing variables
    evbatt = {}
    total_ev_demand = 0         # Total number of kWh of the batteries that need to 
                                # be filled
    total_inst_chargerate = 0   # The number of kW needed at the moment that - if
                                # sustained constantly, will change the cars fully
                                # by the time they leaves                       
    n = 1                       # extract one random sample from normal mixture distribution to give arrival time
    mu = [9, 17]                # means for arrival time
    sigma = [0.1,2.1]           # standard deviations for arrival time

    
    # Creating instances of the EV battery class
    for n in range(1,(carnumber + busnumber + 1)):

        # CAR instances
        Z = np.random.choice([0,1]) # latent variable
        if n <= carnumber:
                                                # Battery capacity        
            evbatt["EV{0}".format(n)]=EVbattery(np.random.gamma(5.66,7),\
                                                # State of charge
                                                np.clip(np.random.beta(2,1.7), 0, 1),\
                                                # Premium charging?
                                                random.choices([0, 1], weights = [95, 5], k = 1), \
                                                # Type of charging, 0 for slow, 1 for fast
                                                random.randint(0,1),\
                                                # Length of stay in hours
                                                np.random.normal(10,2.1),\
                                                # Time of arrival, year, month, day set in settings, hour and minute randomized
                                                datetime.datetime(simulation.current_datetime.year,simulation.current_datetime.month,\
                                                                  simulation.current_datetime.day,\
                                                                  int(np.clip(float(np.random.normal(mu[Z], sigma[Z], 1)),6,23)), \
                                                                  random.randint(0,59)))
        # BUS instances
        else: 
                                                # Battery capacity        
            evbatt["EV{0}".format(n)]=EVbattery(320,\
                                                # State of charge
                                                np.clip(random.gauss(0.5,0.15), 0, None),\
                                                # Premium charging?
                                                0, \
                                                # Type of charging, 0 for slow, 1 for fast
                                                2,\
                                                # Length of stay in hours
                                                buschargelength,\
                                                # Time of arrival, year, month, day set in settings, hour and minute randomized
                                                datetime.datetime(simulation.current_datetime.year,simulation.current_datetime.month,\
                                                                  simulation.current_datetime.day,5,0) + \
                                                                  datetime.timedelta (hours = (closetime - opentime) / busnumber) * (n - carnumber))

            total_ev_demand = total_ev_demand + evbatt["EV{0}".format(n)].fill
            total_inst_chargerate = total_inst_chargerate + evbatt["EV{0}".format(n)].avg_chargerate
    
    return evbatt, total_ev_demand, total_inst_chargerate

# =============================================================================
# 
# =============================================================================


class EVbattery:
    
    # =========================================================================
    # Initialising variables
    # =========================================================================
    def __init__(self, capacity, SOC, premium, chargetype, time, arrivaltime):

        # =====================================================================
        # Charging related
        # =====================================================================
        self.capacity = capacity  # kWh
        self.SOC = SOC  # proportion charged when arriving in P+R
        self.fill = self.capacity - self.capacity * self.SOC # kWh needed to completely fill battery
        self.chargetype = chargetype    # Type of charging (slow=0, fast=1, rapid=2)
        self.premium = premium          # Premium charging, i.e car is guaranteed to charge to 100% is physically possible
        
            # Charging rate limit
        if self.chargetype == 0:
            self.crlimit = slowcharge_ulim
        elif self.chargetype == 1:
            self.crlimit = fastcharge_ulim
        else:
            self.crlimit = rapidcharge_ulim

        # =====================================================================
        # Time related
        # =====================================================================
        self.time = time # length of time car will be parked in hours (driver inputs on arrival)
        self.arrivaltime = arrivaltime # When the car arrives in the day
        self.leavetime = arrivaltime + datetime.timedelta(hours = self.time)
        self.present = 0    # If a car is present in the parking lot at a particular time
        
        # =====================================================================
        # For the algorithm's use
        # =====================================================================
        self.avg_chargerate = self.fill / self.time

        self.grid_perm = 0          # If this value is 1, then the car has 'permission' to buy energy from the grid to charge
                                    # If this value is 0, then the car cannot demand extra energy from the grid

        # Minimum charge duration for leaving SOC to hit the requirement (80%)
        if self.premium == 0:
            self.min_charge_dur = datetime.timedelta(hours = (end_SOC_req - self.SOC)*self.capacity / self.crlimit)
        else:
            self.min_charge_dur = datetime.timedelta(hours = (1 - self.SOC) * self.capacity / self.crlimit)

        # Needs the maximum chargerate at all times when present?
        if self.time * self.crlimit <= (end_SOC_req - self.SOC)*self.capacity:
            self.need_maxcharge = 1
        else: 
            self.need_maxcharge = 0
        
    # =========================================================================
    # This function charges the car by updating the relevant parameters
    # =========================================================================
    def charge(self, simulation):
        
        self.fill = np.clip((self.fill - self.chargerate * simulation.t_inc), 0, self.capacity)

        self.SOC = np.clip((self.capacity - self.fill) / self.capacity, 0, 1) # This is the real expression to use for final program
        
        self.avg_chargerate = np.clip(self.fill / ((self.leavetime - simulation.current_datetime).total_seconds()/3600) , 0 , None)


    # =========================================================================
    # This function updates the car's status
    # =========================================================================
    def statusUpdate(self, simulation):
        
        # Present at the site or not
        if (self.arrivaltime <= simulation.current_datetime) and (simulation.current_datetime < self.leavetime):
            self.present = 1
        else:
            self.present = 0     

        # =====================================================================
        # Grid energy permission
        # =====================================================================     
        # If the car is not present then no grid energy demand
        if self.present == 0 :
            self.grid_perm = 0

        # If the car is present and need the maxinum chargerate or is a bus, then allow grid energy demand
        elif self.need_maxcharge == 1 or self.chargetype == 2:
            self.grid_perm = 1
            
        # If the car leaves before 7am then allow grid energy demand
        elif self.present == 1 and \
             datetime.time(self.leavetime.hour, self.leavetime.minute) <= datetime.time(7,0):
                 self.grid_perm = 1

        # If the car leaves between 7am and  4pm or it is the weekend, then only allow charging at (leavetime - min_charge_dur)
        elif datetime.time(self.leavetime.hour, self.leavetime.minute) <= datetime.time(16,0) or \
             simulation.current_date.weekday() > 4:
            if simulation.current_datetime >= (self.leavetime - self.min_charge_dur):
                self.grid_perm = 1
            else:
                self.grid_perm = 0


        # If the car leaves between 4pm and 7pm, then only allow charging at (4pm - min_chare_dur)
        elif datetime.time(self.leavetime.hour, self.leavetime.minute) <= datetime.time(19,0):
            if simulation.current_datetime >= datetime.datetime(simulation.current_datetime.year, simulation.current_datetime.month, \
                                                simulation.current_datetime.day, 16,0) - self.min_charge_dur:

                # No charging in the red band time           
                if simulation.current_datetime > datetime.datetime(simulation.current_datetime.year, simulation.current_datetime.month, \
                                                simulation.current_datetime.day, 16,0) and \
                    simulation.current_datetime < datetime.datetime(simulation.current_datetime.year, simulation.current_datetime.month, \
                                                simulation.current_datetime.day, 19,0):
                        self.grid_perm = 0
                else: 
                    self.grid_perm = 1
            else:
                self.grid_perm = 0
                
        # If the car leaves after 7pm, then only allow charging at (leavetime - min_charge_dur - 3 hours) to avoid red band zone
        elif datetime.time(self.leavetime.hour, self.leavetime.minute) >= datetime.time(19,0):
            if simulation.current_datetime >= self.leavetime - self.min_charge_dur - datetime.timedelta (hours = 3):

                # No charging in the red band time           
                if simulation.current_datetime > datetime.datetime(simulation.current_datetime.year, simulation.current_datetime.month, \
                                                simulation.current_datetime.day, 16,0) and \
                    simulation.current_datetime < datetime.datetime(simulation.current_datetime.year, simulation.current_datetime.month, \
                                                simulation.current_datetime.day, 19,0):
                        self.grid_perm = 0
                else: 
                    self.grid_perm = 1
            else:
                self.grid_perm = 0

        else: 
            self.grid_perm = 0


# =============================================================================
# Variables to change
# =============================================================================

def gridEnergyCalculator(evbatt, simulation):
    global grid_energy_needed,grid_energy_needed_day,red_band_energy,amber_band_energy,green_band_energy
    total_extra_energy_needed = 0
    
    for n in range (1, vnumber + 1):
        
        #======================================================================
        # Picking out the EVs that after the energy division are charging at a 
        # sub-optimal rate (less than the average charging rate) and buying in
        # energy from the grid to match that average charging rate.
        #
        # Conditions to buy from the grid:
        #   - charging rate less than it's charging limit
        #   - SOC less than 0.8, i.e our goal for the leaving SOC
        #   - the EV is present at the site
        #   - permission to buy from the grid
        #======================================================================      
        extra_energy_needed = 0
        
        if (evbatt["EV{0}".format(n)].chargerate < np.clip(evbatt["EV{0}".format(n)].avg_chargerate,0,evbatt["EV{0}".format(n)].crlimit)) \
           and (evbatt["EV{0}".format(n)].SOC < end_SOC_req) \
           and evbatt["EV{0}".format(n)].present == 1 \
           and evbatt["EV{0}".format(n)].grid_perm == 1:

               # If the car needs the max charge rate or is a premium charging, then buy enough from the grid to provide max charge rate
               if evbatt["EV{0}".format(n)].need_maxcharge == 1 or evbatt["EV{0}".format(n)].premium:
                   extra_energy_needed = evbatt["EV{0}".format(n)].crlimit - evbatt["EV{0}".format(n)].chargerate
                   evbatt["EV{0}".format(n)].chargerate = evbatt["EV{0}".format(n)].crlimit                   

               # Otherwise, buy enough to provide the average charge rate
               else:
                   extra_energy_needed = np.clip(evbatt["EV{0}".format(n)].avg_chargerate,0,evbatt["EV{0}".format(n)].crlimit) - evbatt["EV{0}".format(n)].chargerate
                   evbatt["EV{0}".format(n)].chargerate = np.clip(evbatt["EV{0}".format(n)].avg_chargerate,0,evbatt["EV{0}".format(n)].crlimit)
                 
        #======================================================================
        # Categorizing the energy used into the time bands for finance applications
        #======================================================================
        # Summing up total energy bought from the grid
        grid_energy_needed += extra_energy_needed * simulation.t_inc     # Goes towards total energy bought during the simulation
        grid_energy_needed_day += extra_energy_needed * simulation.t_inc # Goes towards total energy bought during the day
        total_extra_energy_needed += extra_energy_needed                    # Goes towards total energy bought during that time instant, mainly for visualising
        
        # Weekday
        if simulation.current_date.weekday() < 5:
            if simulation.current_time >= datetime.time(16,0) and simulation.current_time < datetime.time(19,0):
                red_band_energy += extra_energy_needed * simulation.t_inc
            elif (simulation.current_time >= datetime.time(7,0) and simulation.current_time < datetime.time(16,0)) \
                 or\
                 (simulation.current_time >= datetime.time(19,0) and simulation.current_time < datetime.time(23,0)):
                     amber_band_energy += extra_energy_needed * simulation.t_inc
            elif (simulation.current_time >= datetime.time(0,0) and simulation.current_time < datetime.time(7,0)) \
                 or\
                 simulation.current_time >= datetime.time(23,0):
                     green_band_energy += extra_energy_needed * simulation.t_inc
        
        # Weekend
        else: 
            green_band_energy += extra_energy_needed * simulation.t_inc
    

    return evbatt




# =============================================================================
# Show results of the simulation in tuple 0.total electricity sold 1.cost of buying from grid
# =============================================================================
def showResults(evbatt, simulation):  
    
    # =========================================================================
    # Print energy balance values
    # =========================================================================
    # Cost of energy
    energy_cost = red_band_energy * red_energy_cost \
                    + amber_band_energy * amber_energy_cost \
                    + green_band_energy * green_energy_cost
                    
    showResults=[int(np.around(total_sold_energy + grid_energy_needed)),int(energy_cost)]
    return showResults

def results():
    global total_sold_energy
    #=============================================================================
    # Set up simulation and PV
    # =============================================================================
    simulation = Simulation(starttime, endtime, time_increment)
    solar_profile = pv_site1.getOutput(dt)
        
    # =============================================================================
    # Simulation
    # =============================================================================
    
    while simulation.current_datetime < simulation.endtime:
        # =========================================================================
        # Generate a new set of data for every new day, add totals of last day to results
        # =========================================================================
        if simulation.current_date != simulation.last_date:
            evbatt, total_ev_demand, total_inst_chargerate = datagen(simulation)
            
            for n in range (1, vnumber + 1):
                evbatt["EV{0}".format(n)].statusUpdate(simulation)
            
    
            # Picks the range for solar profile corresponding to the day
            simulation.rangepick()
            
    
        # =========================================================================
        # Calculating distribution and buy from grid
        # =========================================================================
        evbatt = chargeRateBalance(evbatt, simulation, solar_profile)
        for n in range (1, vnumber + 1):
            total_sold_energy += evbatt["EV{0}".format(n)].chargerate * simulation.t_inc   
        
    #    for n in range (1, vnumber + 1):
    #            evbatt["EV{0}".format(n)].grid_perm = 1
        
        evbatt = gridEnergyCalculator(evbatt, simulation)
        
        # =========================================================================
        # Charging
        # =========================================================================
        for n in range (1, vnumber + 1):
            evbatt["EV{0}".format(n)].charge(simulation)
        
        # =========================================================================
        # Incrementing time
        # =========================================================================
        simulation.timeUpdate()
        
        for n in range (1, vnumber + 1):    
            evbatt["EV{0}".format(n)].statusUpdate(simulation)
        
    #total electricity sold
    #print(showResults(evbatt, simulation)[0])
    #cost of buying from grid
    #print(showResults(evbatt, simulation)[1])

    return showResults(evbatt, simulation)