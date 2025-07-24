

def test_calculate_sample_size_srs_p0_e05_case(): # edge case with proportion 0
    """
    Test sample size calculation for an extreme simple or systematic sampling design case.
    Proportion is 0%, margin of error is 5%. 
    Non-response rate is 10%.
    Population size is 20,000.
    Design effect is 1.0 (not used in SRS).
    Expect the sample size to match known manual result.
    """
    result = ss.calculate_sample_size(sample_design="simple_random", population_size=20000, proportion=0, margin_of_error=5, non_response=10)
    """
    Test sample size calculation for simple or systematic sampling design extreme case with proportion 0.
    Proportion is 0%, margin of error is 5%. 
    Non-response rate is 10%.
    Population size is 20,000.
    Design effect is 1.0 (not used in SRS).
    Expect the sample size to match known manual result.
    """
    n0 = (1.96**2 * 0 * (1-0)) / (0.05**2)
    expected = math.ceil((n0 / (1 + (n0 - 1) / 20000)) / (1 - 0.1))
    assert abs(result - expected) == 0  # exact result since proportion is 0

def test_calculate_sample_size_srs_p100_e05_case(): # edge case with proportion 100
    """
    Test sample size calculation for simple or systematic sampling design case with proportion 100.
    Proportion is 100%, margin of error is 5%. 
    Non-response rate is 10%.
    Population size is 20,000.
    Design effect is 1.0 (not used in SRS).
    Expect the sample size to match known manual result.
    """
    result = ss.calculate_sample_size(sample_design="simple_random", population_size=20000, proportion=100, margin_of_error=5, non_response=10)
    n0 = (1.96**2 * 1 * (1-1)) / (0.05**2)
    expected = math.ceil((n0 / (1 + (n0 - 1) / 20000)) / (1 - 0.1))
    assert abs(result - expected) == 0  # exact result since proportion is 100

def test_calculate_sample_size_srs_p50_e100_case(): # edge case with moe of %50
    """
    Test sample size calculation for simple or systematic sampling design case with moe of 50.
    Proportion is 50%, margin of error is 50%. 
    Non-response rate is 10%.
    Population size is 20,000.
    Design effect is 1.0 (not used in SRS).
    Expect the sample size to match known manual result.
    """
    result = ss.calculate_sample_size(sample_design="simple_random", population_size=20000, proportion=100, margin_of_error=50, non_response=10)
    n0 = (1.96**2 * 0.5 * (1-0.5)) / (0.5**2)
    expected = math.ceil((n0 / (1 + (n0 - 1) / 20000)) / (1 - 0.1))
    assert abs(result - expected) == 0  # edge case with moe of 50

def test_calculate_sample_size_srs_p50_e0005_case(): # edge case with moe of 0.05%
    """
    Test sample size calculation for simple or systematic sampling design case with moe 0.05%.
    Proportion is 50%, margin of error is 0.05%. 
    Non-response rate is 10%.
    Population size is 20,000.
    Design effect is 1.0 (not used in SRS).
    Expect the sample size to match known manual result.
    """
    result = ss.calculate_sample_size(sample_design="simple_random", population_size=20000, proportion=50, margin_of_error=0.05, non_response=10)
    n0 = (1.96**2 * 0.5 * (1-0.5)) / (0.0005**2)
    expected = math.ceil((n0 / (1 + (n0 - 1) / 20000)) / (1 - 0.1))
    assert abs(result - expected) == 0  # edge case with moe of %0.05

def test_calculate_sample_size_srs_fpc500_case(): # fpc edge case with population of 500
    """
    Test sample size calculation for simple or systematic sampling design case with small population of 500. This should accurately correct for fpc. 
    Proportion is 50%, margin of error is 5%. 
    Non-response rate is 10%.
    Population size is 500.
    Design effect is 1.0 (not used in SRS).
    Expect the sample size to match known manual result.
    """
    result = ss.calculate_sample_size(sample_design="simple_random", population_size=500, proportion=0.5, margin_of_error=0.05, non_response=0.1)
    n0 = (1.96**2 * 0.5 * (1-0.5)) / (0.05**2)
    expected = math.ceil((n0 / (1 + (n0 - 1) / 500)) / (1 - 0.1))
    assert abs(result - expected) == 0  # edge case with population of 500

def test_calculate_sample_size_srs_fpc50000_case(): # fpc edge case with population of 50000
    """
    Test sample size calculation for simple or systematic sampling design case with a large population of 50000.
    Proportion is 50%, margin of error is 5%. 
    Non-response rate is 10%.
    Population size is 50,000.
    Design effect is 1.0 (not used in SRS).
    Expect the sample size to match known manual result.
    """
    result = ss.calculate_sample_size(sample_design="simple_random", population_size=50000, proportion=0.5, margin_of_error=0.05, non_response=0.1)
    n0 = (1.96**2 * 0.5 * (1-0.5)) / (0.05**2)
    expected = math.ceil((n0 / (1 + (n0 - 1) / 50000)) / (1 - 0.1))
    assert abs(result - expected) == 0  

def test_calculate_sample_size_srs_nr0_case(): # fpc edge case with nonresponse of 0
    """
    Test sample size calculation for simple or systematic sampling design case with non-response of 0%. 
    Proportion is 0.05%, margin of error is 0.05%. 
    Non-response rate is 10%.
    Population size is 500.
    Design effect is 1.0 (not used in SRS).
    Expect the sample size to match known manual result.
    """
    result = ss.calculate_sample_size(sample_design="simple_random", population_size=50000, proportion=0.5, margin_of_error=0.05, non_response=0)
    n0 = (1.96**2 * 0.5 * (1-0.5)) / (0.05**2)
    expected = math.ceil((n0 / (1 + (n0 - 1) / 50000)) / (1 - 0.1))
    assert abs(result - expected) == 0  


# Tests for Clustered sample design

def test_calculate_sample_size_clustered_p50_e05_case():
    """
    Test sample size calculation for a typical cluster design case.
    Expect the sample size to match known manual result.
    """
    result = ss.calculate_sample_size(sample_design="clustered", population_size=20000, proportion=50, margin_of_error=5, non_response=10, design_effect=1.5)
    n0 = (2.045**2 * 0.5 * (1 - 0.5)) / (0.05**2)
    n = (n0 / (1 + (n0 - 1) / 20000)) * 1.5
    expected = math.ceil(n) / (1 - 0.1)
    assert abs(result - expected) == 0  # tolerance for float comparison

def test_calculate_sample_size_srs_p0_e05_case(): # edge case with proportion 0
    result = ss.calculate_sample_size(sample_design="clustered", population_size=20000, proportion=0, margin_of_error=5, non_response=10)
    n0 = (2.045**2 * 0.5 * (1 - 0.5)) / (0.05**2)
    n = (n0 / (1 + (n0 - 1) / 20000)) * 1.5
    expected = math.ceil(n) / (1 - 0.1)
    assert abs(result - expected) == 0  # exact result since proportion is 0

def test_calculate_sample_size_srs_p100_e05_case(): # edge case with proportion 100
    result = ss.calculate_sample_size(sample_design="clustered", population_size=20000, proportion=100, margin_of_error=5, non_response=10)
    n0 = (1.96**2 * 1 * (1-1)) / (0.05**2)
    expected = math.ceil((n0 / (1 + (n0 - 1) / 20000)) / (1 - 0.1))
    assert abs(result - expected) == 0  # exact result since proportion is 100

def test_calculate_sample_size_srs_p50_e100_case(): # edge case with moe of %50
    result = ss.calculate_sample_size(sample_design="clustered", population_size=20000, proportion=100, margin_of_error=0.05, non_response=10)
    n0 = (1.96**2 * 0.5 * (1-0.5)) / (0.5**2)
    expected = math.ceil((n0 / (1 + (n0 - 1) / 20000)) / (1 - 0.1))
    assert abs(result - expected) == 0  # edge case with moe of 50

def test_calculate_sample_size_srs_p50_e0005_case(): # edge case with moe of 0.05%
    result = ss.calculate_sample_size(sample_design="clustered", population_size=20000, proportion=50, margin_of_error=0.05, non_response=10)
    n0 = (1.96**2 * 0.5 * (1-0.5)) / (0.0005**2)
    expected = math.ceil((n0 / (1 + (n0 - 1) / 20000)) / (1 - 0.1))
    assert abs(result - expected) == 0  # edge case with moe of %0.05

def test_calculate_sample_size_srs_fpc500_case(): # fpc edge case with population of 500
    result = ss.calculate_sample_size(sample_design="clustered", population_size=500, proportion=0.5, margin_of_error=0.05, non_response=0.1)
    n0 = (1.96**2 * 0.5 * (1-0.5)) / (0.05**2)
    expected = math.ceil((n0 / (1 + (n0 - 1) / 500)) / (1 - 0.1))
    assert abs(result - expected) == 0  # edge case with population of 500

def test_calculate_sample_size_srs_fpc50000_case(): # fpc edge case with population of 50000
    result = ss.calculate_sample_size(sample_design="clustered", population_size=50000, proportion=0.5, margin_of_error=0.05, non_response=0.1)
    n0 = (1.96**2 * 0.5 * (1-0.5)) / (0.05**2)
    expected = math.ceil((n0 / (1 + (n0 - 1) / 50000)) / (1 - 0.1))
    assert abs(result - expected) == 0  

def test_calculate_sample_size_srs_nr0_case(): # fpc edge case with nonresponse of 0
    result = ss.calculate_sample_size(sample_design="clustered", population_size=50000, proportion=0.5, margin_of_error=0.05, non_response=0)
    n0 = (1.96**2 * 0.5 * (1-0.5)) / (0.05**2)
    expected = math.ceil((n0 / (1 + (n0 - 1) / 50000)) / (1 - 0.1))
    assert abs(result - expected) == 0  






