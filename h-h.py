## this is the first try for h-h program for csc8311
from math import exp
import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
from tqdm import tqdm


# creating classes for alpha and beta
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


class Conductance:
    def __init__(self, num):
        self.num = num

    def gnmh_k(self):
        return g_k * (x[0] ** 4)

    def gnmh_na(self):
        return g_na * ((x[1] ** 3) * x[2])

    def gnmh_r(self):
        return g_r


print("welcome to the hodgkin-huxley graph generator")

print("this aims to simulate neuron potential over time")

# set constant values for maximal conductances of potassium, sodium and rest

g_k = 36  # maximal conductance of potassium in mS/cm^2
g_na = 120  # same as above for sodium
g_r = 0.3  # same as above for r

# set voltages for m, n and h
e = [-12, 115, 10.613]


# external input - to be input by user
i_ext = None
while i_ext is None:
    try:
        i_ext = int(input("what is the external input to the neuron, please input a zero or positive integer ?"))
    except ValueError:
        print("Sorry '{}' is not 0 or a positive integer ".format(i_ext))

while i_ext < 0:
    try:
        print("this is not a valid value for input current, please input a zero or positive integer")
        i_ext = int(input("what is the external input to the neuron?"))
    except ValueError:
        print(" sorry '{}' is not a positive".format(i_ext))

print("you have set the external input to", i_ext, "mV")

# resting potential of neuron - input by user
mem_pot = None
while mem_pot is None:
    try:
        mem_pot = int(input("what is the neuron resting potential? Please make this a zero or negative integer"))
    except ValueError:
        print("Sorry,'{}' is not 0 or a negative integer ".format(mem_pot))

while mem_pot > 0:
    try:
        print ("You have input a positive integer, please input zero or negative integer")
        mem_pot = int(input("what is the neuron resting potential? Please make this a zero or negative integer"))
    #print("you have set the membrane resting potential to", mem_pot, "mv")
    except ValueError:
        print("Sorry, '{}' is not 0 a negative integer ".format(mem_pot))

print("you have set the membrane resting potential to", mem_pot, "mv")


if __name__ == "__main__":


    # initialization of some variables
    t_step = 0.001
    t = sc.arange(0, 15, step=t_step)  # the time is to go from 0 to 15 in steps of t_step
    x_0 = [None]*3  # empty list for x_0
    x = [0, 0, 1]  # initial
    gnmh = [None]*3  # empty list for gnmh
    tau = [None]*3
    mem_pot = mem_pot
    potential = np.array(mem_pot)
    current_time = 0
    time = np.array(current_time)
    threshold = -55
    # time step for the eular integration method
    t_step = 0.001

    for i in tqdm(t):

        #if t.any() == 10:
         #   i_ext = 5  # starts the external current at time 10
        #elif t.any() == 40:  # stops the external current at time 40
         #   i_ext = 0
        #else:

        # h-h alpha functions- assign values to empty list above
        a = Alpha(mem_pot)
        alpha = [a.alpha_a(), a.alpha_b(), a.alpha_c()]
            #print(alpha)

        # h-h beta functions -assign values to empty list above
        b = Beta(mem_pot)
        beta = [b.beta_a(), b.beta_b(), b.beta_c()]

        # tau and x_0 redefined with regards to alpha and beta
        a_b = [x + y for x, y in zip(alpha, beta)]  # element-wise summation of alpha and beta
        # print(a_b) #used for some debugging
        tau = [1 / x for x in a_b]
        # print(tau)
        x_0 = [x * y for x, y in zip(alpha, tau)]

            # leaky integration part---- work out how !!!
        x = (np.multiply((1 - (np.divide(t_step, tau))), x)) + np.multiply((np.divide(t_step, tau)), x_0)
            # x = (1 - dt /eldiv/ tau) *elmul* x + dt /eldiv/ tau *elmul* x_0
            # x = ((1 - t_step)/tau) * (x + (t_step/(tau * x_0)))

            # conductance calculations
        c = Conductance(x)
        gnmh = [c.gnmh_k(), c.gnmh_na(), c.gnmh_r() ]
            #gnmh[0] = g_k * (x[0] ** 4)
            #gnmh[1] = g_na * ((x[1] ** 3) * x[2])
            #gnmh[2] = g_r

            # ohms law for current
        minus = [mem_pot - x for x in e]
        current = [x * y for x, y in zip(gnmh, minus)]
            # update membrane potential
        if (mem_pot + i_ext) < threshold:
            mem_pot = mem_pot
        else:
            mem_pot = mem_pot + (t_step * (i_ext - sum(current)))
        potential = np.append(potential, mem_pot)

            # mem_pot = mem_pot + (t_step * (i_ext - sum(current)))
            # potential = np.append(potential, mem_pot)


            # storage of values needed for plotting graph
        for i in (t >= 0):
            current_time = current_time + 1
        time = np.append(time, current_time)
            # time = np.array(t)
            # time = np.array(t)
            # potential = np.array(mem_pot)





    fig, ax = plt.subplots()
    plt.axhline(y=threshold, linewidth=1, linestyle='dashed', color='k', label='firing threshold of neuron')
    ax.plot(time, potential)
    ax.set(xlabel="time", ylabel="membrane potential (mV)")
    fig.savefig("csc8311.png")
    plt.legend()
    plt.show()


print("finished")

