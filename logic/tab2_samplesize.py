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

def calculate_sample_size_mortality_rate(sample_design, mortality_rate, margin_of_error, recall_period, non_response, household_size, population_size = 20000, design_effect=1):
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
    recall_days : int
        The number of days in the recall period for mortality (e.g., 30 for a 30-day recall).
    household_size : int
        The average number of individuals per household.
    non_response : float
        The expected rate of non-response (e.g., 10 for 10%).
    design_effect : float, optional
        The design effect for clustered sampling (default is 1 for simple random or systematic random sampling designs).

    Returns
    -------
    int
        The calculated sample size in individuals.
    int
        The calculated sample size in person-time (in person-days).
    int
        The calculated sample size in households.
    """

    r = mortality_rate / 10000
    d = margin_of_error / 10000

    Z = 1.96  # default to 95%
    t = 2.045 # default for 95% for cluster surveys
    N = population_size
    response_rate = (100 - non_response) / 100

    if sample_design == 'simple_random' or sample_design == 'stratified':

        # Step 1: Calculate number of people needed
        numerator = Z**2 * r * (1 - r)
        denominator = d**2 * recall_period 
        n_individuals = numerator / denominator
        n_adj_individuals = (n_individuals * population_size) / (n_individuals + (population_size - 1))
        n_person_time = n_adj_individuals * recall_period

        # Adjust for design effect if applicable
        # Step 2: Convert to number of households
        n_households = (n_adj_individuals / household_size)

        return (
            math.ceil(n_adj_individuals),
            math.ceil(n_person_time),
            math.ceil(n_households / response_rate)
        )

    elif sample_design == 'clustered':
        # Step 1: Calculate number of people needed
        numerator = t**2 * r * (1 - r) * design_effect
        denominator = d**2 * recall_period 
        n_individuals = numerator / denominator
        n_adj_individuals = (n_individuals * population_size) / (n_individuals + (population_size - 1))
        n_person_time = n_adj_individuals * recall_period

        # Step 2: Convert to number of households
        n_households = (n_adj_individuals / household_size)

        return (
            math.ceil(n_adj_individuals), 
            math.ceil(n_person_time),
            math.ceil(n_households / response_rate)
        ) 
    else:
        raise ValueError("Invalid sample design type provided.")

def calculate_planning_parameters(
   sample_design,
   household_sample_size,
   number_teams,
   enumerators_per_team,
   number_psu_per_team_per_day,
   start_time,
   end_time,
   average_interview_time,
   average_travel_time,
   average_rest_time):
    """
    Calculate the planning parameters based on the provided inputs. 
    These calculations assume that per best practice there is one working team per PSU. 

    Parameters
    ----------
    sample_design : str
        The sampling design to use (e.g., 'simple_random', 'stratified', 'clustered').
    household_sample_size : int
        The total number of households to be sampled.
    number_teams : int
        The number of teams available for the survey.
    enumerators_per_team : int
        The number of enumerators in each team.
    number_psu_per_team_per_day : int
        The number of Primary Sampling Units (PSUs) each team can handle per day.
    start_time : str
        The start time of the survey in HH:MM format.
    end_time : str
        The end time of the survey in HH:MM format.
    average_interview_time : float
        The average time taken for each interview in minutes.
    average_travel_time : float
        The average travel time between households in minutes.
    average_rest_time : float
        The average rest time for enumerators in minutes.

    Returns
    -------
    int
        The number of PSUs needed to complete the survey.
    int
        The number of days needed to complete the survey.
    """
    
    # Convert start and end times to datetime objects for calculation
    
    start_dt = datetime.strptime(start_time, "%H:%M")
    end_dt = datetime.strptime(end_time, "%H:%M")
    
    # Calculate total working hours per day
    total_working_hours = (end_dt - start_dt).seconds / 3600  # Convert seconds to hours
    
    # Calculate total available time per team per day in minutes
    total_available_time = total_working_hours * 60  # Convert hours to minutes
    
    # Calculate effective working time per enumerator per day
    effective_working_time = (
        total_available_time - 
        (average_rest_time) - 
        (average_travel_time))
    
    if sample_design == 'simple_random' or sample_design == 'stratified':
        # Calculate the number of days required to complete the household sample size
        number_days_needed = math.ceil((household_sample_size*average_interview_time) /  (effective_working_time* number_teams * enumerators_per_team))
        number_psu_needed = None

        return (number_psu_needed, number_days_needed)

    elif sample_design == 'clustered':

        # Calculate the number of PSUs each team can handle per day
        time_per_psu = (effective_working_time / number_psu_per_team_per_day)
        psu_size = math.floor((time_per_psu / average_interview_time)* enumerators_per_team)
        number_psu_needed = math.ceil(household_sample_size / psu_size)

        # Calculate the number of days needed to complete all PSUs
        number_days_needed = math.ceil((number_psu_needed / (number_psu_per_team_per_day*number_teams)))

        return (number_psu_needed, psu_size, number_days_needed)

    else:
        raise ValueError("Invalid sample design type provided.")

