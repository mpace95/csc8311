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
e = [-12, 115, 10.613]


# external input - to be input by user

i_ext = int(input("what is the external input to the neuron ?"))

# i_ext = 60  # set myself for now as input seems to still think it's type string
print("You have set the external input to", i_ext)
type(i_ext)

# resting potential of neuron - input by user
mem_pot = int(input("what is the neuron resting potential? Please make this a zero or negative integer"))
# mem_pot = -65  # set myself for now as input seems to still think it's type string
print("you have set the membrane resting potential to", mem_pot, "mv")

# initial time set to zero
current_time = 0

# set initial x values
# x = [0, 0, 1]

# time step for the eular integration method
t_step = 0.001

# Eular integration method

# Eular integration method


# attempting to make use of classes
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


# def integration(t_step, i_ext, rest_pot, e_n, e_m, w_h):
# taken out function definition for the moment - put back in or rearrange to make use of classes

t = sc.arange(0, 15, step=t_step)
alpha = [None]*3  # set empty list of alphas to change
beta = [None]*3  # set empty list of beta to change
x_0 = [None]*3  # empty list for x_0
x = [0, 0, 1]  # initial
gnmh = [None]*3  # empty list for gnmh
tau = [None]*3
mem_pot = mem_pot
potential = np.array(mem_pot)
current_time = 0
time = np.array(current_time)
threshold = -55

for i in t:
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
        gnmh[0] = g_k * (x[0] ** 4)
        gnmh[1] = g_na * ((x[1] ** 3) * x[2])
        gnmh[2] = g_r

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

