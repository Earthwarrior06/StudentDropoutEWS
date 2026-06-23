# I. FrontEnd(TBD next week)
### 1. The Frontend will have a login page
### 2. A csv uploader that is capable of taking 10M Value Count CSVs
  - This will be done by trying to access the logical address of the CSVs(through pandas)
  - **NOTE: The program will stop working if the csv is deleted and feature csv not made**

# II. How The CSVs Will Be Modified
### 1. A certain course, year, and branch is selected by the user
 - **NOTE:In future steps we will not use the aformentioned for training**
 - It will only be used for confirmation of how well the system works at the very end
### 2. Now All required features will be added
  - possiple future additions
  - - Split Data into quarters(Q1-Q2, Q1-Q3,Q1-Q4)
    - Add different weighing for fail and withdrawal if one is more important to prevent

# III. Training ML Models
### 1. Options for Models presented to the user
 - **XGBoostClassifier**: In Experimenting Outperform All Other Tree Models consistently
 - **RandomTreeClassifier**: Performed Decently, Quicker To Train Than XGBoost
 - **LogisticRegression**: By Far The Worst Accuracy, Quickest To Train
 - ~~VotingClassifier~~: Performed Exactly as the average of the above models, Slowest To Train **20 Minutes to get SHAP Values**
### 2. Now Whichever Models Were Selected Will Run through Variations of its hyperparameters
 - The Version Of Each With The Highest Accuracy Will be exported as a JSON  file



# IV. Viewing The Prediction Data
### 1. Said models Will Use the Selected course, year, and branch as Test Values
- During Testing it will show effective accuracy using final result column
### 2. Shap Values found will Be Explained By LLM
