# logic/samplesize.py

import math
from logic.validators import validate_type, validate_int, validate_float 

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
        The estimated proportion of the population that has the attribute of interest.
    margin_of_error : float
        The desired margin of error (e.g., 0.05 for 5%).
    non_response : float
        The expected rate of non-response (e.g., 0.1 for 10%).
    design_effect : float, optional
        The design effect for clustered sampling (default is 1 for simple random or systematic random sampling designs).

    Returns
    -------
    int
        The calculated sample size.
    """
    
    Z = 1.96  # default to 95%
    p = proportion
    e = margin_of_error
    N = population_size
    response_rate = 1 - non_response

    n0 = (Z**2 * p * (1 - p)) / (e**2)
    n = (n0 / (1 + (n0 - 1) / N)) * design_effect

    if sample_design == 'simple_random' or sample_design == 'stratified':
        return math.ceil(n /response_rate)
    elif sample_design == 'clustered':
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
        The estimated proportion of the population that has the attribute of interest.
    margin_of_error : float
        The desired margin of error (e.g., 0.05 for 5%).
    non_response : float
        The expected rate of non-response (e.g., 0.1 for 10%).
    design_effect : float, optional
        The design effect for clustered sampling (default is 1 for simple random or systematic random sampling designs).

    Returns
    -------
    int
        The calculated sample size.
    """
    Z = 1.96  # default to 95%
    p = proportion
    e = margin_of_error
    N = population_size
    response_rate = 1 - non_response

    n0 = (Z**2 * p * (1 - p)) / (e**2)
    n_ind = (n0 / (1 + (n0 - 1) / N)) * design_effect
    n_hh = n_ind / (household_size*prop_subpopulation)

    if sample_design == 'simple_random' or sample_design == 'stratified':
        return math.ceil(n_hh /response_rate)
    elif sample_design == 'clustered':
        return math.ceil(n_hh /response_rate)
    else:
        raise ValueError("Invalid sample design type provided.")

def calculate_sample_size_mortality_rate(sample_design, population_size, mortality_rate, margin_of_error, recall_period, non_response, household_size, design_effect=1):
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
        The estimated proportion of the population that has the attribute of interest.
    margin_of_error : float
        The desired margin of error (e.g., 0.05 for 5%).
    recall_days : int
        The number of days in the recall period for mortality (e.g., 30 for a 30-day recall).
    household_size : int
        The average number of individuals per household.
    non_response : float
        The expected rate of non-response (e.g., 0.1 for 10%).
    design_effect : float, optional
        The design effect for clustered sampling (default is 1 for simple random or systematic random sampling designs).

    Returns
    -------
    int
        The calculated sample size.
    """

    r = cmr_per_10k_day / 10000
    d = precision_per_10k_day / 10000

    Z = 1.96  # default to 95%
    N = population_size
    response_rate = 1 - non_response

    # Step 1: Calculate number of people needed
    numerator = Z**2 * r * (1 - r) * design_effect
    denominator = d**2 * recall_days 
    n_individuals = numerator / denominator
    n_adj_individuals = (n_individuals * total_population) / (n_individuals + (total_population - 1))

    # Step 2: Convert to number of households
    n_households = (n_adj_individuals / household_size)

    if sample_design == 'simple_random' or sample_design == 'stratified':
        return math.ceil(n_households /response_rate)
    elif sample_design == 'clustered':
        return math.ceil(n_households /response_rate)
    else:
        raise ValueError("Invalid sample design type provided.")

