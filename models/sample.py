import math
import logic.validators
import datetime
import pandas as pd
from PyQt6.QtCore import QTime
from typing import Optional

class Sample:
    """
    A class to represent a sampling frame.
    This class is designed to manage the sampling frame for surveys or studies,
    including the creation of a sampling frame, updating it, and managing the sample size.
    """

    Z = 1.96  # default to 95%
    T = 2.045 # default for 95% for cluster surveys

    def __init__(self, 
                 sampling_frame: Optional[pd.DataFrame] = None,
                 sample_design: str = "simple_random",
                 total_population: int = 20000, 
                 fpc: bool = True, 

                 proportion: float = 50, 
                 margin_of_error: float = 5.5, 
                 non_response: float = 3.5, 
                 design_effect: float = 1,

                 proportion_ind: float = 50, 
                 margin_of_error_ind: float = 5.5, 
                 non_response_ind: float = 3.5, 
                 design_effect_ind: float = 1,
                 average_household_size: float = 4.5,
                 prop_subpopulation: float = 20,

                 mortality_rate: float = 0.1,
                 recall_period: int = 90,
                 margin_of_error_rate: float = 0.05,
                 design_effect_rate: float = 1,
                 non_response_rate: float = 10,
                 average_household_size_rate: float = 4.5,
                 
                 planning_sample_size: int = 450,
                 num_days: int = 12,
                 num_enumerators_per_team: int = 3, 
                 num_teams: int = 4,
                 start_time: datetime = datetime.time(9,30),
                 end_time: datetime = datetime.time(17,30), 
                 average_interview_time: int=30,
                 average_travel_time: int=90,
                 average_rest_time: int=60,

                 result_sample_size: int = None,
                 result_sample_size_ind: int = None,
                 result_sample_size_ind_hh: int = None,
                 result_sample_size_mortality_ind: int = None,
                 result_sample_size_mortality_pt: int = None,
                 results_sample_size_mortality_hh: int = None,
                 parent = None
                 ):
        """
        Initialize the Sample class with the necessary parameters.
        Parameters:
            sampling_frame (pd.Dataframe): The sampling frame used to select sampling units. 
            sample_design (str): The design of the sample (e.g., "simple_random", "clustered").
            total_population (int): The total population size.
            fpc (bool): Finite Population Correction factor (True or False).
            proportion (float): The estimated proportion of the population with the characteristic of interest.
            margin_of_error (float): The desired margin of error for the estimate.
            non_response (float): The expected non-response rate.
            design_effect (float): The design effect to adjust for complex survey designs.
            proportion_ind (float): The estimated proportion of the population with the characteristic of interest for individual samples.
            margin_of_error_ind (float): The desired margin of error for individual samples.
            non_response_ind (float): The expected non-response rate for individual samples.
            design_effect_ind (float): The design effect to adjust for complex survey designs for individual samples.
            average_household_size (float): The average household size in the population.
            prop_subpopulation (float): The proportion of the sub-population of interest.
            mortality_rate (float): The estimated mortality rate in the population.
            recall_period (int): The recall period for the survey (in days).
            margin_of_error_rate (float): The desired margin of error for mortality rate estimates.
            design_effect_rate (float): The design effect to adjust for complex survey designs for mortality rate estimates.
            non_response_rate (float): The expected non-response rate for mortality rate estimates.
            sampling_frame (list): The list of units in the sampling frame.
            planning_sample_size (int): The number of surveys for planning suyrvey operations (number of enumerators, days, clusters, etc.)
            num_days (int): The number of days for the survey.
            num_enumerators_per_team (int): The number of enumerators per team.
            num_teams (int): The number of teams conducting the survey.
            average_interview_tiem (int): The average number of minutes to implement one survey (e.g. 30 minutes)
            average_travel_time (int): The average number of minutes spent travelling to and from assessment sites per day (e.g. 90 minutes)
            average_rest_time (int): The average number of minutes assessment teams will rest for during the work day for breaks, lunch, etc. (e.g. 60 minutes)
        """
        if sampling_frame is None:
            sampling_frame = pd.DataFrame(columns=["strata", "unit", "population", "cluster"])
        self.sampling_frame = sampling_frame
        self.sample_design = sample_design
        self.total_population = total_population
        self.fpc = fpc  # Finite Population Correction

        self.proportion = proportion
        self.margin_of_error = margin_of_error
        self.non_response = non_response
        self.design_effect = design_effect

        self.proportion_ind = proportion_ind
        self.margin_of_error_ind = margin_of_error_ind
        self.non_response_ind = non_response_ind
        self.design_effect_ind = design_effect_ind
        self.average_household_size = average_household_size
        self.prop_subpopulation = prop_subpopulation

        self.mortality_rate = mortality_rate
        self.recall_period = recall_period
        self.margin_of_error_rate = margin_of_error_rate
        self.design_effect_rate = design_effect_rate
        self.non_response_rate = non_response_rate
        self.average_household_size_rate = average_household_size_rate    

        self.planning_sample_size = planning_sample_size
        self.num_days = num_days
        self.num_enumerators_per_team = num_enumerators_per_team
        self.num_teams = num_teams
        self.average_interview_time = average_interview_time
        self.average_travel_time = average_travel_time
        self.average_rest_time = average_rest_time
        
        self.result_sample_size = result_sample_size
        self.result_sample_size_ind = result_sample_size_ind
        self.result_sample_size_ind_hh = result_sample_size_ind_hh
        self.result_sample_size_mortality_ind = result_sample_size_mortality_ind
        self.result_sample_size_mortality_pt = result_sample_size_mortality_pt
        self.result_sample_size_mortality_hh = results_sample_size_mortality_hh

        is_valid, conv_start_time = logic.validators.validate_time(start_time, name="Daily start time")
        if is_valid:
            self.start_time = conv_start_time
        else:
            error_message = f"{start_time} is not a valid time input."
            if parent is None:
                print(error_message)
            else:
                logic.validators.show_error(error_message)
            raise ValueError(error_message)
    
        is_valid, conv_end_time = logic.validators.validate_time(end_time, name="Daily end time")
        if is_valid:
            self.end_time = conv_end_time
        else:
            error_message = f"{end_time} is not a valid time input."
            if parent is None:
                print(error_message)
            else:
                logic.validators.show_error(error_message)
            raise ValueError(error_message)
        

    def update_params(self, sample_design=None , 
                                 total_population=None, 
                                 fpc=None, 
                                 proportion=None, 
                                 margin_of_error=None, 
                                 non_response=None, 
                                 design_effect=None,
                                 proportion_ind=None,
                                 margin_of_error_ind=None,
                                 non_response_ind=None,
                                 design_effect_ind=None,
                                 average_household_size=None,
                                 prop_subpopulation=None,    
                                 mortality_rate=None,
                                 recall_period=None,
                                 margin_of_error_rate=None,
                                 design_effect_rate=None,
                                 non_response_rate=None,
                                 average_household_size_rate=None,
                                 sampling_frame=None,
                                 planning_sample_size=None,
                                 num_days=None,
                                 num_enumerators_per_team=None,
                                 num_teams=None,
                                 start_time = None,
                                 end_time = None,
                                 average_interview_time=None,
                                 average_travel_time=None,
                                 average_rest_time=None):
        """
        Update the sampling parameters of the sampling frame.
        This method allows updating any of the parameters used in the sample size calculation.
        """
        if (sample_design is not None and logic.validators.validate_type(sample_design, expected_type=str, name="Sample design input")):
            is_valid, conv_sample_design = logic.validators.validate_string_choice(text=sample_design, allowed_values=["simple_random", "clustered"], name="Sample design input")
            if is_valid:
                self.sample_design = conv_sample_design
        if (total_population is not None and logic.validators.validate_type(total_population, expected_type=int, name="Total population input")):
            is_valid, conv_total_population = logic.validators.validate_int(total_population, min_value=1, name="Total population")
            if is_valid:
                self.total_population = conv_total_population
        if (fpc is not None and logic.validators.validate_type(fpc, expected_type=bool, name="FPC selection input")):
            self.fpc = fpc
        if (proportion is not None and logic.validators.validate_type(proportion, expected_type=float, name="Proportion input")):
            is_valid, conv_proportion = logic.validators.validate_float(text=proportion, min_value = 0, max_value = 100, name = "Proportion input")
            if is_valid:
                self.proportion = conv_proportion
        if (margin_of_error is not None and logic.validators.validate_type(margin_of_error, expected_type=float, name="Margin of error input")):
            is_valid, conv_margin_of_error = logic.validators.validate_float(text=margin_of_error, min_value = 0, max_value = 100, name = "Margin of error input")
            if is_valid:
                self.margin_of_error = conv_margin_of_error
        if (non_response is not None and logic.validators.validate_type(non_response, expected_type=float, name="Non-response rate input")):
            is_valid, conv_non_response = logic.validators.validate_float(text=non_response, min_value = 0, max_value = 100, name = "Non-response rate input")
            if is_valid:
                self.non_response = conv_non_response
        if (design_effect is not None and logic.validators.validate_type(design_effect, expected_type=float, name="Design effect input")):
            is_valid, conv_design_effect = logic.validators.validate_float(text=design_effect, min_value = 1, max_value = 100, name = "Design effect input")
            if is_valid:
                self.design_effect = conv_design_effect
        if (proportion_ind is not None and logic.validators.validate_type(proportion_ind, expected_type=float, name="Proportion for individual sample input")):
            is_valid, conv_proportion_ind = logic.validators.validate_float(text=proportion_ind, min_value = 0, max_value = 100, name = "Proportion for individual sample input")
            if is_valid:
                self.proportion_ind = conv_proportion_ind
        if (margin_of_error_ind is not None and logic.validators.validate_type(margin_of_error_ind, expected_type=float, name="Margin of error for individual sample input")):
            is_valid, conv_margin_of_error_ind = logic.validators.validate_float(text=margin_of_error_ind, min_value = 0, max_value = 100, name = "Margin of error for individual sample input")
            if is_valid: 
                self.margin_of_error_ind = conv_margin_of_error_ind
        if (non_response_ind is not None and logic.validators.validate_type(non_response_ind, expected_type=float, name="Non-response rate for individual sample input")):
            is_valid, conv_non_response_ind = logic.validators.validate_float(text=non_response_ind, min_value = 0, max_value = 100, name = "Non-response rate for individual sample input")
            if is_valid:
                self.non_response_ind = conv_non_response_ind
        if (design_effect_ind is not None and logic.validators.validate_type(design_effect_ind, expected_type=float, name="Design effect for individual sample input")):
            is_valid, conv_design_effect_ind = logic.validators.validate_float(text=design_effect_ind, min_value = 1, max_value = 100, name = "Design effect for individual sample input")
            if is_valid: 
                self.design_effect_ind = conv_design_effect_ind
        if (average_household_size is not None and logic.validators.validate_type(average_household_size, expected_type=float, name="Average household size for individual sample input")):
            is_valid, conv_average_household_size = logic.validators.validate_float(text=average_household_size, min_value = 1, max_value = 50, name = "Average household size for individual sample input")
            if is_valid:
                self.average_household_size = conv_average_household_size
        if (prop_subpopulation is not None and logic.validators.validate_type(prop_subpopulation, expected_type=float, name="Proportion of population for individual sample input")):
            is_valid, conv_prop_subpopulation = logic.validators.validate_float(text=prop_subpopulation, min_value = 0, max_value = 100, name = "Proportion of population for individual sample input")
            if is_valid:
                self.prop_subpopulation = conv_prop_subpopulation
        if (mortality_rate is not None and logic.validators.validate_type(mortality_rate, expected_type=float, name="Mortality rate input")):
            is_valid, conv_mortality_rate = logic.validators.validate_float(text=mortality_rate, min_value = 0, max_value = 50, name = "Mortality rate input")
            if is_valid: 
                self.mortality_rate = conv_mortality_rate
        if (recall_period is not None and logic.validators.validate_type(recall_period, expected_type=int, name="Recall period input")):
            is_valid, conv_recall_period = logic.validators.validate_int(text=recall_period, min_value = 0, max_value = 1000, name = "Recall period input")
            if is_valid:
                self.recall_period = conv_recall_period
        if (margin_of_error_rate is not None and logic.validators.validate_type(margin_of_error_rate, expected_type=float, name="Margin of error for rates input")):
            is_valid, conv_margin_of_error_rate = logic.validators.validate_float(text=margin_of_error_rate, min_value = 0.0001, max_value = 50, name = "Margin of error for rates input")
            if is_valid:
                self.margin_of_error_rate = conv_margin_of_error_rate
        if (design_effect_rate is not None and logic.validators.validate_type(design_effect_rate, expected_type=float, name="Design effect for rates input")):
            is_valid, conv_design_effect_rate = logic.validators.validate_int(text=design_effect_rate, min_value = 1, max_value = 100, name = "Design effect for rates input")
            if is_valid: 
                self.design_effect_rate = conv_design_effect_rate
        if (non_response_rate is not None and logic.validators.validate_type(non_response_rate, expected_type=float, name="Non-response rate for rates input")):
            is_valid, conv_non_response_rate = logic.validators.validate_int(text=non_response_rate, min_value = 0, max_value = 1000, name = "Non-response rate for rates input")
            if is_valid: 
                self.non_response_rate = conv_non_response_rate
        if (average_household_size_rate is not None and logic.validators.validate_type(average_household_size_rate, expected_type=float, name="Average household size for rates input")):
            is_valid, conv_average_household_size_rate = logic.validators.validate_int(text=average_household_size_rate, min_value = 1, max_value = 50, name = "Average household size for rates input")
            if is_valid:
                self.average_household_size_rate = conv_average_household_size_rate
        if (sampling_frame is not None and logic.validators.validate_dataframe(sampling_frame, required_columns=["strata", "unit", "population", "cluster"], name = "Sampling frame")):
            self.sampling_frame = sampling_frame

        # Update the planned number of surveys, number of days, enumerators per team, and number of teams  
        if (planning_sample_size is not None and logic.validators.validate_type(planning_sample_size, expected_type = int, name = "Number of planned surveys")):
            is_valid, conv_planning_sample_size = logic.validators.validate_int(planning_sample_size, min_value=1, max_value=100000, name = "Number of planned surveys")
            if is_valid:
                self.planning_sample_size = conv_planning_sample_size
        if (num_days is not None and logic.validators.validate_type(num_days, expected_type = int, name = "Number of survey days")):
            is_valid, conv_num_days = logic.validators.validate_int(num_days, min_value=1, max_value=1000, name = "Number of survey days")
            if is_valid:
                self.num_days = conv_num_days
        if (num_enumerators_per_team is not None and logic.validators.validate_type(num_enumerators_per_team, expected_type=int, name="Number of enumerators per team")):
            is_valid, conv_enum_per_team = logic.validators.validate_int(num_enumerators_per_team, min_value=1, max_value=1000, name = "Number of enumerators per team")
            if is_valid:
                self.num_enumerators_per_team = conv_enum_per_team
        if (num_teams is not None and logic.validators.validate_type(num_teams, int, "Number of teams")):
            is_valid, conv_num_teams = logic.validators.validate_int(num_teams, min_value=1, max_value=100, name="Number of teams")
            if is_valid:
                self.num_teams = conv_num_teams
        if (start_time is not None):
            is_valid, conv_start_time = logic.validators.validate_time(start_time, name="Daily start time")
            if is_valid:
                self.start_time = conv_start_time
        if (end_time is not None):
            is_valid, conv_end_time = logic.validators.validate_time(end_time, name="Daily end time")
            if is_valid:
                self.end_time = conv_end_time
        if (average_interview_time is not None and logic.validators.validate_type(average_interview_time, int, "Average interview time")):
            is_valid, conv_average_interview_time = logic.validators.validate_int(average_interview_time, min_value=1, max_value=600, name="Average interview time")
            if is_valid:
                self.average_interview_time = conv_average_interview_time
        if (average_travel_time is not None and logic.validators.validate_type(average_travel_time, int, "Average travel time")):
            is_valid, conv_average_travel_time = logic.validators.validate_int(average_travel_time, min_value=1, max_value=600, name="Average travel time")
            if is_valid:
                self.average_travel_time = conv_average_travel_time
        if (average_rest_time is not None and logic.validators.validate_type(average_rest_time, int, "Average rest time")):
            is_valid, conv_average_rest_time = logic.validators.validate_int(average_rest_time, min_value=1, max_value=600, name="Average rest time")
            if is_valid:
                self.average_rest_time = conv_average_rest_time

    def calculate_sample_size(self,
                              sample_design = None,
                              population_size=None,
                              proportion=None,
                              margin_of_error = None,
                              non_response=None,
                              design_effect=None,
                              fpc=None,
                              parent=None):
        """
        Calculate the sample size of individuals or households based on the specified parameters for a random sampling design or a clustered design. Assumes a 95% confidence level.
        This method can be used standalone, however if no parameters passed it will utilize the saved attributes in the Sample instance. 
        Parameters
        ----------
        sample_design : str
            The sampling design to use (e.g., 'simple_random', 'clustered').
        population_size : int
            The total population size to determine if finite population correction is needed.
        proportion : float
            The estimated proportion of the population that has the attribute of interest (e.g., 30 for 30%).
        margin_of_error : float
            The desired margin of error (e.g., 10 for 10%).
        non_response : float
            The expected rate of non-response (e.g., 10 for 10%).
        design_effect : float, optional
            The design effect for clustered sampling (default is 1 for simple random sampling designs).
        fpc : bool
            The finite population correction factor to determine if should correct for population size (True or False).
        Returns
        -------
        int
            The calculated sample size, corrected for non-response rate.
        """

        sample_design = sample_design if sample_design is not None else self.sample_design 
        population_size = population_size if population_size is not None else self.total_population 
        proportion = proportion if proportion is not None else self.proportion 
        margin_of_error = margin_of_error if margin_of_error is not None else self.margin_of_error 
        non_response = non_response if non_response is not None else self.non_response 
        design_effect= design_effect if design_effect is not None else self.design_effect
        fpc=fpc if fpc is not None else self.fpc

        required_params = {
                            "sample_design": sample_design,
                            "population_size": population_size,
                            "proportion": proportion,
                            "margin_of_error": margin_of_error,
                            "non_response": non_response,
                            "fpc": fpc,
                            }

        missing = [key for key, value in required_params.items() if value is None]

        if missing:
            error_message = f"The following parameters are missing or None: {', '.join(missing)}"
            if parent is None:
                print(error_message)
            else:
                logic.valdiators.show_error(error_message)
            raise ValueError(error_message)
        
        if sample_design == "clustered" and design_effect is None:
            error_message = f"Design effect cannot be None if calculating sample size for clustered designs."
            if parent is None:
                print(error_message)
            else:
                logic.valdiators.show_error(error_message)
            raise ValueError(error_message)

        p = proportion / 100  # Convert percentage to proportion
        e = margin_of_error / 100  # Convert percentage to proportion
        N = population_size
        response_rate = (100 - non_response) / 100

        if sample_design == 'simple_random':
            n0 = (Sample.Z**2 * p * (1 - p)) / (e**2)
            
            if fpc == True:
                n = (n0 / (1 + (n0 - 1) / N))
            elif fpc == False:
                n = n0
            else:
                error_message = f"Use of finite population correction (fpc) must be explicitly True or False. Invalid input."
                if parent is None:
                    print(error_message)
                else:
                    logic.validators.show_error(error_message)
                raise ValueError(error_message)
            self.result_sample_size = math.ceil(n/response_rate)
            return math.ceil(n /response_rate)
        
        elif sample_design == 'clustered':
            n0 = (Sample.T**2 * p * (1 - p)) / (e**2)
            if fpc == True:
                n = (n0 / (1 + (n0 - 1) / N)) * design_effect
            elif fpc == False:
                n = n0 * design_effect
            else:
                error_message = f"Use of finite population correction (fpc) must be explicitly 'yes'or 'no'. Invalid input."
                if parent is None:
                    print(error_message)
                else:
                    logic.validators.show_error(error_message)
                raise ValueError(error_message)
            
            self.result_sample_size = math.ceil(n/response_rate)
            return math.ceil(n/response_rate)
        else:
            error_message = f"Invalid sample design type provided."
            if parent is None:
                print(error_message)
            else:
                logic.validators.show_error(error_message)
            raise ValueError(error_message)

    def calculate_sample_size_ind_to_hh(self,
                              sample_design = None,
                              population_size=None,
                              proportion=None,
                              margin_of_error = None,
                              non_response=None,
                              design_effect=None,
                              household_size=None, 
                              prop_subpopulation=None,
                              fpc=None, 
                              parent = None):
        """
        Calculate the sample size of individuals based on the specified parameters for a simple random sampling design or a clustered design, and then convert to an estimated number of households using available demographic information. Assumes a 95% confidence level.
        Assumes that all eligible individuals in a sampled household are selected. 

        Parameters
        ----------
        sample_design : str
            The sampling design to use (e.g., 'simple_random', 'clustered').
        population_size : int
            The total population size to determine if finite population correction is needed.
        proportion : float
            The estimated proportion of the population that has the attribute of interest (e.g., 30 for 30%).
        margin_of_error : float
            The desired margin of error (e.g., 10 for 10%).
        non_response : float
            The expected rate of non-response (e.g., 10 for 10%).
        design_effect : float, optional
            The design effect for clustered sampling (default is 1 for simple random random sampling designs).
        household_size : int
            The average number of individuals per household.
        prop_subpopulation : float
            The proportion of the population that is part of the subpopulation of interest (e.g., 30 for 30%).
        fpc : str
            The finite population correction factor to determine if should correct for population size ('yes' or 'no'). 

        Returns
        -------
        int
            The calculated sample size in individuals.
        int
            The calculated sample size in households, corrected for non-response rate.
        """

        sample_design = sample_design if sample_design is not None else self.sample_design
        population_size = population_size if population_size is not None else self.total_population 
        proportion = proportion if proportion is not None else self.proportion_ind 
        margin_of_error = margin_of_error if margin_of_error is not None else self.margin_of_error_ind 
        non_response = non_response if non_response is not None else self.non_response_ind 
        design_effect= design_effect if design_effect is not None else self.design_effect_ind
        household_size=household_size if household_size is not None else self.average_household_size
        prop_subpopulation=prop_subpopulation if prop_subpopulation is not None else self.prop_subpopulation
        fpc=fpc if fpc is not None else self.fpc

        required_params = {
                            "sample_design": sample_design,
                            "population_size": population_size,
                            "proportion": proportion,
                            "margin_of_error": margin_of_error,
                            "non_response": non_response,
                            "household_size": household_size,
                            "prop_subpopulation": prop_subpopulation,
                            "fpc": fpc,
                            }

        missing = [key for key, value in required_params.items() if value is None]

        if missing:
            error_message = f"The following parameters are missing or None: {', '.join(missing)}"
            if parent is None:
                print(error_message)
            else:
                logic.valdiators.show_error(error_message)
            raise ValueError(error_message)
        
        if sample_design == "clustered" and design_effect is None:
            error_message = f"Design effect cannot be None if calculating sample size for clustered designs."
            if parent is None:
                print(error_message)
            else:
                logic.valdiators.show_error(error_message)
            raise ValueError(error_message)

        p = proportion / 100  # Convert percentage to proportion
        e = margin_of_error / 100  # Convert percentage to proportion
        N = population_size
        response_rate = (100 - non_response) / 100
        prop_subpopulation = prop_subpopulation / 100  # Convert percentage to proportion

        if sample_design == 'simple_random':
            n0 = (Sample.Z**2 * p * (1 - p)) / (e**2)
            
            if fpc == True:
                n_ind = (n0 / (1 + (n0 - 1) / N))
            elif fpc == False:
                n_ind = n0
            else:
                error_message = f"Use of finite population correction (fpc) must be explicitly 'yes'or 'no'. Invalid input."
                if parent is None:
                    print(error_message)
                else:
                    logic.validators.show_error(error_message)
                raise ValueError(error_message)
            n_hh = n_ind / (household_size*prop_subpopulation)

            self.result_sample_size_ind = math.ceil(n_ind)
            self.result_sample_size_ind_hh = math.ceil(n_hh /response_rate)
            return math.ceil(n_ind), math.ceil(n_hh /response_rate)
        elif sample_design == 'clustered':
            n0 = (Sample.T**2 * p * (1 - p)) / (e**2)
            if fpc == True:
                n_ind = (n0 / (1 + (n0 - 1) / N)) * design_effect
            elif fpc == False:
                n_ind = n0  * design_effect
            else:
                error_message = f"Use of finite population correction (fpc) must be explicitly 'yes'or 'no'. Invalid input."
                if parent is None:
                    print(error_message)
                else:
                    logic.validators.show_error(error_message)
                raise ValueError(error_message)
            n_hh = n_ind / (household_size*prop_subpopulation)

            self.result_sample_size_ind = math.ceil(n_ind)
            self.result_sample_size_ind_hh = math.ceil(n_hh /response_rate)
            return math.ceil(n_ind), math.ceil(n_hh /response_rate)
        else:
            error_message = f"Invalid sample design type provided."
            if parent is None:
                print(error_message)
            else:
                logic.validators.show_error(error_message)
            raise ValueError(error_message)

    def calculate_sample_size_mortality_rate(self, sample_design=None, 
                                             mortality_rate=None, 
                                             margin_of_error=None, 
                                             recall_period=None, 
                                             non_response=None, 
                                             household_size=None, 
                                             population_size=None, 
                                             design_effect=None,
                                             fpc=None,
                                             parent=None):
        """
        Calculate the sample size of individuals based on the specified parameters for a simple random sampling design or a clustered design, and then convert to an estimated number of households using available demographic information. Assumes a 95% confidence level.
        Assumes that all eligible individuals in a sampled household are selected. 
        
        Parameters
        ----------
        sample_design : str
            The sampling design to use (e.g., 'simple_random', 'clustered').
        population_size : int
            The total population size to determine if finite population correction is needed.
        mortality_rate : float
            The estimated rate that an event per day per 10,000 people (e.g., 1 death per 10000 per day).
        margin_of_error : float
            The desired margin of error (e.g., 10 for 10%).
        recall_period : int
            The number of days in the recall period for mortality (e.g., 30 for a 30-day recall).
        household_size : int
            The average number of individuals per household.
        non_response : float
            The expected rate of non-response (e.g., 10 for 10%).
        design_effect : float, optional
            The design effect for clustered sampling (default is 1 for simple random sampling designs).
        fpc : bool
            The finite population correction factor to determine if should correct for population size (True or False).

        Returns
        -------
        int
            The calculated sample size in individuals.
        int
            The calculated sample size in person-time (in person-days).
        int
            The calculated sample size in households, corrected for non-response rate.
        """

        sample_design = sample_design if sample_design is not None else self.sample_design 
        population_size = population_size if population_size is not None else self.total_population 
        mortality_rate = mortality_rate if mortality_rate is not None else self.mortality_rate 
        margin_of_error = margin_of_error if margin_of_error is not None else self.margin_of_error_rate 
        non_response = non_response if non_response is not None else self.non_response_rate 
        design_effect= design_effect if design_effect is not None else self.design_effect_rate
        household_size=household_size if household_size is not None else self.average_household_size
        recall_period=recall_period if recall_period is not None else self.recall_period
        fpc=fpc if fpc is not None else self.fpc

        required_params = {
                            "sample_design": sample_design,
                            "population_size": population_size,
                            "mortality_rate": mortality_rate,
                            "margin_of_error": margin_of_error,
                            "non_response": non_response,
                            "recall_period": recall_period,
                            "household_size": household_size,
                            "fpc": fpc,
                            }

        missing = [key for key, value in required_params.items() if value is None]

        if missing:
            error_message = f"The following parameters are missing or None: {', '.join(missing)}"
            if parent is None:
                print(error_message)
            else:
                logic.valdiators.show_error(error_message)
            raise ValueError(error_message)
        
        if sample_design == "clustered" and design_effect is None:
            error_message = f"Design effect cannot be None if calculating sample size for cluster or RLC designs."
            if parent is None:
                print(error_message)
            else:
                logic.valdiators.show_error(error_message)
            raise ValueError(error_message)

        r = mortality_rate / 10000
        d = margin_of_error / 10000
        N = population_size
        response_rate = (100 - non_response) / 100

        if sample_design == 'simple_random':

            # Step 1: Calculate number of people needed
            numerator = Sample.Z**2 * r * (1 - r)
            denominator = d**2 * recall_period 
            n_individuals = numerator / denominator

            if fpc == True:
                n_adj_individuals = (n_individuals * N) / (n_individuals + (N - 1))
            elif fpc == False:
                n_adj_individuals = n_individuals
            else:
                error_message = f"Use of finite population correction (fpc) must be explicitly 'yes'or 'no'. Invalid input."
                if parent is None:
                    print(error_message)
                else:
                    logic.validators.show_error(error_message)
                raise ValueError(error_message)
            
            n_person_time = n_adj_individuals * recall_period

            # Adjust for design effect if applicable
            # Step 2: Convert to number of households
            n_households = (n_adj_individuals / household_size)

            self.result_sample_size_mortality_ind = math.ceil(n_adj_individuals)
            self.result_sample_size_mortality_pt = math.ceil(n_person_time)
            self.result_sample_size_mortality_hh = math.ceil(n_households / response_rate)
            return (
                math.ceil(n_adj_individuals),
                math.ceil(n_person_time),
                math.ceil(n_households / response_rate)
            )

        elif sample_design == 'clustered':
            # Step 1: Calculate number of people needed
            numerator = Sample.T**2 * r * (1 - r)
            denominator = d**2 * recall_period 
            n_individuals = numerator / denominator
            if fpc == True:
                n_adj_individuals = (n_individuals * population_size) / (n_individuals + (population_size - 1)) * design_effect
            elif fpc == False:
                n_adj_individuals = n_individuals * design_effect
            else:
                error_message = f"Use of finite population correction (fpc) must be explicitly 'yes'or 'no'. Invalid input."
                if parent is None:
                    print(error_message)
                else:
                    logic.validators.show_error(error_message)
                raise ValueError(error_message)
            
            n_person_time = n_adj_individuals * recall_period

            # Step 2: Convert to number of households
            n_households = (n_adj_individuals / household_size)

            self.result_sample_size_mortality_ind = math.ceil(n_adj_individuals)
            self.result_sample_size_mortality_pt = math.ceil(n_person_time)
            self.result_sample_size_mortality_hh = math.ceil(n_households / response_rate)
            return (
                math.ceil(n_adj_individuals), 
                math.ceil(n_person_time),
                math.ceil(n_households / response_rate)
            ) 
        else:
            error_message = f"Invalid sample design type provided."
            if parent is None:
                print(error_message)
            else:
                logic.validators.show_error(error_message)
            raise ValueError(error_message)

    def calculate_planning_parameters(self,
                                      sample_design=None,
                                      household_sample_size=None,
                                      number_teams=None,
                                      enumerators_per_team=None,
                                      number_psu_per_team_per_day=None,
                                      start_time=None,
                                      end_time=None,
                                      average_interview_time=None,
                                      average_travel_time=None,
                                      average_rest_time=None,
                                      parent=None):
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
                The number of PSUs needed to complete the survey, if cluster or rlc sample design (otherwise returns None).
            int
                The number of days needed to complete the survey.
            """
            
            sample_design = sample_design if sample_design is not None else self.sample_design, 
            household_sample_size = household_sample_size if household_sample_size is not None else self.planning_sample_size, 
            number_teams = number_teams if number_teams is not None else self.num_teams
            enumerators_per_team = enumerators_per_team if enumerators_per_team is not None else self.num_enumerators_per_team
            number_psu_per_team_per_day = number_psu_per_team_per_day if number_psu_per_team_per_day is not None else self.num_enumerators_per_team
            start_time = start_time if start_time is not None else self.start_time
            end_time = end_time if end_time is not None else self.end_time
            average_interview_time = average_interview_time if average_interview_time is not None else self.average_interview_time
            average_travel_time = average_travel_time if average_travel_time is not None else self.average_travel_time
            average_rest_time = average_rest_time if average_rest_time is not None else self.average_rest_time

            required_params = {
                            "sample_design": sample_design,
                            "household_sample_size": household_sample_size,
                            "number_teams": number_teams,
                            "enumerators_per_team": enumerators_per_team,
                            "number_psu_per_team_per_day": number_psu_per_team_per_day,
                            "start_time": start_time,
                            "end_time": end_time,
                            "average_interview_time": average_interview_time,
                            "average_travel_time": average_travel_time,
                            "average_rest_time": average_rest_time,
                            }

            missing = [key for key, value in required_params.items() if value is None]

            if missing:
                error_message = f"The following parameters are missing or None: {', '.join(missing)}"
                if parent is None:
                    print(error_message)
                else:
                    logic.valdiators.show_error(error_message)
                raise ValueError(error_message)

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

            elif sample_design == 'clustered' or sample_design == 'rlc':

                # Calculate the number of PSUs each team can handle per day
                time_per_psu = (effective_working_time / number_psu_per_team_per_day)
                psu_size = math.floor((time_per_psu / average_interview_time)* enumerators_per_team)
                number_psu_needed = math.ceil(household_sample_size / psu_size)

                # Calculate the number of days needed to complete all PSUs
                number_days_needed = math.ceil((number_psu_needed / (number_psu_per_team_per_day*number_teams)))

                return (number_psu_needed, psu_size, number_days_needed)

            else:
                error_message = f"Invalid sample design type provided."
                if parent is None:
                    print(error_message)
                else:
                    logic.validators.show_error(error_message)
                raise ValueError(error_message)


    # def check_sampling_frame(self):
    #     """
    #     Check the sampling frame for completeness, format, and accuracy.
    #     This method should verify that the sampling frame is up-to-date and contains all necessary information.
    #     """
    #     pass

    # def draw_sample(self, sample_size, sample_design, cluster_size=None, num_clusters=None):
    #     """
    #     Draw a sample from the sampling frame.
    #     This method should implement the logic to randomly select a sample from the sampling frame
    #     based on the provided sample size.
    #     """
    #     pass

    # def export_sample(self, file_path: str):
    #     """
    #     Export the sample to a file.
    #     This method should save the sample data to a specified file path in a suitable format (e.g., CSV, JSON).
    #     """
    #     pass

    # def export_sampling_frame(self, file_path: str):
        # """
        # Export the sampling frame to a file.
        # This method should save the sampling frame data to a specified file path in a suitable format (e.g., CSV, JSON).
        # """
        # pass
    