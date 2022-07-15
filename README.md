# Autonomous_boat_simulation

Simulation of a autonomous boat cleaning up patches of waste in the ocean. There are 3 different simulations carried out with the same surrounding scripts and functionalities (images, classes for boat and waste...) in order to make comparative testing to determine the best strategy:

* Simulation of the boat following a fixed path: Boat moves up and down panning the majority of the area looking for waste, which is being carried by the currents (main_boats_fixed.py).
* Simulation of the boat following current patterns to save energy (main_boats_hybrid.py)
* Simulation of garbage accumulation over time following determined current patterns

At the end of these simulations the final task is to compare the efficiency of both strategies, determining the amount of trash collected per unit of energy consumed, which was calculated by pixels moved by the boat.

Co-authors: Carolina Lopez Olmo
