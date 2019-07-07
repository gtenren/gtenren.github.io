# EY Data Science Challenge

As a participant for EY Data Science Challenge 2019, this project aim to produce a model that helps authorties to understand the journey of citizens while they move in the city throughout the day. This allow authorities to introduce innovative infrastructure and policy to influence citizen mobility.

## Data

The data is collected through a 210000 mobile devices. For each device, there were multiple trajectories. An observation include the starting and ending point coordinate and the travel time of that trajectory. The last exit point is missing as the goal is to predict whether the exit point of a particular device will be in the target region at 15:00.

## Single Instance 

Based on the assumption that the last starting point has all the information about exit point, we only used the last trajectory of every device as our training data. 

## Instance Based Method

Instead of using the last trajectory as the representative of the device, we used a wrapper method that treated all the trajectories which last trajectory enters the target region as "positive", 'negative' otherwise. Then we used all instances as our input to train the model. 

## Bag Based Method

 For bag based approach, we summaries the instances within a bag basd on statistical method. The representative instance will then be used as input to train the model.

