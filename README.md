# fetch-receipt-count-prediction

This repo is part of homework for fetch Machine Learning Apprentship for summer 2024.
I will quickly get into the steps and how to setup the code.
# Setup
1. Pull or Download the code in your machine.
   
2. install the requirements present in requirements.txt
   ```
    pip install -r requirements.txt
   ```
   here, i am assuming python is already installed in the machine, if not (https://www.python.org/downloads/) can be downloaded from here and setup , its easy.

3. Verify Project and File structure once.
   
   ![image](https://github.com/Nims972/fetch-receipt-count-prediction/assets/22131911/baf8945e-b58f-4970-b10c-55fbb66fc576)

4. go the the project from command line and start flask server , (if project is imported in IDE, it would be just run the file , you can still use below command in IDE console)
   ```
   python -m flask run
   ```
5. Once flask is started it should display output something like below

   ![image](https://github.com/Nims972/fetch-receipt-count-prediction/assets/22131911/b3069f90-1442-48aa-8a40-5524f166f0fa)
 


# Approach Summary

   
  - First I am preparing features from date like ['day', 'month', 'dayofweek','weekofyear', 'holidays']
  - Basis initial EDA I show some trend in weekly seasonal decompose , hence I have gone with 7 day history to predict the next day(8th) count.
  - I have used Sequential model from Keras and TF with LSTM and Dense layers to train the trend/receipt counts. I am passing batch of 7 days while training the model.
  - Building upon this for final prediction of next year
      a. using last 7 days of year 2021 to comeup with 1st day of 2022
      b. using last 6 days of year 2021 and then 1 day of year 2022 to comeup with 2nd day of 2022 and so on.
  - this way populated whole year and displayed the monthly count of receipt in the nodebook.(check the last section of fetch notebook)

    
