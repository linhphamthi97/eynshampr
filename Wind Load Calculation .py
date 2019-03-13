GridRef = [443486,210189];
X = 450;         #choose it cause it's closer to that value on NA1
Y = 200;
Vbmap = 21.35;   #fundamental basic wind velocity before alt correction in m/s
A = 79.248;      #altitude in meters
Calt = 1+0.001*A; #altitude factor for height of structure above ground <10
Vbo = Vbmap*Calt; #Fundamental basic wind velocity

##There are 3 primary directinos of oreintation for the parking lots
Cdir1 = 0.73;    #Direction factor read off NA2.6 using angle -75 due south
Cdir2 = 0.8;     #Direction factor using -22 due south
Cdir3 = 0.73;    #Direction factor using -120 due south
##The optimal slope are 35, 38 and 35 degrees using PVGIS, use 35 for all
deg = 35;        #Optimal angle in degrees
deg_actual = 21.8#actual angle in degrees due to the height limits
    
Cseason = 1;      #Seasonal factor taken to be 1 since it's up all year

Vb1 = Cdir1 * Cseason * Vbo #basic wind velocity for orientation -75 and -120
Vb2 = Cdir2 * Cseason * Vbo #basic wind velocity for oreintation -22

##Calculating the height of the structure that the wind speed is taken at
L = 4.5;          #Minimum length of parking space
h1 = 2.2;         #Minimum height of structure
h2 = 4;           #Max height
z = (h1+h2)/2; #The 

Crough = 0.8035;  #Roughness factor for fetch >=100 km and structures at 5.5 m
Corog = 1;        #Orography factor taken at 1

Vm1 = Crough * Corog * Vb1; #mean wind velocity for -75 and -120 
Vm2 = Crough * Corog * Vb2; #mean wind velocity for -22

##The structure is situated in the country, so country terrain is selected
lvflat = 0.1990;  #a new term with turbulence factor incorperated in it

Ce = 1.6365;    #read off NA7 for z = 3.1, in country terrain
rho = 1.226     #air density in km/m^3
Qb1 = 1/2 * rho * Vm1**2; #basic velocity pressure for -75 and -120
Qb2 = 1/2 * rho * Vm2**2; #basic velocity pressure for -22
Qp1 = Ce * Qb1; #peak velocity pressure forces per unit area
Qp2 = Ce * Qb2;

#Pressure coefficients Cpe10 is used as loaded areas are bigger than 10m^2 
import numpy as np
import array as arr

#Max force per unit length of the structure is highest at the ones with length
# of 9 standard parking spaces 
Load0 = Qp2 / 21.6 *105.23;  #details in Logbook
Load = Load0 * 1.5;       #Safety factor of 1.5 is included
Load_Wind = Load * 7.5; #Load per unit slope length when viewed from the side
Angle = np.radians(deg_actual);#Converting angle of attack to radians

#First case where the wind load is in the same direcction as the vertical load
Load_Vert = np.cos(Angle)*Load_Wind;
Load_Hor = np.sin(Angle)*Load_Wind;

#Other Vertical loads
Load_V_sheet = 5*9.8;   #5kg per unit area metal sheet roofing
Unit_Area = 5.1264*7.5;#Area of one unit
Weight_Panels = 21*9.8;#Weight of one panel
Area_Panels = 1.956*0.992;  #Area of the chosen panels
No_Panels = Unit_Area/Area_Panels;#number of Panels can fit onto one unit of dimensions 7.5 x 5.1264
Load_V_Panels = Weight_Panels * No_Panels / Unit_Area;#Load of panels per unit area

Load_V_total = Load_V_Panels*7.5*1.5 + 1.5*0.5*Load_Vert + 1.35*Load_V_sheet*7.5;
Load_H_total = 1.5*Load_Hor;

#Structure Analysis Part
#the smallest beam I can use is the 
#126x76x13 and using pin-jointed frames for sake of simplicity. 

#As there are four 7.5 meter long members in parrallel, the middle two members
#will experience double the force.
UB_mass = 13; #kg per meter
Load_V_all = 5.1264*Load_V_total+1.5*(7.5*4+5.1264*2)*UB_mass*9.8;

#For shear stress calculations:
R_support = 0.5*(0.37*Load_V_total * 7.5 + 7.5*13*9.8); #Force experienced for the 
#two supports closer to the middle
