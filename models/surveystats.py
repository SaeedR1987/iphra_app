class SurveyStats:
    def __init__(self, 
                 data: pd.DataFrame, 
                 weight_col: str, 
                 psu_col: Optional[str] = None, 
                 strata_col: Optional[str] = None):
        """
        A wrapper for basic survey-weighted statistics using statsmodels.

        Parameters
        ----------
        data : pd.DataFrame
            Your cleaned dataset.
        weight_col : str
            Column name of the weights.
        psu_col : str, optional
            Primary Sampling Unit column (cluster).
        strata_col : str, optional
            Strata column name.
        """
        self.data = data
        self.design = sm.survey.SurveyDesignSpec(
            weights=data[weight_col],
            cluster=data[psu_col] if psu_col else None,
            strata=data[strata_col] if strata_col else None
        )
        self.survey = sm.survey.SurveyData(self.design, data)

    def mean(self, var: str, sample_design: str, z: float = 1.96) -> dict:
        """
        Calculate survey-corrected mean with CI and design effect for clustered designs.

        Parameters
        ----------
        var : str
            Variable name to calculate mean for.
        sample_design : str
            One of 'simple_random', 'systematic', or 'clustered'.
        z : float
            Z-score for CI (default 1.96 for 95%).

        Returns
        -------
        dict
            Dictionary with mean estimate, SE, CI bounds, design effect (if clustered), and method used.
        """
        est, se = self.survey.mean(var)

        weights = self.design.weights
        data = self.data[var]

        # Effective sample size approximation using Kish's formula
        n_eff = (weights.sum()) ** 2 / (weights ** 2).sum()

        # Sample variance for the variable (weighted)
        weighted_mean = est
        weighted_var_num = np.sum(weights * (data - weighted_mean) ** 2)
        weighted_var = weighted_var_num / weights.sum()

        # Variance under SRS: weighted variance divided by n_eff
        srs_variance = weighted_var / n_eff
        actual_variance = se ** 2

        if sample_design in ['simple_random', 'systematic']:
            method = "delta"
            deff = 1.0
        elif sample_design == 'clustered':
            method = "survey_corrected"
            deff = actual_variance / srs_variance if srs_variance > 0 else None
        else:
            return {
                "type": "mean",
                "error": f"Unknown sample design: {sample_design}",
                "variable": var,
                "estimate": est,
                "se": se,
                "ci_lower": None,
                "ci_upper": None,
                "design_effect": None,
                "method": None
            }

        ci_lower = est - z * se
        ci_upper = est + z * se

        return {
            "type": "mean",
            "variable": var,
            "estimate": est,
            "se": se,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "design_effect": deff,
            "method": method,
            "sample_design": sample_design
        }

    def proportion(self, var: str, sample_design: str, z: float = 1.96) -> dict:
        """
        Calculate survey-corrected proportion with CI and design effect for clustered designs.

        Parameters
        ----------
        var : str
            Variable name to calculate proportion for.
        sample_design : str
            One of 'simple_random', 'systematic', or 'clustered'.
        z : float
            Z-score for CI (default 1.96 for 95%).

        Returns
        -------
        dict
            Dictionary with proportion estimate, SE, CI bounds, design effect (if clustered), and method used.
        """
        # Get estimate and SE from survey object
        est, se = self.survey.proportion(var)

        # Calculate SRS variance for design effect calculation if clustered
        # SRS variance for a proportion: p*(1-p)/n_eff
        # We'll approximate n_eff using sum of weights squared (or total weight)
        # This depends on your design; here is a common approach:

        # Total weighted sample size approximation
        weights = self.design.weights
        n_eff = (weights.sum())**2 / (weights**2).sum()  # effective sample size (Kish's formula)
        srs_variance = est * (1 - est) / n_eff
        actual_variance = se ** 2

        if sample_design in ['simple_random', 'systematic']:
            method = "delta"
            deff = 1.0
        elif sample_design == 'clustered':
            method = "survey_corrected"
            deff = actual_variance / srs_variance if srs_variance > 0 else None
        else:
            return {
                "type": "proportion",
                "error": f"Unknown sample design: {sample_design}",
                "variable": var,
                "estimate": est,
                "se": se,
                "ci_lower": None,
                "ci_upper": None,
                "design_effect": None,
                "method": None
            }

        ci_lower = est - z * se
        ci_upper = est + z * se

        # Bound CIs between 0 and 1
        ci_lower = max(0, ci_lower)
        ci_upper = min(1, ci_upper)

        return {
            "type": "proportion",
            "variable": var,
            "estimate": est,
            "se": se,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "design_effect": deff,
            "method": method,
            "sample_design": sample_design
        }

    def ratio(self,
          numerator: str,
          denominator: str,
          sample_design: str,
          z: float = 1.96,
          min_psu_for_delta: int = 30,
          bootstrap_iterations: int = 500) -> dict:
        """
        Calculate a weighted ratio with CI based on sample design.
        Uses delta method for SRS/Systematic or clustered designs with enough PSUs;
        uses bootstrap otherwise.

        Parameters
        ----------
        numerator : str
            Numerator column.
        denominator : str
            Denominator column.
        sample_design : str
            Type of design: 'simple_random', 'systematic', 'clustered'.
        z : float
            Z-score for CI (default 1.96).
        min_psu_for_delta : int
            Threshold PSU count for delta method if clustered.
        bootstrap_iterations : int
            Iterations for bootstrapping.

        Returns
        -------
        dict
            Ratio, SE, CI, method used, PSU count.
        """
        data = self.data.copy()
        weights = self.design.weights
        psu_col = self.design.cluster.name if self.design.cluster is not None else None

        # Compute weighted numerator and denominator
        weighted_num = np.sum(data[numerator] * weights)
        weighted_den = np.sum(data[denominator] * weights)
        ratio = weighted_num / weighted_den if weighted_den != 0 else np.nan

        # Determine PSU count (if applicable)
        if psu_col:
            unique_psus = data[psu_col].nunique()
        else:
            unique_psus = None

        # Decide method
        if sample_design in ['simple_random', 'systematic']:
            method = 'delta'
        elif sample_design == 'clustered':
            if unique_psus is not None and unique_psus < min_psu_for_delta:
                method = 'bootstrap'
            else:
                method = 'delta'
        else:
            return {
                "type": "ratio",
                "error": f"Unknown sample design: {sample_design}",
                "estimate": ratio,
                "method": None
            }

        # DELTA METHOD
        if method == 'delta':
            try:
                est_num, se_num = self.survey.mean(numerator)
                est_den, se_den = self.survey.mean(denominator)

                se_ratio = np.sqrt((se_num / weighted_den) ** 2 +
                                ((weighted_num * se_den) / (weighted_den ** 2)) ** 2)
                ci_lower = ratio - z * se_ratio
                ci_upper = ratio + z * se_ratio

                return {
                    "type": "ratio",
                    "method": "delta",
                    "sample_design": sample_design,
                    "psu_count": unique_psus,
                    "numerator": numerator,
                    "denominator": denominator,
                    "estimate": ratio,
                    "se": se_ratio,
                    "ci_lower": ci_lower,
                    "ci_upper": ci_upper
                }
            except Exception as e:
                return {
                    "type": "ratio",
                    "method": "delta",
                    "sample_design": sample_design,
                    "psu_count": unique_psus,
                    "error": str(e),
                    "estimate": ratio,
                    "se": None,
                    "ci_lower": None,
                    "ci_upper": None
                }

        # BOOTSTRAP METHOD
        elif method == 'bootstrap':
            try:
                ratios = []
                psu_list = data[psu_col].unique()

                for _ in range(bootstrap_iterations):
                    sampled_psus = np.random.choice(psu_list, size=len(psu_list), replace=True)
                    boot_df = pd.concat([data[data[psu_col] == psu_val] for psu_val in sampled_psus])
                    boot_weights = boot_df[self.design.weights.name]
                    num = np.sum(boot_df[numerator] * boot_weights)
                    den = np.sum(boot_df[denominator] * boot_weights)
                    if den != 0:
                        ratios.append(num / den)

                if len(ratios) > 0:
                    ratio_point = np.nanmean(ratios)
                    ci_lower = np.nanpercentile(ratios, 2.5)
                    ci_upper = np.nanpercentile(ratios, 97.5)
                    se = np.nanstd(ratios, ddof=1)
                else:
                    ratio_point, ci_lower, ci_upper, se = np.nan, np.nan, np.nan, np.nan

                return {
                    "type": "ratio",
                    "method": "bootstrap",
                    "sample_design": sample_design,
                    "psu_count": unique_psus,
                    "numerator": numerator,
                    "denominator": denominator,
                    "estimate": ratio_point,
                    "se": se,
                    "ci_lower": ci_lower,
                    "ci_upper": ci_upper
                }

            except Exception as e:
                return {
                    "type": "ratio",
                    "method": "bootstrap",
                    "sample_design": sample_design,
                    "psu_count": unique_psus,
                    "error": str(e),
                    "estimate": None,
                    "se": None,
                    "ci_lower": None,
                    "ci_upper": None
                }

    def median(self,
           var: str,
           sample_design: str,
           z: float = 1.96,
           bootstrap_iterations: int = 500) -> dict:
        """
        Calculate survey-corrected weighted median with bootstrap confidence intervals.

        Parameters
        ----------
        var : str
            Variable name to calculate median for.
        sample_design : str
            'simple_random', 'systematic', or 'clustered'.
        z : float
            Z-score for confidence interval (default 1.96).
        bootstrap_iterations : int
            Number of bootstrap samples.

        Returns
        -------
        dict
            Weighted median estimate and 95% CI.
        """

        data = self.data.copy()
        weights = self.design.weights
        psu_col = self.design.cluster.name if self.design.cluster is not None else None

        # Weighted median function
        def weighted_median(values, weights):
            sorter = np.argsort(values)
            values_sorted = values[sorter]
            weights_sorted = weights[sorter]
            cum_weights = np.cumsum(weights_sorted)
            cutoff = cum_weights[-1] / 2.0
            return values_sorted[cum_weights >= cutoff][0]

        # Point estimate weighted median
        median_point = weighted_median(data[var].values, weights.values)

        # Bootstrap CI
        if sample_design == "clustered" and psu_col:
            psu_list = data[psu_col].unique()
            medians = []

            for _ in range(bootstrap_iterations):
                sampled_psus = np.random.choice(psu_list, size=len(psu_list), replace=True)
                boot_df = pd.concat([data[data[psu_col] == psu_val] for psu_val in sampled_psus])
                w = boot_df[self.design.weights.name]
                vals = boot_df[var].values
                medians.append(weighted_median(vals, w.values))

        else:
            # For SRS/systematic, bootstrap individuals with weights
            medians = []
            n = len(data)
            for _ in range(bootstrap_iterations):
                indices = np.random.choice(n, size=n, replace=True)
                boot_vals = data[var].values[indices]
                boot_weights = weights.values[indices]
                medians.append(weighted_median(boot_vals, boot_weights))

        # Calculate percentile CI
        ci_lower = np.percentile(medians, 2.5)
        ci_upper = np.percentile(medians, 97.5)

        return {
            "type": "median",
            "variable": var,
            "estimate": median_point,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "method": "bootstrap",
            "bootstrap_iterations": bootstrap_iterations,
            "sample_design": sample_design
        }