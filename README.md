# Churn prediction Ecommerce Customer Behavior Dataset

## Description of the project

### Goal
The project aims to train a model of binary classification which churns based on diverse type of the data of the customer's behaving, demography and financial status. With trained model the model is deployed as a web service aplication. Also a dockerfile is created for deployment od the model in clouds or other host. At the end the docker image was deployed to a AWS cloud with Elastic Beanstalk 

### Structure of the project
1. Downloading the data 
2. Feature engeenering:
- Basic inspecting of the data
- filling missing values and dealing with invalid values in dataset
- Checking correlations coefficients
3. Training models and tuning:
Three models will be trained 
- Linear Regressor model
- Random Forest model
- XGB Tree model
Models have a tunned parameters and the results on validational set are compared. It came out that XGB trees are provides best model. This model with best parameters is trained on full dataset and deployed.
4. The best model is saved as binary file 
5. The saved model is served by application buit with Flask.
The working model is checked with using gunicorn and separately with explicit using url with jupyter lab
5. The project dependencies and venv are served by using dockerfile. 
Working of the docker image is checked.
6. Depying the docker image to the cloud (AWS) 
## Description of the dataset
Used dataset is taken from Kaggle repository
-[Dataset](https://www.kaggle.com/datasets/dhairyajeetsingh/ecommerce-customer-behavior-dataset)
For convenience the file with datasets can be found in foulder /ECOMMERCE under the name: (ecommerce_customer_churn_dataset.csv)

The dataset contains 50k records and 25 features with diffrent types(int, float, str)
They are printed below:
1. Customer Demographics (5 features)

Age, Gender, Country, City, Membership_Years
2. Platform Engagement (8 features)

Login_Frequency, Session_Duration_Avg, Pages_Per_Session
Cart_Abandonment_Rate, Wishlist_Items, Email_Open_Rate
Mobile_App_Usage, Social_Media_Engagement_Score
3. Purchase Behavior (6 features)

Total_Purchases, Average_Order_Value, Days_Since_Last_Purchase
Discount_Usage_Rate, Return_Rate, Payment_Method_Diversity
4. Customer Service (3 features)

Customer_Service_Calls, Product_Reviews_Written, Lifetime_Value
5. Financial & Status (3 features)

 Credit_Balance, Churned (**target variable**), Signup_Quarter

 The Churned variable is the target.

 FOr convenience and reproducibility of the results the splitted data are also in folder ECOMMERCE:
- test_data.json (is used for final test)
- train_data.json (is to first training of diffrent models )
- val_data.json (used to checking the results of the training of the diffrents models and choosing best one)
## Short description of the peculiar files
1. Inspecting_data.ipynb
File with feature engineering, filling values and saving test, val, train data used in the next notebook
2. Training_Models.ipynb
Notebook with training 3 models for logistic regression. Includes also tuning parameters.
3. train_final_model.py is python sript for training and saving final model. Training is done on merged data_val and data_train

4. pred_app.py is a script which codes deployment of the model into web service with flask and 

5. final_model.bin - the binary file with saved final model used by pred_app.py

6. POST_request.ipyn - is for checking that application works

## Description of enviromental setups 
For the project manager uv pkg was used. 
1. Installation of uv:
- for Linux: 
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
- for windows look at officail docs (https://docs.astral.sh/uv/#__tabbed_1_1)
2. In docs you can check how to initaite project and how to add, remove, manage project enviroment

3. Generally uv create to important files:
-pyproject.toml
-uv.lock
4. The nice feature of uv is that one doesn't need to enter indirectly to venv, but just using command uv ...
- you can for example use jupyterlab by command
```bash
uv run --with jupyter jupyter lab
```

## Using of the service
1. First possiblity
Using follow command in terminal you can run pred_app.py with uv 
```bash
uv run -- flask --app pred_app.py run
```
Adress: http://127.0.0.1:5000/prediction 
Next using file: POST_request.ipynb (can be activated in another terminal) you can check the output 
2. Second possibility 
Using uv to run pred_app.file
```bash
uv run pred_app.py
```
You should get:
```bash
 * Serving Flask app 'churning'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:9696
 * Running on http://192.168.100.102:9696
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 327-628-520
```
This is more convenient because of **activated debbuger mode**. 
Adress: http://192.168.100.102:9696/prediction
Working can be checked using also POST_request.ipynb

3. Third possibility
Using gunicorn we can use command:
```bash
uv run gunicorn --bind 0.0.0.0:9696 pred_app:web_app
```
This activates file pred_app.py (web_app is my name for Flask)
Now in another terminal you can use:
```bash
curl -X POST http://localhost:9696/prediction \
-H "Content-Type: application/json" \
-d '{
    "Age": 25,
    "Membership_Years": 3.1,
    "Login_Frequency": 29,
    "Session_Duration_Avg": 51.4,
    "Pages_Per_Session": 8.4,
    "Cart_Abandonment_Rate": 19.1,
    "Wishlist_Items": 9,
    "Total_Purchases": 32.5,
    "Average_Order_Value": 141.3,
    "Days_Since_Last_Purchase": 73,
    "Discount_Usage_Rate": 25.2,
    "Returns_Rate": 5.5,
    "Email_Open_Rate": 37.9,
    "Customer_Service_Calls": 1,
    "Product_Reviews_Written": 11,
    "Social_Media_Engagement_Score": 83,
    "Mobile_App_Usage": 50.4,
    "Lifetime_Value": 3041.29,
    "Credit_Balance": 5354,
    "Gender": "Male",
    "Country": "India",
    "City": "Delhi",
    "Payment_Method_Diversity": 4.0,
    "Signup_Quarter": "Q4"
}'
```
The result should be:
```bash
{"churn_prediction:":0.2114461213350296}
```

## Description of the docker file
To build docker image use
```bash
sudo docker build -t churn-predict .
```
I needed to use sudo before docker - now our docker image has name churn-predict
My docker weights about 1 Gb 
At the end you should get:
```bash
Successfully tagged churn-predict:latest
```
You can also check
```bash
 sudo docker ps
```
You should see container_ID, name of image (churn-predict), name of container (churn-container), etc.
If it works that means the docker is active. You can check using command in another terminal:
```bash
curl -X POST http://localhost:9696/prediction \
-H "Content-Type: application/json" \
-d '{
    "Age": 25,
    "Membership_Years": 3.1,
    "Login_Frequency": 29,
    "Session_Duration_Avg": 51.4,
    "Pages_Per_Session": 8.4,
    "Cart_Abandonment_Rate": 19.1,
    "Wishlist_Items": 9,
    "Total_Purchases": 32.5,
    "Average_Order_Value": 141.3,
    "Days_Since_Last_Purchase": 73,
    "Discount_Usage_Rate": 25.2,
    "Returns_Rate": 5.5,
    "Email_Open_Rate": 37.9,
    "Customer_Service_Calls": 1,
    "Product_Reviews_Written": 11,
    "Social_Media_Engagement_Score": 83,
    "Mobile_App_Usage": 50.4,
    "Lifetime_Value": 3041.29,
    "Credit_Balance": 5354,
    "Gender": "Male",
    "Country": "India",
    "City": "Delhi",
    "Payment_Method_Diversity": 4.0,
    "Signup_Quarter": "Q4"
}'
```
the result of the prediction

You can stop caontainer by
```bash
sudo docker stop churn-container
```
And again start:
```bash
sudo docker start churn-container
```
## Descroptiom of deploying model to AWS with using docker container
1. Having dockerimage we need to instal two things:
- you need to have AWS CLI (command line)
If you don't have it yet follow the instraction from official site [AWS_CLI_installation]
(https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
The installation depends on you operational system.
You can check the positive result of the installation with (Linux):
```bash
aws --version
```
You should get something similar to this:
```bash
aws-cli/2.40.3 Python/3.14.8 Linux/7.0.0-43-generic exe/x86_64.ubuntu.24
```
Be awere that you need to configure you machine with you AWS account
Command for configuration (you need to have a keyes):
```bash
aws configure --profile eb-cli
``` 
After finishing the authentication you can use:
```bash
aws sts get-caller-identity --profile eb-cli
```
You should get UserID, Acount and Arn
- Second thing is AWS Elastic Beanstalk Command Line Interface
This cinterface can be installed locally only in you project. Using uv we can install it (in project folder) by using:
```bash
uv tool install awsebcli
```
You can check the version after installing(in you venv):
```bash
eb --version
```
You should see something like that:
```bash
EB CLI 3.27.7 (Python 3.12.3 (main, Aug 31 2026, 10:18:26) [GCC 13.3.0])
``` 
2. To initialize the Elastick Beanstalk app one should use command:
```bash
eb init -p docker -r eu-north-1 churn-serving
```
churning-serving is a name of application and eu-north-1 should be in agreement with you accout configuration
Youn can verify that eb properly activates our application by docker:
```bash
eb local run --port 9696
```
It should activate our app and using another terminal and using command with data posted above (in Using of the service section) you should get proper prediction as in the other cases.
To finish the deployment of our model to AWS cloud one needs to create enviroment which will be managing the docker containers and distributed it to other parts of a team 
```bash
eb create churn-serving-env
```
After proper realization you should get the IP of the server and see new environment in your Elastic Beanstalk Environments  