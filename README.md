# csc8311
assignment for csc8311
A model of the Hodgkin-huxley neuron spike
This project uses the Hodgkin-huxley model of a neuron spike. The idea for this came from Fundamentals of Computational Neuroscience (Trappenberg, 2009). It takes in user input of the neuron resting potential, and the external input being injected to the neuron. The program passes these input variables into the Hodgkin-Huxley equations and produces  a time against membrane potential graph of the synapse. In this model the spike threshold of the neuron 

Getting started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

Prerequisites
You will need to install these things in order for the code to run successfully.
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm


What to input 
The program will prompt to put in a plausible value for external input potential to the neuron (a.k.a - a positive integer) and a plausible value for the resting membrane potential (most neurons have a resting potential of -65mV, but you are welcome to see what happens with other values). You can see that if you put in a higher external input (e.g. 200mv) you can see that multiple spikes will be initialized, but if the external input is lower - e.g 5 a spike may not be initialised. 

Example input and output 
Input example 1:
 Set i_ext = 30
 Set mem_pot = -65

this will result in the following output graph 
￼
Tests
Tests were not implemented in this case due to time restrictions, in future tests should be added.

Deployment
Run the h-h.py file and input relevant values for membrane potential and external input when prompted, after the loading bar indicates 100% the graph should appear and save automatically. 

Versioning
We use GitHub for versioning. For the versions available, see the commits on this repository https://github.com/mpace95/csc8311/commits/master.
