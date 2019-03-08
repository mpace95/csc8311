# this is a model of the hodgkin-huxley theory of neuron spiking
# The idea for this came from Fundamentals of Computational Neuroscience (Trappenberg, 2009).
# For those not familiar with this model and without access to the aforementioned book,
# this link provides a good explanation : "https://neuronaldynamics.epfl.ch/online/Ch2.S2.html".
# The current model takes in user input of the neuron resting potential,
# and the external input being injected to the neuron.
# The program passes these input variables into the Hodgkin-Huxley equations
# and produces  a time against membrane potential graph of the synapse.
# In this model the spike threshold of the neuron is set to -55mV


# before you run the code, ensure you have these things installed on your machine: matplotlib, numpy, tqdm, and scipy
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import scipy as sc


# creating classes for alpha and beta and the associated equations for alpha 1,2,3, and beta 1,2,3
class Alpha:
    def __init__(self, pot):
        self.pot = pot

    def alpha_a(self):
        return (10 - self.pot)/(100 * (np.exp((10 - self.pot)/10)-1))

    def alpha_b(self):
        return (25 - self.pot) / (10 * (np.exp((25 - self.pot) / 10) - 1))

    def alpha_c(self):
        return 0.07 * (np.exp((-self.pot)/20))


class Beta:
    def __init__(self, pot):
        self.pot = pot

    def beta_a(self):
        return 0.125*(np.exp((-self.pot)/80))

    def beta_b(self):
        return 4*np.exp((-self.pot)/18)

    def beta_c(self):
        return 1/(np.exp((30-self.pot)/10)+1)


# create a class for conductance and the calculations for conductance of:
# potassium channel (k), sodium channel(na) and resistance in the system(r)
class Conductance:
    def __init__(self, num):
        self.num = num

    def gnmh_k(self):
        return g_k * (x[0] ** 4)

    def gnmh_na(self):
        return g_na * ((x[1] ** 3) * x[2])

    def gnmh_r(self):
        return g_r


# welcoming user to the program
print("welcome to the hodgkin-huxley graph generator")
print("this aims to simulate neuron potential over time")

# set constant values for maximal conductances in mS/cm^2 of potassium, sodium and resistance
# these are known set constants from the literature
g_k = 36  # maximal conductance of potassium in mS/cm^2
g_na = 120  # same as above for sodium
g_r = 0.3  # same as above for r

# set voltages for m, n and h - these are he gating variables,
# possibility of channel being open at any one moment in time
e = [-12, 115, 10.613]

# external input (potential) to neuron - to be input by user
i_ext = None
while i_ext is None:
    try:
        """This ensures the user cannot pass on t next stage until a suitable integer for i_ext is given"""
        i_ext = int(input("what is the external input to the neuron, please input a zero or positive integer ?"))
    except ValueError:
        print("Sorry '{}' is not 0 or a positive integer ".format(i_ext))

while i_ext < 0:
    try:
        """This ensures the user passes in an external input greater than 0"""
        print("this is not a valid value for input current, please input a zero or positive integer")
        i_ext = int(input("what is the external input to the neuron?"))
    except ValueError:
        print(" sorry '{}' is not a positive".format(i_ext))

# remind user to what have set
print("you have set the external input to", i_ext, "mV")


# resting potential of neuron - input by user
mem_pot = None
while mem_pot is None:
    try:
        """Ensure the user inputs an integer for resting membrane potential"""
        mem_pot = int(input("what is the neuron resting potential? Please make this a zero or negative integer"))
    except ValueError:
        print("Sorry,'{}' is not 0 or a negative integer ".format(mem_pot))

while mem_pot > 0:
    try:
        """ensures the membrane potential is negative, as resting potential of neuron is never positive """
        print("You have input a positive integer, please input zero or negative integer")
        mem_pot = int(input("what is the neuron resting potential? Please make this a zero or negative integer"))
    except ValueError:
        print("Sorry, '{}' is not 0 a negative integer ".format(mem_pot))

# when user successfully entered a correct number for resting potential, remind them of input
print("you have set the membrane resting potential to", mem_pot, "mv")


# initialization of some variables
t_step = 0.001 # the time step for which Eular integration method is implemented - a data point for every 0.001s

# the time is to go from 0 to 15 in steps of t_step, 15 for run-time, information gain trade-off
t = sc.arange(0, 15, step=t_step)
x_0 = [None]*3  # empty list for x_0, asymptotic value
x = [0, 0, 1]  # initial gating variables
gnmh = [None]*3  # empty list for gnmh - conductances at beginning set to 0
tau = [None]*3  # initial time constants set to empty
mem_pot = mem_pot # initial membrane potential equal to user input number
potential = np.array(mem_pot)  # empty array to store potentials in for plotting
current_time = 0  # current time starts at 0
time = np.array(current_time)  # empty array to store time in for plotting
threshold = -55  # firing threshold of a neuron, -55mV is the norm from literature

if __name__ == "__main__":  # defining the main piece of code
    for i in tqdm(t):  # for all instances in time range (tqdm there for progress bar)

        # h-h alpha functions - assign values to empty list above
        a = Alpha(mem_pot)
        alpha = [a.alpha_a(), a.alpha_b(), a.alpha_c()]

        # h-h beta functions - assign values to empty list above
        b = Beta(mem_pot)
        beta = [b.beta_a(), b.beta_b(), b.beta_c()]

        # tau and x_0 redefined with regards to alpha and beta
        a_b = [x + y for x, y in zip(alpha, beta)]  # element-wise summation of alpha and beta
        tau = [1 / x for x in a_b]  # update tau - element wise division of 1 by each a_b
        x_0 = [x * y for x, y in zip(alpha, tau)]  # update x_0 - element wise multiplication of alpha and tau

        # leaky integration part, works out the leakage current of the neuron
        x = (np.multiply((1 - (np.divide(t_step, tau))), x)) + np.multiply((np.divide(t_step, tau)), x_0)

        # conductance calculations
        c = Conductance(x)
        gnmh = [c.gnmh_k(), c.gnmh_na(), c.gnmh_r()]

        # Using ohms law to work out the current in amps
        # split into 2 parts to simplify element wise processes
        minus = [mem_pot - x for x in e]
        current = [x * y for x, y in zip(gnmh, minus)]
            # update membrane potential
        if (mem_pot + i_ext) < threshold:
            """if the sum of membrane potential and external input does not meet threshold, 
            the neuron membrane potential will not change. No spike will be elicited"""
            mem_pot = mem_pot
        else:
            """if the sum of external and current potential meets threshold a spike will be elicited,
            and membrane potential will be updated"""
            mem_pot = mem_pot + (t_step * (i_ext - sum(current)))
        potential = np.append(potential, mem_pot)  # update store of potentials for plotting

        # update the current time
        for j in (t >= 0):
            """This updates the current time"""
            current_time = current_time + 1
        # add current time to store of times for plotting
        time = np.append(time, current_time)

    # plotting graph of the membrane potential over time
    fig, ax = plt.subplots()
    # add ine to show where spike threshold is
    plt.axhline(y=threshold, linewidth=1, linestyle='dashed', color='k', label='firing threshold of neuron')
    # plot line for time against potential
    ax.plot(time, potential)
    # label
    ax.set(xlabel="time", ylabel="membrane potential (mV)")
    # figure automatically saved under this name
    fig.savefig("csc8311.png")
    plt.legend()
    plt.show()  # graph should automatically pop-up in separate window

print("finished")
# finished is only printed when the graph has been closed down,
# otherwise the program is technically still running

