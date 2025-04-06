READ.ME file for datasets related to pig registration information ("Exp? - Pig registrations all info combined.csv").
These datasets were created immediately following each of the four experiments, and were used to match this pig information with a range of other data.

An explanation of the columns:
- pig: The RFID number that identifies the pig.
- pig.short: Only in experiment 3. The RFID number ('pig') was generally long and hence for practical reasons made short in other files. 
- experiment: The experiment the pig was reared in, either 1, 2, 3 or 4.
- compartment: The room the pig was housed in, either A, B, C, D or F, matched with the experiment number (e.g. A.1 = compartment A, experiment 1).
- pen: The pen the pig was housed in, either 1 or 2, matched with the compartment and experiment numbers (e.g. A2.1 = compartment A, pen 2, experiment 1).
- bodyw_start: The body weight of the pig on the day or arrival at the farm
- station: The ID number of the IVOG feeding station that the pig had access to.
- bodyw_end: The body weight of the pig upon the final weighing, which was several days to weeks before slaughter. All pigs were weighed once, on the same day.
- bodyw_mid: Only for experiment 2. The body weight of the pig upon a weighing day in the middle of the growing-finishing phase.
- gender: The sex of the pig. Generally barrow or gilt, but sometimes barrows were not fully castrated.

Information on weighing days can be found in the 'On-farm observations' data files, tab 'Additional information'.
