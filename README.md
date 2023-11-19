## BlazeCast

## Inspiration

Across the globe, wildfires have emerged as a pressing and relentless threat, intensified by a convergence of factors such as climate change, land use patterns, and increasingly unpredictable weather. These infernos ravage landscapes, jeopardize lives, and decimate ecosystems, leaving a trail of destruction in their wake. The urgency of the issue is compounded by the challenge of accurately predicting their erratic behavior, often resulting in delayed responses and exacerbated damages. Our solution steps in as a crucial game-changer by **leveraging AI to rapidly identify wildfire origins and predict their trajectories**. By amalgamating diverse data sets—from environmental factors to historical patterns—we empower authorities and communities with timely, accurate information. This enables proactive measures, swift response, and informed decisions, ultimately saving lives, protecting property, and mitigating the catastrophic aftermath of these natural disasters.
  
  

## What it does

BlazeCast takes in user input highlighting the initial wildfire emergence points. It then pulls real-time weather data including temperature, pressure, humidity, wind speed, elevation, etc, and feeds it into a custom machine-learning model. This model then predicts the spread of the fire and outputs that to show the user where they should be focusing disaster response resources.



## How we built it

We split BlazeCast into submodules that all came together to create the final product and its features.

**Live Weather Data**: This submodule specializes in making API calls to the VisualCrossing weather API and Google Maps elevation data API. Based on a 32x32 array of longitude and latitude coordinates of the selected piece of land given by the UI, it calls both APIs and returns a 3D array of 7x32x32 dimension. Along with this, data is super-sampled to work with the cache data to reduce API costs. Each array in this 3D array represents an attribute such as elevation, wind speed, or temperature.

**API Data Caching**: The API data caching is a JSON structure that stores API calls to limit repeated requests. When an API call is made, that data is saved to this JSON file and cross-referenced when the next API call is going to be made. Data is pulled instead of calling the API if it is available in the cache. This reduces costs and streamlines the efficiency of our project as a whole.

**Pre-Processing of Wildfire Dataset**: In this submodule, the wildfire dataset undergoes a series of preprocessing steps to make it suitable for training the machine learning model. This includes cleaning and formatting the data, handling missing values, and normalizing the features. Additionally, temporal aspects such as time of day, day of the week, and seasonal variations may enhance the model's predictive capabilities.

**Model Structure**: The model architecture is designed to effectively capture the spatiotemporal dependencies in the input data. It comprises a combination of convolutional layers for spatial feature extraction, recurrent layers or attention mechanisms for capturing temporal dependencies, and fully connected layers for overall pattern recognition.

**Model Training**: The model is trained using a pre-processed wildfire dataset. The training process involves optimizing the model's parameters using a suitable optimization algorithm, ADAM. The loss function is defined to quantify the disparity between the predicted and actual wildfire occurrence, and backpropagation is employed to adjust the model weights accordingly. The training set is split into training and validation sets to monitor the model's performance and prevent overfitting.

**User Interface**: The user interface uses leaflet in javascript to implement an interactive map for the user to highlight grid boxes for the wildfire location selection. The interface has four buttons for zoom functionality into a 32-kilometer by 32-kilometer area, grid creation to overlap on the map, user selection of select grid boxes for wildfire locations, and finalization of the map. 

**Model Input**: This module takes all of the input arrays from the live weather data module and converts them into individual grids to be predicted upon. The input is a 3D array of the latitude and longitude of an area that was selected as having a wildfire. This array is directly taken from the user interface.

**Model Output**: The model output is the result of running the input array through our machine-learning model. It is represented in the form of a map, highlighting areas where fire is likely to spread in the next hour.

## Challenges we ran into

- **Efficiently allocating API tokens**: We realized that canvassing a 64x64 kilometer area of land and getting real-time data for each cell requires a lot of API calls. One of our biggest issues was making this many calls when a lot of data was repeated. We solved this issue by implementing a caching system.

- **Training the model**: Training a model on over 4.7 million parameters requires a lot of GPU power. Training our model for 10 epochs was not only resource-intensive but also time-intensive. The training of this model was done using the Adam optimizer on Google's colab on an A100 GPU. Along with this, we made mistakes in dataset input and the overall training of the model which made it predict wrong after some training runs. 

- **Validating the accuracy of our model**: We also had to implement validation to monitor overfitting. This ensured that our model was trained correctly and would work for the use case intended.

- **Integrating all of the submodules, different data types**: Much of this project was split up and each team member was given responsibilities. However, optimizing all of the code and refactoring it to fit together at the end was a challenge we had to overcome.

## Accomplishments that we're proud of

- Training an original model from the ground up

- We extrapolated large amounts of data from multiple different APIs and combined them into one cohesive data structure

- We created an interactive UI that will work on current wildfires

- We created multiple sub-modules with specialized purposes and combined them into one product

## What we learned

- How to train a ML model using a variety of factors 

- Using natural language models to generate description

- Engineering specific prompts for desired results with Large Language Models

- Working in a software team with specific roles using branching and git

- Splitting up a big picture into multiple smaller workflows and assigning roles

## What's next for BlazeCast

- Longer training of machine learning model

- Larger training database

- Added data for vegetation and air pressure

- Rooftop reflectivity factor

- Time Lapse form video to show better visual of fire progression

- Automatic mobilization of disaster response resources based on calculated impact


