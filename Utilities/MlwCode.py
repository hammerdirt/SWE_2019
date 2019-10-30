"""
Makes the MLW code class
"""
import numpy as np
import json
import csv
import datetime
import requests
import os

def get_the_data(variable_names,end_points):
    """
    get_the_data(variable_names,end_points)

    Returns a dictionary with key = vairiable_names
    and value = to JSON output from endpoint
    """
    data = {}
    for i, name in enumerate(variable_names):
        print(variable_names)
        print(end_points[i])
        data[name] = requests.get(end_points[i]).json()
    return data
# make a pieces per meter value for each observation
def get_pieces_per_meter(aDict):
    """
    get_pieces_per_meter(aDict)

    Divides the quantity by the length.
    Creates a new k,v pair with the results
    """
    new_list_of_objects = []
    the_keys = list(aDict.keys())
    for this_key in the_keys:
        new_list = aDict[this_key]
        for the_object in new_list:
            new_object = the_object
            new_object["pcs_m"] = np.round(new_object["quantity"]/new_object["length"], 4)
            new_list_of_objects.append(new_object)
    return new_list_of_objects
# make a summary of the data
def make_summary(data):
    """
    Makes a summary of the data in dictionary format
    """
    results = {}
    pcs_m = []
    for result in data:
        pcs_m.append(result["pcs_m"])
    results["the_min"] = np.min(pcs_m)
    results["the_max"] = np.max(pcs_m)
    results["the_median"] = np.median(pcs_m)
    results["the_average"] = np.mean(pcs_m)
    results["twenty_fifth"] = np.percentile(pcs_m, 25)
    results["seventy_fifth"] =  np.percentile(pcs_m, 75)
    results["no_samples"] = len(pcs_m)
    results["last_sample"] = max([x["date"] for x in data])
    results["first_sample"] = min([x["date"] for x in data])
    return results
# make time value pairts
def time_value_pairs(aList):
    """
    Makes an array of [time, value] pairs of the 'pcs_m'
    """
    myPairs = [[result['date'], result['pcs_m']] for result in aList]
    return myPairs
#  group by month
class MlWCodes():
    def __init__(self, code, common_names, end_points):
        self.code = code
        self.data = get_pieces_per_meter(get_the_data(common_names,end_points))
        self.time_value = time_value_pairs(self.data)
        self.summary = make_summary(self.data)



def makeClasessFromCodes(codes_of_interest, end_point):
    what_i_want = []
    for code in codes_of_interest:
        code_class = MlWCodes(code=code, common_names=[code], end_points=[end_point + code])
        what_i_want.append(code_class)
    return what_i_want

def group_values_by_month(aList):
    grouped_by_month = {}
    for x in aList:
        month = x[0].month
        months = grouped_by_month.keys()
        if month in months:
            grouped_by_month[month].append(x)
        else:
            grouped_by_month[month] = [x]
    return grouped_by_month
def group_values_by_month_year(aList):
    grouped_by_month_year = {}
    for x in aList:
        month_year = (x[0].year, x[0].month)
        months_years = grouped_by_month_year.keys()
        if month_year in months_years:
            grouped_by_month_year[month_year].append(x)
        else:
            grouped_by_month_year[month_year] = [x]
    return grouped_by_month_year
def makePythonDate(aList):
    return [[datetime.datetime.strptime(x[0], "%Y-%m-%d"), x[1]] for x in aList.time_value]
def makeSummaryOfAGroup(aDict):
    what_i_want = {}
    for k,v in aDict.items():
        vals = [x[1] for x in v]
        dates = [x[0] for x in v]
        mean = np.mean(vals)
        median = np.median(vals)
        least = np.min(vals)
        most = np.max(vals)
        count = len(vals)
        first = min(dates)
        last = max(dates)
        what_i_want.update({k:(v,mean, median, most, least,count, first, last)})
    return what_i_want
def groupSummary(aMLWCodeClass):
    what_i_want = {}
    the_dates = makePythonDate(aMLWCodeClass)
    by_month_year = group_values_by_month_year(the_dates)
    by_month=group_values_by_month(the_dates)
    what_i_want.update({"month_year":makeSummaryOfAGroup(by_month_year)})
    what_i_want.update({"month":makeSummaryOfAGroup(by_month)})
    return what_i_want
def makeSeasons(this_data, seasons):
    my_seasons = {}
    my_summaries = []
    for k, v in seasons.items():
        cumulative=[]
        dates = []
        for val in v:
            some_data = this_data[val][0]
            for pair in some_data:
                cumulative.append(pair[1])
                dates.append(pair[0])
        my_seasons.update({k:cumulative})
        mean = np.mean(cumulative)
        median = np.median(cumulative)
        least = np.min(cumulative)
        most = np.max(cumulative)
        count = len(cumulative)
        first = min(dates)
        last = max(dates)
        my_summaries.append({k:{"mean":mean, "median":median, "min":least, "max":most, "samples":count, "first": first, "last":last}})

    return( my_seasons, my_summaries)
def makeGroupsFromClasses(aList):
    what_i_want = []
    for x in aList:
        what_i_need = groupSummary(x)
        what_i_want.append(what_i_need)
    return what_i_want
def getTheDataINeed(a_name="", api_url="", date=""):
    some_data = get_the_data([a_name],[api_url])
    the_data = get_pieces_per_meter(some_data)
    what_i_want = {}
    if date and a_name:
        what_i_want['the_day'] = [obj for obj in the_data if obj['date'] == date]
        what_i_want[a_name] = the_data
    elif not date and a_name:
        what_i_want[a_name] = the_data

    else:
        print("Wheres my stuff? - there was an error try again")
    return what_i_want
