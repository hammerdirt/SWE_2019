import pandas as pd
import datetime
# import MlwCode.get_the_data as get_the_data
# import MlwCode.get_pieces_per_meter as get_pieces_per_meter



def make_folders(here, folders):
    """
    make_folders(here, folders)
    Each name in the folders list gets appended to the variable here.

    'here' is the output from os.getcwd()
    """
    my_folders = {}
    for folder in folders:
        place = here +"/"+ folder
        my_folders[folder] = place
    return my_folders
def makeStringFromList(aList):
    """
    Takes an array of strings and combines them to a comma
    separated string, with no trailing comma.
    """
    a_string = ""
    stop_here = len(aList)-1
    for i,obj in enumerate(aList):
        if i == stop_here:
            a_string += "{}".format(obj)
        else:
            a_string += "{}, ".format(obj)
    return a_string


def makeADataFrame(data,code,index):
    """
    makeADataFrame(data,code,index)

    Makes a pandas dataframe from a dictionary. Creates a column for the MLW code
    Use it to store summary values from the MLWCode class.

    data = MLWCodeClass.make_summary

    code = The mlw code of the class

    index = dataframe index level
    """
    aDf= pd.DataFrame(data, index=[index])
    return aDf.join(pd.DataFrame({'code_id': [code]}))
def joinDataFrames(aList, codes_of_interest):
    """
    joinDataFrames(aList, codes_of_interest)

    Takes a list  of MLWClasses and extracts the .summary attribute. Stores each code summary
    in one datadrame. Then joins the dataframes into one.

    aList = [a list of MLWCode objects]

    codes_of_interest = [a list of corresponding MLW codes]

    """
    start = aList[0]
    start_df = makeADataFrame(start.summary,codes_of_interest[0],0)
    for i,data in enumerate(aList[1:]):
        n = i+1
        a_df = makeADataFrame(data.summary,codes_of_interest[n], 0)
        start_df = start_df.append(a_df, ignore_index=True)
    return start_df

def getOtherDays( all_the_days, a_date):
    """
    getOtherDays( all_the_days, a_date)

    Returns all the data for a date from the api data.

    all_the_days = the data from the api

    date= "%Y-%m-%d"
    """
    my_day = list(filter(lambda d: d['date'] == a_date, all_the_days))
    return my_day
def getACategory(a_code, some_data):
    """
    getACategory(a_code, some_data)

    Returns all the data for an mlw code from the api data.

    some_data = the data from the api

    a_code = an mlw code
    """
    my_code_data = list(filter(lambda d: d['code_id'] == a_code, some_data))
    return my_code_data
def getASetOfUniqueValues(some_attribute, some_data):
    """
    getASetOfUniqueValues(some_attribute, some_data)

    Returns all the data for any attribute from the api data.

    some_data = the data from the api

    some_attribute, = an mlw code
    """
    my_special_data = [x[some_attribute] for x in some_data ]
    return list(set(my_special_data))
def getTheValuesOfAnAttribute(some_attribute, attribute_value, some_data):
    """
    getTheValuesOfAnAttribute(some_attribute, attribute_value, some_data)

    Returns an array of values whose attribut value matches the given

    some_data = the data from the api

    some attribute = an mlw code
    """
    my_special_data = [x for x in some_data if x[some_attribute] == attribute_value]
    return my_special_data
def getPandasCodeSummary(df,codes):
    the_dfs = []
    for code in codes:
        a_sum = df.loc[df['code_id'] == code]['pcs_m'].describe()
        a_sum['code_id'] = code
        a_sum = a_sum.to_dict()
        a_df = pd.DataFrame.from_dict([a_sum])
        the_dfs.append(a_sum)
    what_i_want = pd.DataFrame(the_dfs)
    return what_i_want
def getValueOfInterestFromDayOfInterest(day_of_interest, code_of_interest):
    for value in day_of_interest:
        if code_of_interest == value["code_id"]:
            myday_y = value['pcs_m']
            my_date = datetime.datetime.strptime(value['date'], "%Y-%m-%d")
            my_month = my_date.month
    return myday_y, my_month
