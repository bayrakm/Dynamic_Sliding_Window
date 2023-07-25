#  Exploratory Data Analysis

Unraveling Insights: A Journey through Exploratory Data Analysis in the Dynamic Sliding Window Project

## Introduction:

Exploratory Data Analysis (EDA) is a crucial step in any data science project, providing invaluable insights into the dataset's characteristics and guiding subsequent data preprocessing. In this article, we delve into the EDA process employed in our dynamic sliding window project, which aimed to develop a robust and agile price prediction model. Through careful data cleaning, outlier detection, and encoding, we sought to ensure the reliability and accuracy of our predictions. Let's explore the key steps taken during our EDA journey.

## 1. Data

The dataset used in this project consists of 111,739 data points, making it a substantial collection of information. It comprises 17 different features that provide valuable insights for the price prediction task. The data was sourced from four prominent websites in the automotive industry: autotrader, cargurus, parkers, and theaa.

The dataset focuses on cars from four specific makes: Toyota, Ford, Vauxhall (Opel), and Volkswagen. Within each make, there are five different models represented, ranging from mini cars to SUVs. This variety ensures a diverse representation of vehicle types, allowing for a comprehensive analysis and prediction of prices across different classes of models.

Overall, the dataset encompasses a significant amount of information, covering multiple features and a range of popular car makes and models. This rich dataset provides a solid foundation for conducting exploratory data analysis, developing predictive models, and evaluating their performance in the context of price prediction.

## 2. Step by Step EDA

1. Handling Inconsistent NaN Values:
Our first priority was to address inconsistent NaN values, as they could impact the quality of our model. We systematically replaced various representations of NaN, such as 'n/a', 'NA', and others, with a uniform representation, making the data consistent and easier to process.

2. Fixing Inconsistent String Formats:
To achieve uniformity in our dataset, we tackled inconsistencies in string formats, such as capitalization, unnecessary prefixes, and suffixes. By standardizing the text values, we reduced potential errors during further analysis and modeling.

3. Removing Redundant Data Points:
To maintain the dataset's relevancy and focus on meaningful predictions, we took steps to remove redundant data points. Unwanted makes and models were carefully dropped, ensuring our model concentrated solely on the relevant information.

4. Handling Inconsistent Values in Columns:
We noticed some columns, like the year column, contained inconsistent values like 0, 1, or 3. These outliers were likely data entry errors and were removed to maintain data integrity.

5. Converting 0 Values to NaN:
Certain columns contained meaningless 0 values, such as door number '0'. To avoid confusion during modeling, we appropriately converted these 0 values to NaN, highlighting their insignificance.

6. Removing Clear Outliers:
Outliers can skew predictions and adversely affect the model's performance. To maintain accuracy, we removed clear outliers, such as extremely high car prices that seemed erroneous, e.g., a £600,000 car.

7. Filling NaN Values through Grouped Aggregation:
For columns with NaN values, we applied grouped aggregation functions to fill in the missing data accurately. This ensured we capitalized on relevant information to replace the NaN values.

8. Dropping Remaining NaN Values:
After thorough data cleaning and filling missing values, some NaN values might persist. As these could potentially introduce bias, we carefully dropped any remaining NaN values.

9. Encoding Data for ML Models and Saving:
To prepare the dataset for machine learning models, we encoded categorical features into numerical representations. This step allowed the models to process the data effectively. After this process, we saved the cleaned and encoded dataset for further analysis and modeling.

## Conclusion:
The Exploratory Data Analysis process in our dynamic sliding window project was instrumental in transforming raw data into a reliable and efficient price prediction model. By addressing inconsistencies, handling outliers, and encoding data for machine learning, we paved the way for successful modeling, enabling accurate and agile predictions in the ever-changing automotive market. The meticulous EDA process sets the stage for the subsequent steps, ensuring the model is primed to adapt and excel in the face of concept drift.