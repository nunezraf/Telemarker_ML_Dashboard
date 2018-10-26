def ML_model():
#########Importing libraries##########
    import numpy as np
    import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
    import os
    from PIL import  Image
    import itertools
    import warnings
    warnings.filterwarnings("ignore")
    import io

    ############Visualization#############
    # import matplotlib.pyplot as plt
    # get_ipython().run_line_magic('matplotlib', 'inline')
    # import seaborn as sns
    # import plotly.offline as py
    # py.init_notebook_mode(connected=True)
    # import plotly.graph_objs as go
    # import plotly.tools as tls
    # import plotly.figure_factory as ff
    ############Machine Learning ##########
    from sklearn.datasets import make_regression
    from sklearn.linear_model import LinearRegression
    from sklearn.datasets import make_regression
    from sklearn.preprocessing import LabelEncoder
    from sklearn.preprocessing import StandardScaler
    from sklearn.datasets.samples_generator import make_blobs # Jose
    from sklearn.model_selection import train_test_split # Jose
    from sklearn.linear_model import LogisticRegression # Jose
    from sklearn.model_selection import GridSearchCV # Jose
    from sklearn.metrics import classification_report, accuracy_score # Jose
    from sklearn.neighbors import KNeighborsClassifier # Jose
    from sklearn.datasets import make_classification # Jose
    from sklearn import metrics # Jose

    ########Bring in the DATA!###########

    telcom = pd.read_csv("dataset/Telemarker.csv")

    #######Data Cleaning Process#########

    #Replacing spaces with null values in total charges column
    telcom['TotalCharges'] = telcom["TotalCharges"].replace(" ",np.nan)

    #Dropping null values from total charges column which contain .16% missing data
    telcom = telcom[telcom["TotalCharges"].notnull()]
    telcom = telcom.reset_index()[telcom.columns]

    #convert to float type
    telcom["TotalCharges"] = telcom["TotalCharges"].astype(float)
    telcom["MonthlyCharges"] = telcom["MonthlyCharges"].astype(float)

    #replace 'No phone service' to No
    telcom["MultipleLines"] = telcom["MultipleLines"].replace("No phone service","No")

    #replace 'No internet service' to No for the following columns
    replace_cols = [ 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                    'TechSupport','StreamingTV', 'StreamingMovies']

    for i in replace_cols : 
        telcom[i]  = telcom[i].replace({'No internet service' : 'No'})

    #Separating catagorical and numerical columns
    Id_col     = ['customerID']
    target_col = ["Churn"]
    cat_cols   = telcom.nunique()[telcom.nunique() < 6].keys().tolist()
    cat_cols   = [x for x in cat_cols if x not in target_col]
    num_cols   = [x for x in telcom.columns if x not in cat_cols + target_col + Id_col]

    #Binary columns with 2 values
    bin_cols   = telcom.nunique()[telcom.nunique() == 2].keys().tolist()

    # #Columns more than 2 values
    multi_cols = [i for i in cat_cols if i not in bin_cols]

    # #Label encoding Binary columns
    le = LabelEncoder()
    for i in bin_cols :
        telcom[i] = le.fit_transform(telcom[i])
        
    # #Duplicating columns for multi value columns
    telcom = pd.get_dummies(data = telcom,columns = multi_cols)

    # #Scaling Numerical columns
    std = StandardScaler()
    scaled = std.fit_transform(telcom[num_cols])
    scaled = pd.DataFrame(scaled,columns=num_cols)
    # #dropping original values merging scaled values for numerical columns
    df_telcom_og = telcom.copy()
    telcom = telcom.drop(columns = num_cols,axis = 1)
    telcom = telcom.merge(scaled,left_index=True,right_index=True,how = "left")

    var_summ = telcom.describe().transpose()
    # var_summ =  var_summ.rename(columns = {"index" : "feature"})
    var_summ.index.name = "Feature"
    # var_summ = pd.Series([0,2,2,2,2,2,2,2], index=["count", "mean", "std", "min", "25%", "50%", "75%","max"])
    var_summ = var_summ.round(2)

    # #Model Building 

    # splitting train and test data 
    train,test = train_test_split(telcom,test_size = .20 ,random_state = 42)
        
    ##seperating dependent and independent variables
    cols    = [i for i in telcom.columns if i not in Id_col + target_col]
    X_train = train[cols]
    y_train = train[target_col]
    X_test  = test[cols]
    y_test  = test[target_col]

    # Logistic Regression
    classifier = LogisticRegression()
    classifier.fit(X_train, y_train)
    coefficient = classifier.coef_

    telcom1 = telcom.drop(["Churn"],axis = 1)
    df = telcom1.set_index("customerID")

    column_names = list(df.columns.values)

    column_names = list(df.columns.values)

    return classifier

#     coef_df = pd.DataFrame({"gender": telcom1["gender"] * coefficient[0][0],
#                             "SeniorCitizen": telcom1["SeniorCitizen"] * coefficient[0][1],
#                             "Partner": telcom1["Partner"] * coefficient[0][2],
#                             "Dependents": telcom1["Dependents"] * coefficient[0][3],
#                             "PhoneService": telcom1["PhoneService"] * coefficient[0][4],
#                             "MultipleLines": telcom1["MultipleLines"] * coefficient[0][5],
#                             "OnlineSecurity": telcom1["OnlineSecurity"] * coefficient[0][6],
#                             "OnlineBackup": telcom1["OnlineBackup"] * coefficient[0][7],
#                             "DeviceProtection": telcom1["DeviceProtection"] * coefficient[0][8],
#                             "TechSupport": telcom1["TechSupport"] * coefficient[0][9],
#                             "StreamingTV": telcom1["StreamingTV"] * coefficient[0][10],
#                             "StreamingMovies": telcom1["StreamingMovies"] * coefficient[0][11],
#                             "PaperlessBilling": telcom1["PaperlessBilling"] * coefficient[0][12],
#                             "InternetService_DSL": telcom1["InternetService_DSL"] * coefficient[0][13],
#                             "InternetService_Fiber optic": telcom1["InternetService_Fiber optic"] * coefficient[0][14],
#                             "InternetService_No": telcom1["InternetService_No"] * coefficient[0][15],
#                             "Contract_Month-to-month": telcom1["Contract_Month-to-month"] * coefficient[0][16],
#                             "Contract_One year": telcom1["Contract_One year"] * coefficient[0][17],
#                             "Contract_Two year": telcom1["Contract_Two year"] * coefficient[0][18],
#                             "PaymentMethod_Bank transfer (automatic)": telcom1["PaymentMethod_Bank transfer (automatic)"] * coefficient[0][19],
#                             "PaymentMethod_Credit card (automatic)": telcom1["PaymentMethod_Credit card (automatic)"] * coefficient[0][20],
#                             "PaymentMethod_Electronic check": telcom1["PaymentMethod_Electronic check"] * coefficient[0][21],
#                             "PaymentMethod_Mailed check": telcom1["PaymentMethod_Mailed check"] * coefficient[0][22],
#                             "tenure": telcom1["tenure"] * coefficient[0][23],
#                             "MonthlyCharges": telcom1["MonthlyCharges"] * coefficient[0][24],
#                             "TotalCharges": telcom1["TotalCharges"] * coefficient[0][25]
#                         })
#     # print("This is working!")
#     # print(coef_df)
#     print(coef_df.sum(axis=1))
ML_model()

def ML_df():
#########Importing libraries##########
    import numpy as np
    import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
    import os
    from PIL import  Image
    import itertools
    import warnings
    warnings.filterwarnings("ignore")
    import io

    ############Visualization#############
    # import matplotlib.pyplot as plt
    # get_ipython().run_line_magic('matplotlib', 'inline')
    # import seaborn as sns
    # import plotly.offline as py
    # py.init_notebook_mode(connected=True)
    # import plotly.graph_objs as go
    # import plotly.tools as tls
    # import plotly.figure_factory as ff
    ############Machine Learning ##########
    from sklearn.datasets import make_regression
    from sklearn.linear_model import LinearRegression
    from sklearn.datasets import make_regression
    from sklearn.preprocessing import LabelEncoder
    from sklearn.preprocessing import StandardScaler
    from sklearn.datasets.samples_generator import make_blobs # Jose
    from sklearn.model_selection import train_test_split # Jose
    from sklearn.linear_model import LogisticRegression # Jose
    from sklearn.model_selection import GridSearchCV # Jose
    from sklearn.metrics import classification_report, accuracy_score # Jose
    from sklearn.neighbors import KNeighborsClassifier # Jose
    from sklearn.datasets import make_classification # Jose
    from sklearn import metrics # Jose

    ########Bring in the DATA!###########

    telcom = pd.read_csv("dataset/Telemarker.csv")

    #######Data Cleaning Process#########

    #Replacing spaces with null values in total charges column
    telcom['TotalCharges'] = telcom["TotalCharges"].replace(" ",np.nan)

    #Dropping null values from total charges column which contain .16% missing data
    telcom = telcom[telcom["TotalCharges"].notnull()]
    telcom = telcom.reset_index()[telcom.columns]

    #convert to float type
    telcom["TotalCharges"] = telcom["TotalCharges"].astype(float)
    telcom["MonthlyCharges"] = telcom["MonthlyCharges"].astype(float)

    #replace 'No phone service' to No
    telcom["MultipleLines"] = telcom["MultipleLines"].replace("No phone service","No")

    #replace 'No internet service' to No for the following columns
    replace_cols = [ 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                    'TechSupport','StreamingTV', 'StreamingMovies']

    for i in replace_cols : 
        telcom[i]  = telcom[i].replace({'No internet service' : 'No'})

    #Separating catagorical and numerical columns
    Id_col     = ['customerID']
    target_col = ["Churn"]
    cat_cols   = telcom.nunique()[telcom.nunique() < 6].keys().tolist()
    cat_cols   = [x for x in cat_cols if x not in target_col]
    num_cols   = [x for x in telcom.columns if x not in cat_cols + target_col + Id_col]

    #Binary columns with 2 values
    bin_cols   = telcom.nunique()[telcom.nunique() == 2].keys().tolist()

    # #Columns more than 2 values
    multi_cols = [i for i in cat_cols if i not in bin_cols]

    # #Label encoding Binary columns
    le = LabelEncoder()
    for i in bin_cols :
        telcom[i] = le.fit_transform(telcom[i])
        
    # #Duplicating columns for multi value columns
    telcom = pd.get_dummies(data = telcom,columns = multi_cols)

    # #Scaling Numerical columns
    std = StandardScaler()
    scaled = std.fit_transform(telcom[num_cols])
    scaled = pd.DataFrame(scaled,columns=num_cols)
    # #dropping original values merging scaled values for numerical columns
    df_telcom_og = telcom.copy()
    telcom = telcom.drop(columns = num_cols,axis = 1)
    telcom = telcom.merge(scaled,left_index=True,right_index=True,how = "left")

    var_summ = telcom.describe().transpose()
    # var_summ =  var_summ.rename(columns = {"index" : "feature"})
    var_summ.index.name = "Feature"
    # var_summ = pd.Series([0,2,2,2,2,2,2,2], index=["count", "mean", "std", "min", "25%", "50%", "75%","max"])
    var_summ = var_summ.round(2)

    # #Model Building 

    # splitting train and test data 
    train,test = train_test_split(telcom,test_size = .20 ,random_state = 42)
        
    ##seperating dependent and independent variables
    cols    = [i for i in telcom.columns if i not in Id_col + target_col]
    X_train = train[cols]
    y_train = train[target_col]
    X_test  = test[cols]
    y_test  = test[target_col]

    # Logistic Regression
    classifier = LogisticRegression()
    classifier.fit(X_train, y_train)
    coefficient = classifier.coef_

    telcom1 = telcom.drop(["Churn"],axis = 1)
    df = telcom1.set_index("customerID")

    column_names = list(df.columns.values)

    column_names = list(df.columns.values)

    return df

#     coef_df = pd.DataFrame({"gender": telcom1["gender"] * coefficient[0][0],
#                             "SeniorCitizen": telcom1["SeniorCitizen"] * coefficient[0][1],
#                             "Partner": telcom1["Partner"] * coefficient[0][2],
#                             "Dependents": telcom1["Dependents"] * coefficient[0][3],
#                             "PhoneService": telcom1["PhoneService"] * coefficient[0][4],
#                             "MultipleLines": telcom1["MultipleLines"] * coefficient[0][5],
#                             "OnlineSecurity": telcom1["OnlineSecurity"] * coefficient[0][6],
#                             "OnlineBackup": telcom1["OnlineBackup"] * coefficient[0][7],
#                             "DeviceProtection": telcom1["DeviceProtection"] * coefficient[0][8],
#                             "TechSupport": telcom1["TechSupport"] * coefficient[0][9],
#                             "StreamingTV": telcom1["StreamingTV"] * coefficient[0][10],
#                             "StreamingMovies": telcom1["StreamingMovies"] * coefficient[0][11],
#                             "PaperlessBilling": telcom1["PaperlessBilling"] * coefficient[0][12],
#                             "InternetService_DSL": telcom1["InternetService_DSL"] * coefficient[0][13],
#                             "InternetService_Fiber optic": telcom1["InternetService_Fiber optic"] * coefficient[0][14],
#                             "InternetService_No": telcom1["InternetService_No"] * coefficient[0][15],
#                             "Contract_Month-to-month": telcom1["Contract_Month-to-month"] * coefficient[0][16],
#                             "Contract_One year": telcom1["Contract_One year"] * coefficient[0][17],
#                             "Contract_Two year": telcom1["Contract_Two year"] * coefficient[0][18],
#                             "PaymentMethod_Bank transfer (automatic)": telcom1["PaymentMethod_Bank transfer (automatic)"] * coefficient[0][19],
#                             "PaymentMethod_Credit card (automatic)": telcom1["PaymentMethod_Credit card (automatic)"] * coefficient[0][20],
#                             "PaymentMethod_Electronic check": telcom1["PaymentMethod_Electronic check"] * coefficient[0][21],
#                             "PaymentMethod_Mailed check": telcom1["PaymentMethod_Mailed check"] * coefficient[0][22],
#                             "tenure": telcom1["tenure"] * coefficient[0][23],
#                             "MonthlyCharges": telcom1["MonthlyCharges"] * coefficient[0][24],
#                             "TotalCharges": telcom1["TotalCharges"] * coefficient[0][25]
#                         })
#     # print("This is working!")
#     # print(coef_df)
#     print(coef_df.sum(axis=1))
ML_df()