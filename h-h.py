### this is the first try for h-h program for csc8311
print("welcome to the hodgkin-huxley generator")

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

i_ext = input("what is the external input to the neuron ?")
print("You have set the external input to", i_ext)
type(i_ext)

# resting potential of neuron - input by user
rest_pot = input("what is the neuron resting potential? Please make this a zero or negative integer")
print("you have set the membrane resting potential to", rest_pot, "mv")

# initial time set to zero
current_time = 0

# set initial x values
x = [0, 0, 1]

# time step for the eular integration method
t_step = 0.01