# logic/samplesize.py

import math
from datetime import datetime, timedelta

def calculate_sample_size(sample_design, population_size, proportion, margin_of_error, non_response, design_effect=1):
    """
    Calculate the sample size of individuals or households based on the specified parameters for a simple random sampling design or a clustered design. Assumes a 95% confidence level.

    Parameters
    ----------
    sample_design : str
        The sampling design to use (e.g., 'simple_random', 'stratified', 'clustered').
    population_size : int
        The total population size to determine if finite population correction is needed.
    proportion : float
        The estimated proportion of the population that has the attribute of interest (e.g., 30 for 30%).
    margin_of_error : float
        The desired margin of error (e.g., 10 for 10%).
    non_response : float
        The expected rate of non-response (e.g., 10 for 10%).
    design_effect : float, optional
        The design effect for clustered sampling (default is 1 for simple random or systematic random sampling designs).

    Returns
    -------
    int
        The calculated sample size.
    """
    
    Z = 1.96  # default to 95%
    t = 2.045 # default for 95% for cluster surveys
    p = proportion / 100  # Convert percentage to proportion
    e = margin_of_error / 100  # Convert percentage to proportion
    N = population_size
    response_rate = (100 - non_response) / 100

    if sample_design == 'simple_random' or sample_design == 'stratified':
        n0 = (Z**2 * p * (1 - p)) / (e**2)
        n = (n0 / (1 + (n0 - 1) / N))
        return math.ceil(n /response_rate)
    elif sample_design == 'clustered':
        n0 = (t**2 * p * (1 - p)) / (e**2)
        n = (n0 / (1 + (n0 - 1) / N)) * design_effect
        return math.ceil(n/response_rate)
    else:
        raise ValueError("Invalid sample design type provided.")
    
def calculate_sample_size_ind_to_hh(sample_design, population_size, proportion, margin_of_error, non_response, household_size, prop_subpopulation, design_effect=1):
    """
    Calculate the sample size of individuals based on the specified parameters for a simple random sampling design or a clustered design, and then convert to an estimated number of households using available demographic information. Assumes a 95% confidence level.
    Assumes that all eligible individuals in a sampled household are selected. 

    Parameters
    ----------
    sample_design : str
        The sampling design to use (e.g., 'simple_random', 'stratified', 'clustered').
    population_size : int
        The total population size to determine if finite population correction is needed.
    proportion : float
        The estimated proportion of the population that has the attribute of interest (e.g., 30 for 30%).
    margin_of_error : float
        The desired margin of error (e.g., 10 for 10%).
    non_response : float
        The expected rate of non-response (e.g., 10 for 10%).
    design_effect : float, optional
        The design effect for clustered sampling (default is 1 for simple random or systematic random sampling designs).
    household_size : int
        The average number of individuals per household.
    prop_subpopulation : float
        The proportion of the population that is part of the subpopulation of interest (e.g., 30 for 30%).

    Returns
    -------
    int
        The calculated sample size in individuals.
    int
        The calculated sample size in households.
    """

    Z = 1.96  # default to 95%
    t = 2.045 # default for 95% for cluster surveys
    p = proportion / 100  # Convert percentage to proportion
    e = margin_of_error / 100  # Convert percentage to proportion
    N = population_size
    response_rate = (100 - non_response) / 100
    prop_subpopulation = prop_subpopulation / 100  # Convert percentage to proportion

    if sample_design == 'simple_random' or sample_design == 'stratified':
        n0 = (Z**2 * p * (1 - p)) / (e**2)
        n_ind = (n0 / (1 + (n0 - 1) / N))
        n_hh = n_ind / (household_size*prop_subpopulation)
        return math.ceil(n_ind), math.ceil(n_hh /response_rate)
    elif sample_design == 'clustered':
        n0 = (t**2 * p * (1 - p)) / (e**2)
        n_ind = (n0 / (1 + (n0 - 1) / N)) * design_effect
        n_hh = n_ind / (household_size*prop_subpopulation)
        return math.ceil(n_ind), math.ceil(n_hh /response_rate)
    else:
        raise ValueError("Invalid sample design type provided.")




