import sys
from unittest import result

# import functions
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QLineEdit

# import generated ui class
from ui.iphra_app_ui import Ui_MainWindow

# import logic and validation functions
import logic.tab2_samplesize as ss
from logic.validators import validate_type, validate_int, validate_float

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    # Connect the button clicked signal to your handler function
        self.ui.ss_hh_calculate.clicked.connect(self.sample_size_handle_calculate)
        self.ui.ss_ind_calculate.clicked.connect(self.sample_size_ind_handle_calculate)
        self.ui.ss_mortality_calculate.clicked.connect(self.sample_size_mortality_rate_calculate)

    # ✅ Set default radio button
        self.ui.ss_srs_select.setChecked(True)

    def handle_calculate(self):
        print("Calculate button clicked!")

    def sample_size_handle_calculate(self):

        print("THE BUTTON WAS CLICKED!")

        try :
            # Read inputs as strings
            margin_of_error = self.ui.ss_hh_precision_input.text()
            proportion = self.ui.ss_hh_prev_input.text()
            design_effect = self.ui.ss_hh_deff_input.text()
            non_response = self.ui.ss_hh_nonresponse_input.text()
            population_size = self.ui.ss_total_pop_input.text()
            if self.ui.ss_srs_select.isChecked() :
                sample_design = 'simple_random'
            elif self.ui.ss_systematic_select.isChecked() :
                sample_design = 'stratified'
            elif self.ui.ss_clustersampling.isChecked() :
                sample_design = 'clustered'

            print("THE INPUTS ARE READ!")

            # Validate input types
            if not validate_type(sample_design, str, "Sample Design", self):
                return  # Stop further processing gracefully
            if not validate_type(population_size, int, "Population Size", self):
                return  # Stop further processing gracefully
            if not validate_type(proportion, float, "Proportion", self):
                return  # Stop further processing gracefully
            if not validate_type(margin_of_error, float, "Margin of Error", self):
                return  # Stop further processing gracefully
            if not validate_type(non_response, float, "Non-Response Rate", self):
                return  # Stop further processing gracefully
            if not validate_type(design_effect, float, "Design Effect", self):
                return  # Stop further processing gracefully

            print("THE INPUTS TYPES ARE VALIDATED!")

            # Validate input values
            if sample_design not in ['simple_random', 'stratified', 'clustered']:
                return  # Stop further processing gracefully
            ok, proportion_value = validate_float(proportion, "Proportion", min_value=0, max_value=100, parent=self)
            if not ok:
                return  # Stop further processing gracefully
            ok, margin_of_error_value = validate_float(margin_of_error, "Margin of Error", min_value=0, max_value=100, parent=self)
            if not ok:
                return  # Stop further processing gracefully
            ok, non_response_value = validate_float(non_response, "Non-Response Rate", min_value=0, max_value=100, parent=self)
            if not ok:
                return  # Stop further processing gracefully
            ok, design_effect_value = validate_float(design_effect, "Design Effect", min_value=1, parent=self)
            if not ok:
                return  # Stop further processing gracefully
            ok, population_size_value = validate_int(population_size, "Population Size", min_value=1, parent=self)
            if not ok:
                return  # Stop further processing gracefully

            print("THE INPUTS VALUES ARE VALIDATED!")

            # Call calculation function for sample size
            result = ss.calculate_sample_size(
                sample_design=sample_design,
                population_size=int(population_size_value),
                proportion=float(proportion_value),
                margin_of_error=float(margin_of_error_value),
                non_response=float(non_response_value),
                design_effect=float(design_effect_value)
            )

            print("THE RESULT WAS CALCULATED!")

            print("Result calculated:", result)
            
            # Display result
            self.ui.ss_hh_result_value.setText(str(result))

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric inputs.")

    def sample_size_ind_handle_calculate(self):
        print("THE BUTTON WAS CLICKED!")

        try :
            # Read inputs as strings
            margin_of_error = self.ui.ss_ind_precision_input.text()
            proportion = self.ui.ss_ind_prev_input.text()
            design_effect = self.ui.ss_ind_deff_input.text()
            non_response = self.ui.ss_ind_nonresponse_input.text()
            population_size = self.ui.ss_total_pop_input.text()
            household_size = self.ui.ss_ind_hhsize_input.text()
            prop_subpopulation = self.ui.ss_ind_proppop_input.text()

            if self.ui.ss_srs_select.isChecked() :
                sample_design = 'simple_random'
            elif self.ui.ss_systematic_select.isChecked() :
                sample_design = 'stratified'
            elif self.ui.ss_clustersampling.isChecked() :
                sample_design = 'clustered'

            print("THE INPUTS ARE READ!")

            # Validate input types
            if not validate_type(sample_design, str, "Sample Design", self):
                return  # Stop further processing gracefully
            if not validate_type(population_size, int, "Population Size", self):
                return  # Stop further processing gracefully
            if not validate_type(proportion, float, "Proportion", self):
                return  # Stop further processing gracefully
            if not validate_type(margin_of_error, float, "Margin of Error", self):
                return  # Stop further processing gracefully
            if not validate_type(non_response, float, "Non-Response Rate", self):
                return  # Stop further processing gracefully
            if not validate_type(design_effect, float, "Design Effect", self):
                return  # Stop further processing gracefully
            if not validate_type(household_size, float, "Household Size", self):
                return  # Stop further processing gracefully
            if not validate_type(prop_subpopulation, float, "Proportion of Subpopulation", self):
                return  # Stop further processing gracefully

            print("THE INPUTS TYPES ARE VALIDATED!")

            # Validate input values
            if sample_design not in ['simple_random', 'stratified', 'clustered']:
                return  # Stop further processing gracefully
            ok, proportion_value = validate_float(proportion, "Proportion", min_value=0, max_value=100, parent=self)
            if not ok:
                return  # Stop further processing gracefully
            ok, margin_of_error_value = validate_float(margin_of_error, "Margin of Error", min_value=0, max_value=100, parent=self)
            if not ok:
                return  # Stop further processing gracefully
            ok, non_response_value = validate_float(non_response, "Non-Response Rate", min_value=0, max_value=100, parent=self)
            if not ok:
                return  # Stop further processing gracefully
            ok, design_effect_value = validate_float(design_effect, "Design Effect", min_value=1, parent=self)
            if not ok:
                return  # Stop further processing gracefully
            ok, population_size_value = validate_int(population_size, "Population Size", min_value=1, parent=self)
            if not ok:
                return  # Stop further processing gracefully
            ok, household_size_value = validate_float(household_size, "Household Size", min_value=1, parent=self)
            if not ok:
                return  # Stop further processing gracefully
            ok, prop_subpopulation_value = validate_float(prop_subpopulation, "Proportion of Subpopulation", min_value=0, max_value=100, parent=self)
            if not ok:
                return  # Stop further processing gracefully

            print("THE INPUTS VALUES ARE VALIDATED!")

            # Call calculation function for sample size
            result_ind, result_hh = ss.calculate_sample_size_ind_to_hh(
                sample_design=sample_design,
                population_size=int(population_size_value),
                proportion=float(proportion_value),
                margin_of_error=float(margin_of_error_value),
                non_response=float(non_response_value),
                design_effect=float(design_effect_value),
                household_size=float(household_size_value),
                prop_subpopulation=float(prop_subpopulation_value)
            )

            print("THE RESULT WAS CALCULATED!")

            print("Result calculated:", result_ind, result_hh)
            
            # Display result
            self.ui.ss_ind_result_value.setText(str(result_ind))
            self.ui.ss_ind_hh_result_value.setText(str(result_hh))

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric inputs.")

    def sample_size_mortality_rate_calculate(self):
        print("THE BUTTON WAS CLICKED!")

        try:
            # Read inputs as strings
            mortality_rate = self.ui.ss_mortality_rate_input.text()
            margin_of_error = self.ui.ss_mortality_precision_input.text()
            design_effect = self.ui.ss_mortality_deff_input.text()
            non_response = self.ui.ss_mortality_nonresponse_input.text()
            population_size = self.ui.ss_total_pop_input.text()
            recall_days = self.ui.ss_mortality_days_input.text()
            household_size = self.ui.ss_mortality_hhsize_input.text()
            
            if self.ui.ss_srs_select.isChecked() :
                sample_design = 'simple_random'
            elif self.ui.ss_systematic_select.isChecked() :
                sample_design = 'stratified'
            elif self.ui.ss_clustersampling.isChecked() :
                sample_design = 'clustered'

            print("THE INPUTS ARE READ!")

            # Validate input types
            if not validate_type(sample_design, str, "Sample Design", self):
                return  # Stop further processing gracefully
            if not validate_type(population_size, int, "Population Size", self):
                return  # Stop further processing gracefully
            if not validate_type(mortality_rate, float, "Mortality Rate", self):
                return  # Stop further processing gracefully
            if not validate_type(recall_days, int, "Recall Days", self):
                return  # Stop further processing gracefully
            if not validate_type(household_size, float, "Household Size", self):
                return  # Stop further processing gracefully
            if not validate_type(margin_of_error, float, "Margin of Error", self):
                return  # Stop further processing gracefully
            if not validate_type(non_response, float, "Non-Response Rate", self):
                return  # Stop further processing gracefully
            if not validate_type(design_effect, float, "Design Effect", self):
                return  # Stop further processing gracefully

            print("THE INPUTS TYPES ARE VALIDATED!")

            # Validate input values
            if sample_design not in ['simple_random', 'stratified', 'clustered']:
                return  # Stop further processing gracefully
            ok, mortality_rate_value = validate_float(mortality_rate, "Mortality Rate", min_value=0, max_value=10, parent=self)
            if not ok:
                return  # Stop further processing gracefully
            ok, recall_days_value = validate_int(recall_days, "Recall Days", min_value=1, parent=self)
            if not ok:
                return  # Stop further processing gracefully
            ok, household_size_value = validate_float(household_size, "Household Size", min_value=1, parent=self)
            if not ok:
                return  # Stop further processing gracefully
            ok, margin_of_error_value = validate_float(margin_of_error, "Margin of Error", min_value=0, max_value=100, parent=self)
            if not ok:
                return  # Stop further processing gracefully
            ok, non_response_value = validate_float(non_response, "Non-Response Rate", min_value=0, max_value=100, parent=self)
            if not ok:
                return  # Stop further processing gracefully
            ok, design_effect_value = validate_float(design_effect, "Design Effect", min_value=1, parent=self)
            if not ok:
                return  # Stop further processing gracefully
            ok, population_size_value = validate_int(population_size, "Population Size", min_value=1, parent=self)
            if not ok:
                return  # Stop further processing gracefully

            print("THE INPUTS VALUES ARE VALIDATED!")

            # Call calculation function for sample size
            result_ind, result_person_time, result_hh = ss.calculate_sample_size_mortality_rate(
                sample_design=sample_design,
                population_size=int(population_size_value),
                mortality_rate=float(mortality_rate_value),
                recall_period=int(recall_days_value),
                margin_of_error=float(margin_of_error_value),
                non_response=float(non_response_value),
                design_effect=float(design_effect_value),
                household_size=float(household_size_value)
            )

            print("THE RESULT WAS CALCULATED!")

            print("Result calculated:", result_ind, result_person_time, result_hh)
            
            # Display result
            self.ui.ss_mortality_ind_value.setText(str(result_ind))
            self.ui.ss_mortality_persontime_value.setText(str(result_person_time))
            self.ui.ss_mortality_hh_value.setText(str(result_hh))

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric inputs.")

    def sample_size_planning_handle_calculate(self):
        print("THE BUTTON WAS CLICKED!")

        try:
            # Read inputs as strings
            start_time = self.ui.ss_planning_start_time.text()
            end_time = self.ui.ss_planning_end_time.text()
            enumerators_per_team = self.ui.ss_planning_enumerators_per_team.text()
            interviews_per_enumerator_per_day = self.ui.ss_planning_interviews_per_enumerator_per_day.text()
            sample_size = self.ui.ss_planning_sample_size.text()

            if self.ui.ss_srs_select.isChecked() :
                sample_design = 'simple_random'
            elif self.ui.ss_systematic_select.isChecked() :
                sample_design = 'stratified'
            elif self.ui.ss_clustersampling.isChecked() :
                sample_design = 'clustered'

            print("THE INPUTS ARE READ!")

            # Validate input types
            if not validate_type(sample_design, str, "Sample Design", self):
                return  # Stop further processing gracefully
            if not validate_type(start_time, str, "Start Time", self):
                return  # Stop further processing gracefully
            if not validate_type(end_time, str, "End Time", self):
                return  # Stop further processing gracefully
            if not validate_type(enumerators_per_team, int, "Enumerators per Team", self):
                return  # Stop further processing gracefully
            if not validate_type(interviews_per_enumerator_per_day, int, "Interviews per Enumerator per Day", self):
                return  # Stop further processing gracefully
            if not validate_type(sample_size, int, "Sample Size", self):
                return  # Stop further processing gracefully

            print("THE INPUTS TYPES ARE VALIDATED!")

            # Validate input values
            ok, enumerators_value = validate_int(enumerators_per_team, "Enumerators per Team", min_value=1, parent=self)
            if not ok:
                return  # Stop further processing gracefully
            ok, interviews_value = validate_int(interviews_per_enumerator_per_day, "Interviews per Enumerator per Day", min_value=1, parent=self)
            if not ok:
                return  # Stop further processing gracefully
            ok, sample_size_value = validate_int(sample_size, "Sample Size", min_value=1, parent=self)
            if not ok:
                return  # Stop further processing gracefully

            print("THE INPUTS VALUES ARE VALIDATED!")

            # Call calculation function for sample size planning
            number_psu_needed, days_required = ss.calculate_sample_size_planning(
                sample_design=sample_design,    
                start_time=start_time,
                end_time=end_time,
                enumerators_per_team=int(enumerators_value),
                interviews_per_enumerator_per_day=int(interviews_value),
                sample_size=int(sample_size_value)
            )
            print("THE RESULT WAS CALCULATED!")
            print("Result calculated:", number_psu_needed, days_required)

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric inputs.")
 









def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()