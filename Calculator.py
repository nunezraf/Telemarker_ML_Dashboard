
# coding: utf-8

#Import dependency
from ML import ML_model,ML_df
classifier = ML_model()
df = ML_df()

#Define Functions
def calculate(array):
    result = round(100*classifier.predict_proba(array)[0][1],4)
    return result

def change_data(array,index,value):
    temp_arr = array.copy()
    temp_arr[index] = value
    return(temp_arr)

def change_to_YN(value):
    if value == 0:
        return("N")
    if value == 1:
        return("Y")


#Calculate Original %

def origin_prob(customer_id):
    output = calculate(df.loc[[customer_id]])
    return(output)
    

def compare_scenario(customer_id):
    _input = df.loc[[customer_id]]
    columns = df.columns
    scenario = {}
    for i in range(23):
        _input.iloc[:,i] = 1-_input.iloc[:,i]
        scenario[columns[i]+" to "+change_to_YN(_input.iloc[:,i].values[0])] = calculate(_input)
    return(scenario)

origin_prob("6713-OKOMC")
compare_scenario("6713-OKOMC")