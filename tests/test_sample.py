import importlib
import pytest
import math
from models.sample import Sample
from datetime import time
import pandas as pd

# CHECK INITIALIZATION AND UPDATING ATTRIBUTES

def test_Sample_default_init():
    """
    This method tests whether Sample initializes a new object with expected attribute values.
    """
    expected_df = pd.DataFrame(columns=["strata", "unit", "population", "cluster"])
    sample = Sample()
    pd.testing.assert_frame_equal(sample.sampling_frame, expected_df)
    assert sample.sample_design == "simple_random"
    assert sample.total_population == 20000
    assert sample.fpc == True
    assert sample.proportion == 50
    assert sample.margin_of_error == 5.5
    assert sample.non_response == 3.5
    assert sample.design_effect == 1
    assert sample.proportion_ind == 50
    assert sample.margin_of_error_ind == 5.5
    assert sample.non_response_ind == 3.5
    assert sample.design_effect_ind == 1
    assert sample.average_household_size == 4.5
    assert sample.prop_subpopulation == 20
    assert sample.mortality_rate == 0.1
    assert sample.recall_period == 90
    assert sample.margin_of_error_rate == 0.05
    assert sample.non_response_rate == 10
    assert sample.average_household_size_rate == 4.5
    assert sample.planning_sample_size == 450
    assert sample.num_days == 12
    assert sample.num_enumerators_per_team == 3
    assert sample.num_teams == 4
    assert sample.start_time == time(9,30)
    assert sample.end_time == time(17,30)
    assert sample.average_interview_time == 30
    assert sample.average_travel_time == 90
    assert sample.average_rest_time == 60
    assert sample.result_sample_size == None
    assert sample.result_sample_size_ind == None
    assert sample.result_sample_size_ind_hh == None
    assert sample.result_sample_size_mortality_hh == None
    assert sample.result_sample_size_mortality_ind == None
    assert sample.result_sample_size_mortality_pt == None

def test_sample_single_init():
    """
    This method tests if custom initialization is working properly for specifying a single attribute.
    Expect that all other attributes are initialized with default values.
    """
    sample = Sample(total_population=500)
    assert sample.total_population == 500
    assert sample.sample_design == "simple_random"  # default
    assert sample.proportion == 50  # default

def test_sample_calc_sample_size_init():
    """
    This method tests if custom initialization is working properly for attributes related to generalized sample size calculations.
    """
    sample = Sample(total_population=5000, sample_design="clustered", proportion=50, margin_of_error=10, non_response=10, design_effect=1.5, fpc=True)
    assert sample.total_population==5000
    assert sample.sample_design == "clustered"
    assert sample.proportion == 50
    assert sample.margin_of_error == 10
    assert sample.non_response == 10
    assert sample.design_effect == 1.5
    assert sample.fpc == True

def test_sample_calc_sample_size_ind_init():
    """
    This method tests if custom initialization is working properly for attributes related to sample size calculations for individual sub-populations.
    """
    sample = Sample(total_population=5000, sample_design="clustered", proportion_ind=50, margin_of_error_ind=10, non_response_ind=10, design_effect_ind=1.5, fpc=True)
    assert sample.total_population==5000
    assert sample.sample_design == "clustered"
    assert sample.proportion_ind == 50
    assert sample.margin_of_error_ind == 10
    assert sample.non_response_ind == 10
    assert sample.design_effect_ind == 1.5
    assert sample.fpc == True

def test_sample_calc_sample_size_rate_init():
    """
    This method tests if custom initialization is working properly for attributes related to mortality rate sample size calculations.
    """
    sample = Sample(total_population=5000, sample_design="clustered", mortality_rate=1.2, margin_of_error_rate=0.4, non_response_rate=10, design_effect_rate=1.5, fpc=True)
    assert sample.total_population==5000
    assert sample.sample_design == "clustered"
    assert sample.mortality_rate == 1.2
    assert sample.margin_of_error_rate == 0.4
    assert sample.non_response_rate == 10
    assert sample.design_effect_rate == 1.5
    assert sample.fpc == True

def test_sample_calc_planning_init():
    """
    This method tests if custom initialization is working properly for attributes related to planning calculations.
    """
    sample = Sample(planning_sample_size=123, num_days=5, num_enumerators_per_team=1, num_teams=6, start_time="7:30", end_time="18:00", average_interview_time=25, average_travel_time=90, average_rest_time=60)
    assert sample.planning_sample_size==123
    assert sample.num_days==5
    assert sample.num_enumerators_per_team==1
    assert sample.num_teams==6
    assert sample.start_time==time(7,30)
    assert sample.end_time==time(18,0)
    assert sample.average_interview_time==25
    assert sample.average_travel_time==90
    assert sample.average_rest_time==60

def test_update_params_single():
    """
    This method test if update_params functions properly for updating a single attribute (total_population).
    """
    sample = Sample()
    assert sample.total_population == 20000
    sample.update_params(total_population=50000)
    assert sample.total_population == 50000

def test_update_params_invalid_inputs():
    """
    This method tests a series of invalid inputs for various Sample attributes that can be updated through update_params method. 
    Expects various ValueError and TypeError.
    """
    sample = Sample()
    with pytest.raises(TypeError, match = "Total population input must be a int."):
        sample.update_params(total_population=True)
    with pytest.raises(ValueError, match = "Total population must be at least 1."):
        sample.update_params(total_population=-100)
    with pytest.raises(ValueError, match = "Invalid value for Sample design input. Must be one of: simple_random, clustered"):
        sample.update_params(sample_design="OMEGA")
    with pytest.raises(TypeError, match = "Sample design input must be a string."):
        sample.update_params(sample_design=125)
    with pytest.raises(TypeError, match = "FPC selection input must be a boolean."):
        sample.update_params(fpc=25)
    with pytest.raises(TypeError, match = "Proportion input cannot be converted to float."):
        sample.update_params(proportion="a")
    with pytest.raises(ValueError, match = "Proportion input must be at least 0."):
        sample.update_params(proportion=-1)
    with pytest.raises(ValueError, match = "Proportion input must be at most 100."):
        sample.update_params(proportion=125)
    with pytest.raises(TypeError, match = "Margin of error input cannot be converted to float."):
        sample.update_params(margin_of_error="a")
    with pytest.raises(ValueError, match = "Margin of error input must be at least 0."):
        sample.update_params(margin_of_error=-5)
    with pytest.raises(ValueError, match = "Margin of error input must be at most 100."):
        sample.update_params(margin_of_error=500)
    with pytest.raises(TypeError, match = "Non-response rate input cannot be converted to float."):
        sample.update_params(non_response="a")
    with pytest.raises(ValueError, match = "Non-response rate input must be at least 0."):
        sample.update_params(non_response=-5)
    with pytest.raises(ValueError, match = "Non-response rate input must be at most 100."):
        sample.update_params(non_response=500)
    with pytest.raises(TypeError, match = "Design effect input cannot be converted to float."):
        sample.update_params(design_effect="a")
    with pytest.raises(ValueError, match = "Design effect input must be at least 1."):
        sample.update_params(design_effect=-5)
    with pytest.raises(ValueError, match = "Design effect input must be at most 100."):
        sample.update_params(design_effect=500)
    with pytest.raises(TypeError, match = "Proportion for individual sample input must be a float, not a boolean."):
        sample.update_params(proportion_ind=False)
    with pytest.raises(ValueError, match = "Proportion for individual sample input must be at least 0."):
        sample.update_params(proportion_ind=-5)
    with pytest.raises(ValueError, match = "Proportion for individual sample input must be at most 100."):
        sample.update_params(proportion_ind=500)
    with pytest.raises(TypeError, match = "Margin of error for individual sample input must be a float, not a boolean."):
        sample.update_params(margin_of_error_ind=False)
    with pytest.raises(ValueError, match = "Margin of error for individual sample input must be at least 0."):
        sample.update_params(margin_of_error_ind=-5)
    with pytest.raises(ValueError, match = "Margin of error for individual sample input must be at most 100."):
        sample.update_params(margin_of_error_ind=500)
    with pytest.raises(TypeError, match = "Non-response rate for individual sample input must be a float, not a boolean."):
        sample.update_params(non_response_ind=False)
    with pytest.raises(ValueError, match = "Non-response rate for individual sample input must be at least 0."):
        sample.update_params(non_response_ind=-5)
    with pytest.raises(ValueError, match = "Non-response rate for individual sample input must be at most 100."):
        sample.update_params(non_response_ind=500)
    with pytest.raises(TypeError, match = "Design effect for individual sample input cannot be converted to float."):
        sample.update_params(design_effect_ind="Hi")
    with pytest.raises(ValueError, match = "Design effect for individual sample input must be at least 1."):
        sample.update_params(design_effect_ind=-5)
    with pytest.raises(ValueError, match = "Design effect for individual sample input must be at most 100."):
        sample.update_params(design_effect_ind=500)
    with pytest.raises(TypeError, match = "Average household size for individual sample input cannot be converted to float."):
        sample.update_params(average_household_size="Hi")
    with pytest.raises(ValueError, match = "Average household size for individual sample input must be at least 1."):
        sample.update_params(average_household_size=-5)
    with pytest.raises(ValueError, match = "Average household size for individual sample input must be at most 50."):
        sample.update_params(average_household_size=5000)
    with pytest.raises(TypeError, match = "Proportion of population for individual sample input cannot be converted to float."):
        sample.update_params(prop_subpopulation="Hi")
    with pytest.raises(ValueError, match = "Proportion of population for individual sample input must be at least 0."):
        sample.update_params(prop_subpopulation=-5)
    with pytest.raises(ValueError, match = "Proportion of population for individual sample input must be at most 100."):
        sample.update_params(prop_subpopulation=5000)
    with pytest.raises(TypeError, match = "Mortality rate input cannot be converted to float."):
        sample.update_params(mortality_rate="Hi")
    with pytest.raises(ValueError, match = "Mortality rate input must be at least 0."):
        sample.update_params(mortality_rate=-1)
    with pytest.raises(ValueError, match = "Mortality rate input must be at most 50."):
        sample.update_params(mortality_rate=5000)
    with pytest.raises(TypeError, match = "Margin of error for rates input cannot be converted to float."):
        sample.update_params(margin_of_error_rate="Hi")
    with pytest.raises(ValueError, match = "Margin of error for rates input must be at least 0."):
        sample.update_params(margin_of_error_rate=-1)
    with pytest.raises(ValueError, match = "Margin of error for rates input must be at most 50."):
        sample.update_params(margin_of_error_rate=5000)
    with pytest.raises(TypeError, match = "Non-response rate for rates input cannot be converted to float."):
        sample.update_params(non_response_rate="Hi")
    with pytest.raises(ValueError, match = "Non-response rate for rates input must be at least 0."):
        sample.update_params(non_response_rate=-1)
    with pytest.raises(ValueError, match = "Non-response rate for rates input must be at most 100."):
        sample.update_params(non_response_rate=5000)
    with pytest.raises(TypeError, match = "Recall period input cannot be converted to int."):
        sample.update_params(recall_period="Hi")
    with pytest.raises(ValueError, match = "Recall period input must be at least 0."):
        sample.update_params(recall_period=-1)
    with pytest.raises(ValueError, match = "Recall period input must be at most 1000."):
        sample.update_params(recall_period=1500)
    with pytest.raises(TypeError, match = "Number of planned surveys cannot be converted to int."):
        sample.update_params(planning_sample_size="Hi")
    with pytest.raises(ValueError, match = "Number of planned surveys must be at least 1."):
        sample.update_params(planning_sample_size=-1)
    with pytest.raises(ValueError, match = "Number of planned surveys must be at most 100000."):
        sample.update_params(planning_sample_size=200000)
    with pytest.raises(TypeError, match = "Number of survey days cannot be converted to int."):
        sample.update_params(num_days="Hi")
    with pytest.raises(ValueError, match = "Number of survey days must be at least 1."):
        sample.update_params(num_days=-1)
    with pytest.raises(ValueError, match = "Number of survey days must be at most 1000."):
        sample.update_params(num_days=200000)
    with pytest.raises(TypeError, match = "Number of enumerators per team cannot be converted to int."):
        sample.update_params(num_enumerators_per_team="Hi")
    with pytest.raises(ValueError, match = "Number of enumerators per team must be at least 1."):
        sample.update_params(num_enumerators_per_team=-1)
    with pytest.raises(ValueError, match = "Number of enumerators per team must be at most 1000."):
        sample.update_params(num_enumerators_per_team=2000)
    with pytest.raises(TypeError, match = "Number of teams cannot be converted to int."):
        sample.update_params(num_teams="Hi")
    with pytest.raises(ValueError, match = "Number of teams must be at least 1."):
        sample.update_params(num_teams=-1)
    with pytest.raises(ValueError, match = "Number of teams must be at most 100."):
        sample.update_params(num_teams=2000)
    with pytest.raises(TypeError, match = "Average interview time cannot be converted to int."):
        sample.update_params(average_interview_time="Hi")
    with pytest.raises(ValueError, match = "Average interview time must be at least 1."):
        sample.update_params(average_interview_time=-1)
    with pytest.raises(ValueError, match = "Average interview time must be at most 600."):
        sample.update_params(average_interview_time=2000)
    with pytest.raises(TypeError, match = "Average travel time cannot be converted to int."):
        sample.update_params(average_travel_time="Hi")
    with pytest.raises(ValueError, match = "Average travel time must be at least 1."):
        sample.update_params(average_travel_time=-1)
    with pytest.raises(ValueError, match = "Average travel time must be at most 600."):
        sample.update_params(average_travel_time=2000)
    
    with pytest.raises(TypeError, match = "Average rest time cannot be converted to int."):
        sample.update_params(average_rest_time="Hi")
    with pytest.raises(ValueError, match = "Average rest time must be at least 1."):
        sample.update_params(average_rest_time=-1)
    with pytest.raises(ValueError, match = "Average rest time must be at most 600."):
        sample.update_params(average_rest_time=2000)

    with pytest.raises(ValueError, match = "Daily start time is not a valid time input."):
        sample.update_params(start_time="Hi")
    with pytest.raises(ValueError, match = "Daily end time is not a valid time input."):
        sample.update_params(end_time="Hi")

def test_update_params_all():
    """
    This method test if update_params functions properly for updating all possible attributes in a single method call.
    """
    sample = Sample()
    sample.update_params(sample_design="clustered", total_population=15000, 
                         proportion=15, margin_of_error=5, non_response=3, design_effect=1.2,
                         proportion_ind=25, margin_of_error_ind=5, non_response_ind=5, design_effect_ind=1.5, average_household_size=5.7, prop_subpopulation=12,
                         mortality_rate=0.5, margin_of_error_rate=0.3, non_response_rate=10, design_effect_rate=2,average_household_size_rate=6, recall_period=120,
                         planning_sample_size=250, num_days=10, num_enumerators_per_team=3, num_teams=5, start_time="10:30", end_time="13:30", average_interview_time=15, average_rest_time=30, average_travel_time=5)
    assert sample.sample_design == "clustered"
    assert sample.total_population == 15000
    assert sample.proportion == 15
    assert sample.margin_of_error == 5
    assert sample.non_response ==3
    assert sample.design_effect==1.2
    assert sample.proportion_ind==25
    assert sample.margin_of_error_ind==5
    assert sample.non_response_ind==5
    assert sample.design_effect_ind==1.5
    assert sample.average_household_size==5.7
    assert sample.prop_subpopulation==12
    assert sample.mortality_rate==0.5
    assert sample.margin_of_error_rate==0.3
    assert sample.non_response_rate==10
    assert sample.design_effect_rate==2
    assert sample.average_household_size_rate==6
    assert sample.recall_period==120
    assert sample.planning_sample_size==250
    assert sample.num_days==10
    assert sample.num_enumerators_per_team==3
    assert sample.num_teams==5
    assert sample.start_time==time(10,30)
    assert sample.end_time==time(13,30)
    assert sample.average_interview_time==15
    assert sample.average_rest_time==30
    assert sample.average_travel_time==5

def test_general_sample_size_case_valid():
    """
    This method tests a series of valid sample size inputs generalized sample size calculations.
    For simple random and fpc related sample size calculations, expected values tested against the UKSamples Calculator (https://uksamples.co.uk/sample-size-calculator?utm_source=chatgpt.com#col_b_design_effect) 
    For cluster sample size calculations, expected values tested against SMART Initiative ENA Software (https://smartmethodology.org/survey-planning-tools/smart-emergency-nutrition-assessment/)
    Some differences noted with ENA and fpc calculations. Not expecting alignment on this for now. Needs followup.
    Given some small background differences in various sample size calculators, this test evaluates for results within a 3% relative difference (or absolute difference of 1 for very small sample sizes).
     
    """
    # Simple random sampling
    sample = Sample(total_population=5000, sample_design="simple_random", proportion=50, margin_of_error=10, non_response=0, design_effect=1, fpc=True)
    assert math.isclose(sample.calculate_sample_size(), 94, rel_tol=0.03)
    sample = Sample(total_population=5000, sample_design="simple_random", proportion=50, margin_of_error=10, non_response=0, design_effect=1, fpc=False)
    assert math.isclose(sample.calculate_sample_size(), 97, rel_tol=0.03)
    sample = Sample(total_population=50000, sample_design="simple_random", proportion=50, margin_of_error=10, non_response=0, design_effect=1, fpc=True)
    assert math.isclose(sample.calculate_sample_size(), 96, rel_tol=0.03)
    sample = Sample(total_population=50000, sample_design="simple_random", proportion=50, margin_of_error=10, non_response=0, design_effect=1, fpc=False)
    assert math.isclose(sample.calculate_sample_size(), 97, rel_tol=0.03)

    sample = Sample(total_population=5000, sample_design="simple_random", proportion=5, margin_of_error=10, non_response=0, design_effect=1, fpc=True)
    assert abs(sample.calculate_sample_size() - 18) <= 1
    sample = Sample(total_population=5000, sample_design="simple_random", proportion=5, margin_of_error=10, non_response=0, design_effect=1, fpc=False)
    assert abs(sample.calculate_sample_size() - 18) <= 1
    sample = Sample(total_population=50000, sample_design="simple_random", proportion=5, margin_of_error=10, non_response=0, design_effect=1, fpc=True)
    assert abs(sample.calculate_sample_size() - 18) <= 1
    sample = Sample(total_population=50000, sample_design="simple_random", proportion=5, margin_of_error=10, non_response=0, design_effect=1, fpc=False)
    assert abs(sample.calculate_sample_size() - 18) <= 1

    sample = Sample(total_population=5000, sample_design="simple_random", proportion=50, margin_of_error=5, non_response=0, design_effect=1, fpc=True)
    assert math.isclose(sample.calculate_sample_size(), 357, rel_tol=0.03)
    sample = Sample(total_population=5000, sample_design="simple_random", proportion=50, margin_of_error=5, non_response=0, design_effect=1, fpc=False)
    assert math.isclose(sample.calculate_sample_size(), 384, rel_tol=0.03)
    sample = Sample(total_population=50000, sample_design="simple_random", proportion=50, margin_of_error=5, non_response=0, design_effect=1, fpc=True)
    assert math.isclose(sample.calculate_sample_size(), 381, rel_tol=0.03)
    sample = Sample(total_population=50000, sample_design="simple_random", proportion=50, margin_of_error=5, non_response=0, design_effect=1, fpc=False)
    assert math.isclose(sample.calculate_sample_size(), 384, rel_tol=0.03)

    # Clustered designs
    sample = Sample(total_population=5000, sample_design="clustered", proportion=50, margin_of_error=10, non_response=0, design_effect=1.2, fpc=True)
    assert not math.isclose(sample.calculate_sample_size(), 106, rel_tol=0.03) # NOT because apparent differences in how ENA handles fpc adjustments. 
    sample = Sample(total_population=5000, sample_design="clustered", proportion=50, margin_of_error=10, non_response=0, design_effect=1.2, fpc=False)
    assert math.isclose(sample.calculate_sample_size(), 125, rel_tol=0.03)
    sample = Sample(total_population=50000, sample_design="clustered", proportion=50, margin_of_error=10, non_response=0, design_effect=1.2, fpc=True)
    assert math.isclose(sample.calculate_sample_size(), 123, rel_tol=0.03)
    sample = Sample(total_population=50000, sample_design="clustered", proportion=50, margin_of_error=10, non_response=0, design_effect=1.2, fpc=False)
    assert math.isclose(sample.calculate_sample_size(), 125, rel_tol=0.03)

def test_ind_to_hh_sample_size_case_valid():
    """
    This method tests a series of valid sample size inputs for individual sample size calculations and the household conversions.
    For expected values, results are used from SMART Initiative ENA Software (https://smartmethodology.org/survey-planning-tools/smart-emergency-nutrition-assessment/)
    Some differences noted with ENA and fpc calculations with ENA getting smaller sample sizes. Not expecting alignment on this for now. Needs followup.
    Given some small background differences in various sample size calculators, this test evaluates for results within a 3% relative difference (or absolute difference of 1 for very small sample sizes).
    """
    # When converting individuals to households, ENA makes an additional 0.9 correction to the proportion of the sub-population in order to adjust for children 0-5 months.
    # This wont be done for IPHRA app to allow the sample size calculator to be more generalizable. A note will be made for the user to do this manually if needed.
    # For testing below, we will account for the 0.9 adjustment against ENA as the comparison.

    # Simple random sampling
    sample = Sample(total_population=5000, sample_design="simple_random", proportion_ind=50, margin_of_error_ind=10, non_response_ind=0, design_effect_ind=1, fpc=True, average_household_size=5.5, prop_subpopulation=20)
    # NOT because apparent differences in how ENA handles fpc adjustments.
    assert not math.isclose(sample.calculate_sample_size_ind_to_hh()[0], 87, rel_tol=0.03) # individuals
    assert not math.isclose(sample.calculate_sample_size_ind_to_hh()[1], 88*0.9, rel_tol=0.03) # households
    sample = Sample(total_population=5000, sample_design="simple_random", proportion_ind=50, margin_of_error_ind=10, non_response_ind=0, design_effect_ind=1, fpc=False, average_household_size=5.5, prop_subpopulation=20)
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[0], 96, rel_tol=0.03) # individuals
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[1], 97*0.9, rel_tol=0.03) # households
    sample = Sample(total_population=50000, sample_design="simple_random", proportion_ind=50, margin_of_error_ind=10, non_response_ind=0, design_effect_ind=1, fpc=True, average_household_size=5.5, prop_subpopulation=20)
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[0], 95, rel_tol=0.03) # individuals
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[1], 96*0.9, rel_tol=0.03) # households
    sample = Sample(total_population=50000, sample_design="simple_random", proportion_ind=50, margin_of_error_ind=10, non_response_ind=0, design_effect_ind=1, fpc=False, average_household_size=5.5, prop_subpopulation=20)
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[0], 96, rel_tol=0.03) # individuals
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[1], 97*0.9, rel_tol=0.03) # households

    sample = Sample(total_population=5000, sample_design="simple_random", proportion_ind=5, margin_of_error_ind=10, non_response_ind=0, design_effect_ind=1, fpc=True, average_household_size=5.5, prop_subpopulation=20)
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[0], 18, abs_tol = 1) # individuals
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[1], 18*0.9, abs_tol = 1) # households
    sample = Sample(total_population=5000, sample_design="simple_random", proportion_ind=5, margin_of_error_ind=10, non_response_ind=0, design_effect_ind=1, fpc=False, average_household_size=5.5, prop_subpopulation=20)
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[0], 18, abs_tol = 1) # individuals
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[1], 18*0.9, abs_tol = 1) # households
    sample = Sample(total_population=50000, sample_design="simple_random", proportion_ind=5, margin_of_error_ind=10, non_response_ind=0, design_effect_ind=1, fpc=True, average_household_size=5.5, prop_subpopulation=20)
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[0], 18, abs_tol = 1) # individuals
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[1], 18*0.9, abs_tol = 1) # households
    sample = Sample(total_population=50000, sample_design="simple_random", proportion_ind=5, margin_of_error_ind=10, non_response_ind=0, design_effect_ind=1, fpc=False, average_household_size=5.5, prop_subpopulation=20)
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[0], 18, abs_tol = 1) # individuals
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[1], 18*0.9, abs_tol = 1) # households

    sample = Sample(total_population=5000, sample_design="simple_random", proportion_ind=50, margin_of_error_ind=5, non_response_ind=0, design_effect_ind=1, fpc=True, average_household_size=5.5, prop_subpopulation=20)
    # NOT because apparent differences in how ENA handles fpc adjustments.
    assert not math.isclose(sample.calculate_sample_size_ind_to_hh()[0], 269, rel_tol=0.03) # individuals
    assert not math.isclose(sample.calculate_sample_size_ind_to_hh()[1], 272*0.9, rel_tol=0.03) # households
    sample = Sample(total_population=5000, sample_design="simple_random", proportion_ind=50, margin_of_error_ind=5, non_response_ind=0, design_effect_ind=1, fpc=False, average_household_size=5.5, prop_subpopulation=20)
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[0], 384, rel_tol=0.03) # individuals
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[1], 388*0.9, rel_tol=0.03) # households
    sample = Sample(total_population=50000, sample_design="simple_random", proportion_ind=50, margin_of_error_ind=5, non_response_ind=0, design_effect_ind=1, fpc=True, average_household_size=5.5, prop_subpopulation=20)
    # NOT because apparent differences in how ENA handles fpc adjustments.
    assert not math.isclose(sample.calculate_sample_size_ind_to_hh()[0], 368, rel_tol=0.03) # individuals
    assert not math.isclose(sample.calculate_sample_size_ind_to_hh()[1], 372*0.9, rel_tol=0.03) # households
    sample = Sample(total_population=50000, sample_design="simple_random", proportion_ind=50, margin_of_error_ind=5, non_response_ind=0, design_effect_ind=1, fpc=False, average_household_size=5.5, prop_subpopulation=20)
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[0], 384, rel_tol=0.03) # individuals
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[1], 388*0.9, rel_tol=0.03) # households

    # # Clustered designs

    sample = Sample(total_population=5000, sample_design="clustered", proportion_ind=50, margin_of_error_ind=5, non_response_ind=0, design_effect_ind=1.2, fpc=True, average_household_size=5.5, prop_subpopulation=20)
    # NOT because apparent differences in how ENA handles fpc adjustments.
    assert not math.isclose(sample.calculate_sample_size_ind_to_hh()[0], 322, rel_tol=0.03) # individuals
    assert not math.isclose(sample.calculate_sample_size_ind_to_hh()[1], 326*0.9, rel_tol=0.03) # households
    sample = Sample(total_population=5000, sample_design="clustered", proportion_ind=50, margin_of_error_ind=5, non_response_ind=0, design_effect_ind=1.2, fpc=False, average_household_size=5.5, prop_subpopulation=20)
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[0], 502, rel_tol=0.03) # individuals
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[1], 507*0.9, rel_tol=0.03) # households
    sample = Sample(total_population=50000, sample_design="clustered", proportion_ind=50, margin_of_error_ind=5, non_response_ind=0, design_effect_ind=1.2, fpc=True, average_household_size=5.5, prop_subpopulation=20)
    # NOT because apparent differences in how ENA handles fpc adjustments.
    assert not math.isclose(sample.calculate_sample_size_ind_to_hh()[0], 475, rel_tol=0.03) # individuals
    assert not math.isclose(sample.calculate_sample_size_ind_to_hh()[1], 480*0.9, rel_tol=0.03) # households
    sample = Sample(total_population=50000, sample_design="clustered", proportion_ind=50, margin_of_error_ind=5, non_response_ind=0, design_effect_ind=1.2, fpc=False, average_household_size=5.5, prop_subpopulation=20)
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[0], 502, rel_tol=0.03) # individuals
    assert math.isclose(sample.calculate_sample_size_ind_to_hh()[1], 507*0.9, rel_tol=0.03) # households

def test_mortality_rate_sample_size_case_valid():
    sample = Sample(total_population=5000, sample_design="simple_random", mortality_rate=0.5, margin_of_error_rate=0.4, non_response_rate=0, design_effect_rate=1, fpc=True, average_household_size_rate=5.5, recall_period=93)
    
    assert math.isclose(sample.calculate_sample_size_mortality_rate()[0], 1026, rel_tol=0.03) # individuals
    assert math.isclose(sample.calculate_sample_size_mortality_rate()[1], 93*1026, rel_tol=0.03) # person-time
    assert math.isclose(sample.calculate_sample_size_mortality_rate()[2], 187, rel_tol=0.03) # households

    
    


    type(sample.recall_period)
    type(sample.margin_of_error_rate)


# def test_sample_invalid_population():
#     with pytest.raises(ValueError):
#         Sample(total_population=-10)  # if you raise error in __init__ for invalid

# sample = Sample(total_population=-10) 
# sample.total_population

# def test_mutable_defaults_are_independent():
#     sample1 = Sample()
#     sample2 = Sample()
#     # if you had a mutable attribute, e.g. self.my_list = [] in __init__, check:
#     assert sample1.my_list is not sample2.my_list

