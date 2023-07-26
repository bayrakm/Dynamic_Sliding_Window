# Dynamic Sliding Window


## Introduction

In our dynamic sliding window project, our aim is to create an efficient price prediction model that remains up-to-date by continuously adapting to changing data patterns. To achieve this, we implement the dynamic sliding window approach, a powerful technique that allows us to efficiently handle concept drift and maintain model validity over time. Through a series of carefully designed functions, we manage the data dynamically, ensuring timely updates and improved predictive accuracy. Let's explore the key functions utilized to achieve this task and evaluate the performance outcomes of the dynamic sliding window approach.

##### data_stratification():
To optimize the process of data division, the data_stratification() function plays a vital role. It divides the data into identical, stratified chunks based on specified columns and the desired number of chunks. This ensures a fair representation of the entire population in each chunk, minimizing the risk of biased evaluations during the modelling process.

##### eval_metrics():
To comprehensively assess model performance, the eval_metrics() function gathers all evaluation metrics into a convenient dataframe. It takes the actual and predicted values as inputs and calculates metrics such as R-squared, Mean Absolute Error (MAE), Mean Squared Error (MSE), and Root Mean Squared Error (RMSE). These metrics provide crucial insights into the model's accuracy and precision.

##### act_per_data():
The act_per_data() function is designed to calculate the percentage of Mean Absolute Error (% of MAE) between the actual and predicted data. This metric provides a valuable measure of the model's overall accuracy relative to the mean absolute error.

##### scatter_coor():
To visualize the outcomes of actual versus predicted values, the scatter_coor() function generates scatter plots. These plots help us gain an intuitive understanding of the model's performance by visually comparing actual and predicted data points.

##### concat_data():
The concat_data() function is instrumental in updating the dataset dynamically. It stacks new data points on top of the existing data, ensuring that the model remains up-to-date and continuously adapts to the latest information.

##### slide():
The slide() function is the backbone of the dynamic sliding window approach. It shifts and disposes of old data points based on the arrival of new data points. By managing the data dynamically, the model maintains its validity while incorporating fresh information to enhance predictive accuracy.

## Performance Outcomes
To evaluate the effectiveness of the dynamic sliding window approach, we conducted seven experiments. The first experiment employed the standard data modeling using the entire dataset. The second experiment involved the traditional sliding window approach, where data was slid after reaching a certain threshold. The remaining experiments focused on the dynamic sliding window approach, dividing the data into different numbers of chunks to compare the modeling process from a data chunk size perspective. By analyzing the time spent for modeling, percentage of mean absolute error for each model, and other relevant metrics, we gain valuable insights into the dynamic sliding window's efficiency and its ability to adapt to concept drift, ensuring the model's accuracy and reliability over time.

In our quest to build a powerful price prediction model, we explored various modelling approaches, ultimately finding that the dynamic sliding window approach outshone the others in terms of speed, efficiency, and accuracy. By conducting a series of experiments and evaluating key performance metrics, we can confidently state that dynamic modelling stands as the most promising technique for our dynamic sliding window project. Let's delve into the results and discover why dynamic modelling emerged as the superior choice.

#### 1. Data Size: A Lightweight Model with Optimal Data Utilization
In terms of the total number of data points used for modelling, experiment 3 - the dynamic modelling approach - achieved the most remarkable result. With the addition of 18 data chunks, dynamic modelling demonstrated an exceptional ability to complete the process with only half as many data points as classical modelling. This proves the efficiency of dynamic modelling in preventing data inflation and obtaining a lightweight model. Compared to the sliding window approach in experiment 2, dynamic modelling accomplished the task using fewer data points, making significant strides in building a more efficient and resource-friendly model.

#### 2. Time for Modelling: Agility in Action
As expected, a lightweight model translates into less modelling time, and dynamic modelling delivered on this front. The graphical representation reveals that dynamic modelling spends a maximum of around 4 seconds when reaching the maximum amount of data. In contrast, other models experience increased time consumption in the last iteration. This underscores the superiority of dynamic modelling in terms of speed and agility, making it a valuable choice for real-time prediction needs.

#### 3. Error Percentage: A Balance of Precision and Adaptability
Results highlight that all models progressively improve as new data points are added, showcasing their ability to learn from the influx of fresh information. Classical sliding window modelling, observed in experiment 2, achieved the lowest error rate with an impressive 7.939%. Although the dynamic modelling approach in experiment 3 exhibited a slightly higher error rate of 8.164%, the difference is marginal. This indicates that while dynamic modelling excels in speed and data utilization, it does not compromise on accuracy. It strikes a remarkable balance between precision and adaptability, solidifying its position as the most promising modelling approach.

In our dynamic sliding window project, the dynamic modelling approach emerges as the clear winner, outperforming other modelling methods in terms of speed, efficiency, and accuracy. With its ability to handle concept drift, minimize data inflation, and deliver real-time predictions, dynamic modelling stands at the forefront of cutting-edge price prediction models. By selecting dynamic modelling, we pave the way for an agile and precise model that stays ahead of the curve, continuously evolving with the ever-changing data landscape.