import pytest
import math
from logic.tab2_samplesize import calculate_sample_size

def test_calculate_sample_size_typical_case():
    result = calculate_sample_size(sample_design="simple_random", population_size=20000, proportion=0.5, margin_of_error=0.05, non_response=0.1, design_effect=1)
    n0 = (1.96**2 * 0.5 * (1-0.5)) / (0.05**2)
    expected = math.ceil(((n0 / (1 + (n0 - 1) / 20000)) / (1 - 0.1))*1.0)
    assert abs(result - expected) < 0.01  # tolerance for float comparison

def test_calculate_sample_size_edge_case():
    result = calculate_sample_size(sample_design="simple_random", population_size=20000, proportion=0, margin_of_error=0.05, non_response=0.1, design_effect=1)
    n0 = (1.96**2 * 0 * (1-0)) / (0.05**2)
    expected = math.ceil(((n0 / (1 + (n0 - 1) / 20000)) / (1 - 0.1))*1.0)
    assert abs(result - expected) == 0  # tolerance for float comparison

def test_caluclate_sample_size_fpc_case():
    result = calculate_sample_size(sample_design="simple_random", population_size=1000, proportion=0.5, margin_of_error=0.05, non_response=0.1, design_effect=1)
    n0 = (1.96**2 * 0.5 * (1-0.5)) / (0.05**2)
    expected = math.ceil(((n0 / (1 + (n0 - 1) / 1000)) / (1 - 0.1))*1.0)
    assert abs(result - expected) < 0.01  # tolerance for float comparison

def test_caluclate_sample_size_clustered_case():
    result = calculate_sample_size(sample_design="clustered", population_size=20000, proportion=0.5, margin_of_error=0.05, non_response=0.1, design_effect=1.5)
    n0 = (1.96**2 * 0.5 * (1-0.5)) / (0.05**2)
    expected = math.ceil(((n0 / (1 + (n0 - 1) / 20000)) / (1 - 0.1))*1.5)
    assert abs(result - expected) < 0.01  # tolerance for float comparison