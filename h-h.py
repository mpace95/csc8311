### this is the first try for h-h program for csc8311
from math import exp
import matplotlib.pyplot as plt
import numpy as np
import scipy as sc

print("welcome to the hodgkin-huxley graph generator")

print("this aims to simulate neuron potential over time")

# set constant values for maximal conductances of potassium, sodium and rest

g_k = 36  # maximal conductance of potassium in mS/cm^2
g_na = 120  # same as above for sodium
g_r = 0.3  # same as above for r

# set voltages for m, n and h
e_n = (-12)
e_m = 115
e_h = 10.613


# external input - to be input by user

# i_ext = input("what is the external input to the neuron ?")

i_ext = 10  # set myself for now as input seems to still think it's type string
print("You have set the external input to", i_ext)
type(i_ext)

# resting potential of neuron - input by user
# rest_pot = input("what is the neuron resting potential? Please make this a zero or negative integer")
rest_pot = -10  # set myself for now as input seems to still think it's type string
print("you have set the membrane resting potential to", rest_pot, "mv")

# initial time set to zero
current_time = 0

# set initial x values
x = [0, 0, 1]

# time step for the eular integration method
t_step = 0.01

# Eular integration method



# def integration(t_step, i_ext, rest_pot, e_n, e_m, w_h):
# taken out function definition for the moment - put back in or rearrange to make use of classes

t = sc.arange(-30, 10, 0.01)
alpha = [None]*3 # set empty list of alphas to change
beta = [None]*3  # set empty list of beta to change
x_0 = [None]*3  # empty list for x_0
gnmh = [None]*3  # empty list for gnmh
tau = [None]*3
current_pot = rest_pot
for i in t[:]:
#for i in t:
    #if t(i) == 10:
     #       i_ext = 5  # starts the external current at time 10
    #elif t(i) == 40:  #stops the external current at time 40
     #   i_ext = 0

        # h-h alpha functions- assign values to empty list above
    alpha[0] = (10 - current_pot)/(100*(np.exp((10 - current_pot)/10)-1))
    alpha[1] = (25 - current_pot)/ (10*(np.exp((25 - current_pot)/10)-1))
    alpha[2] = 0.07 * np.exp((-rest_pot)/20)

        # h-h beta functions -assign values to empty list above
    beta[0] = 0.125 * np.exp((-current_pot)/80)
    beta[1] = 4 * (np.exp((- current_pot)/18))
    beta[2] = 1/(np.exp(((30 - current_pot)/10)+1))

    # tau and x_0 redefined with regards to alpha and beta
    a_b = [x + y for x, y in zip(alpha, beta)] # element-wise summation of alpha and beta
    #print(a_b) #used for some debugging
    tau = [1/x for x in a_b]
    x_0 = [x * y for x, y in zip(alpha, tau)]

    # leaky integration part
    #x[i] = ((1 - t_step)/tau[i]) * (x + (t_step/(tau[i] * x_0[q])))

        # conductance calculations
    gnmh[0] = g_k * (x[0]**4)
    gnmh[1] = g_na * ((x[1]**3) * x[2])
    gnmh[2] = g_r

        # ohms law for current

    current_n = gnmh[0] * (rest_pot - e_n)
    current_m = gnmh[1] * (rest_pot - e_m)
    current_h = gnmh[2] * (rest_pot - e_h)
    current_list = [current_n, current_m, current_h]
    current = sum(current_list)

        # update membrane potential
    current_pot = current_pot + (t_step * (i_ext - current))

        # storage of values needed for plotting graph
    for i in (t>0):
        current_time = current_time + 1
        x_plot = np.array(t)
        y_plot = np.array(current_pot)



plt.plot(x_plot, y_plot)



