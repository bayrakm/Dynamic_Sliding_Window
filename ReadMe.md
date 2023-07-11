# Building a Dynamic Price Prediction Model: Tackling Concept Drift in Automobile Markets

Inspired by the notion of data as a living organism, our research aims to develop an advanced price prediction model that remains relevant over time by adapting to the evolving nature of data. We recognize the limitations of static machine learning models in sustaining their effectiveness amidst changing circumstances. To address this, we embark on a comprehensive study leveraging real-time data acquired from reputable online platforms specializing in pre-owned car sales. Our dynamic modeling approach ensures the generation of accurate and up-to-date predictions by continuously incorporating fresh data points into our model. The foundation of our methodology lies in two critical phases. Firstly, we employ an automated web scraping pipeline to procure new data and update our dataset on a daily basis, enabling a continuous influx of information. Secondly, during the modeling phase, we employ the sliding window technique, a concept drift approach, to compare and evaluate the performance of the newly generated model against its predecessor. Through this comparison, we identify the superior model, ensuring our predictions are consistently refined and sensitive to market price fluctuations. The result is an agile, lightweight, and enduring dynamic model that surpasses the limitations of traditional approaches, providing invaluable insights into the ever-changing landscape of automobile pricing.


## Content of Notebooks

**1. Data Mining:** In this initial step of the project, the focus was on gathering data from five prominent second-hand car selling websites. The data extraction process was automated using Python libraries such as scrapy and selenium. A custom script was developed to scrape and download the relevant data points from these websites on a daily basis. This ensured a continuous inflow of fresh data for further analysis and model development.

**2. EDA (Exploratory Data Analysis):** This notebook was dedicated to the preprocessing and exploration of the collected data. Data cleaning techniques were applied to handle missing values, outliers, and inconsistencies. The dataset was carefully prepared to be suitable for the subsequent machine learning models. Furthermore, the notebook aimed to gain insights into the characteristics and patterns within the dataset through thorough exploration, including descriptive statistics, visualizations, and feature analysis.

**3. Baseline Modelling:** Baseline modelling involved the implementation and evaluation of six different supervised learning regression algorithms as a baseline for price prediction. The selected algorithms were trained and tested using the preprocessed dataset from Notebook 2. The objective was to identify the best-performing algorithm among the options considered, based on predetermined evaluation metrics such as accuracy, mean squared error, or R-squared. This step served as a benchmark for comparing the performance of subsequent models.

**4. Dynamic Sliding Window:** Here I focused on experimenting with and validating the effectiveness of the dynamic sliding window approach. The dynamic sliding window is a technique employed to address the issue of concept drift, allowing the model to adapt to changing data patterns over time. Several simulation experiments were conducted to assess the efficiency and impact of the dynamic sliding window approach on the predictive performance of the model. The experiments aimed to demonstrate the superiority of this approach in handling concept drift, ensuring the model remains accurate and up-to-date in the face of evolving data. 


## Dataset

The dataset used in this project consists of 111,739 data points, making it a substantial collection of information. It comprises 17 different features that provide valuable insights for the price prediction task. The data was sourced from four prominent websites in the automotive industry: autotrader, cargurus, parkers, and theaa.

The dataset focuses on cars from four specific makes: Toyota, Ford, Vauxhall (Opel), and Volkswagen. Within each make, there are five different models represented, ranging from mini cars to SUVs. This variety ensures a diverse representation of vehicle types, allowing for a comprehensive analysis and prediction of prices across different classes of models.

Overall, the dataset encompasses a significant amount of information, covering multiple features and a range of popular car makes and models. This rich dataset provides a solid foundation for conducting exploratory data analysis, developing predictive models, and evaluating their performance in the context of price prediction.

No | Feature | Data Type | Unit | Description  | 
|----------|----------|----------|----------|----------|
1. | Source | String | N/A | URL of the car. | 
2. | Make | String | N/A | Brand of the car. (e.g., Toyota, Ford) | 
3. | Model | String | N/A | Model of the car. (e.g., Auris, Golf) | 
4. | Price | Continues Number | Sterling | Price of the car on the website. | 
5. | Mileage | Continues Number | Mile | Mileage of the car as a whole number. | 
6. | Year | Discrete Number | N/A | Manufactured year of the car. (e.g., 2012) | 
7. | Power | Continues Number | HP | The power of the car in HP (BHP). | 
8. | Consumption | Continues Number | MPG | Fuel consumption of the car in miles per gallon. | 
9. | Cylinder | Discrete Number | N/A | The number of cylinders of the car. | 
10. | Gears | Discrete Number | N/A | The number of the gears of the car. | 
11. | Fuel type | String | N/A | Fuel type of the car (e.g., Petrol, Diesel) | 
12. | Transmission | String | N/A | Type of the transmission (e.g., Manual, Auto) | 
13. | Body type | String | N/A | The type of the car. (e.g., Hatchback, Sedan)  | 
14. | CO2 Emission | Continues Number | g/km | CO2 emission amount of the car. | 
15. | Door | Discrete Number | N/A | The number of doors of the car. | 
16. | Seat | Discrete Number | N/A | The number of seats in the car. | 
17. | Engine size | Continues Number | Litre | The volume of the engine in litres. | 



## Approach


## Results
