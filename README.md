# queueSim
A Simple Queuing Model Simulation Using Python

This code simulates a model similar to M/M/C/FIFO queuing theory.

## Inputs are:
--Arrival_timestamp : [4, 10, 12, 20, ...] represents that customers reach the spot at 4, 10, 12, 20 successively (should be sorted).

--Serving_duration : [30, 20, 15, 54, ...] represents the time each customer spends at the spot (should be in the same order as the Arrival_timestamp).


## Outputs is a Dataframe consists of columns:

--id : ID of the customers

--arrival_time : the time when one customer arrives according to the input

--duration : how long one customer receiving service according to the input

--start_time : when certain customer starts receiving service (when he does not have to queue, it should be the same with arrival_time)

--end_time : start_time + duration

--stall_id : the counter id that the customer is assigned to in the system


Need to mention that this code is programmed under context of an optimization model of charging strategy for charging stations and electric vehicles. So you find the naming of some variables a bit weird.
