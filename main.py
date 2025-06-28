import sys

# import functions
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QLineEdit

# import generated ui class
from ui.iphra_app_ui import Ui_MainWindow

# import logic and validation functions
from logic.tab2_samplesize import calculate_sample_size
from logic.validators import validate_type, validate_int, validate_float

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    # Connect the button clicked signal to your handler function
        self.ui.ss_hh_calculate.clicked.connect(self.sample_size_handle_calculate)

    def sample_size_handle_calculate(self):
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

            # Validate input types
            is_valid_sample_design, result_sample_design = validate_type(sample_design, str)
            if not is_valid_sample_design : 
                raise TypeError("Invalid input for argument sample_design provided. {result_sample_design}")
            is_valid_population_size, result_population_size = validate_type(population_size, int)
            if not validate_type(is_valid_population_size, int) == False :
                raise TypeError("Invalid input for argument population_size provided. {result_population_size}")
            is_valid_proportion, result_proportion = validate_type(proportion, float)
            if not is_valid_proportion :
                raise TypeError("Invalid input for argument proportion provided. {result_proportion}")
            is_valid_margin_of_error, result_margin_of_error = validate_type(margin_of_error, float)
            if not is_valid_margin_of_error :
                raise TypeError("Invalid input for argument margin_of_error provided. {result_margin_of_error}")
            is_valid_non_response, result_non_response = validate_type(non_response, float)
            if not is_valid_non_response :
                raise TypeError("Invalid input for argument non_response provided. {result_non_response}")
            is_valid_design_effect, result_design_effect = validate_type(design_effect, int)
            if not is_valid_design_effect :
                raise TypeError("Invalid input for argument design_effect provided. {result_design_effect}")
            
            # Validate input values
            if sample_design not in ['simple_random', 'stratified', 'cluster']:
                raise ValueError("Invalid sample design type provided. Must be 'simple_random', 'stratified', or 'clustered'.")
            
            if not (0 < proportion < 1):
                raise ValueError("Proportion must be between 0 and 1.")
            if margin_of_error <= 0:
                raise ValueError("Margin of error must be greater than 0.")
            if not (0 < margin_of_error < 1):
                raise ValueError("Margin of error must be between 0 and 1.")
            if population_size <= 0:
                raise ValueError("Population size must be greater than 0.")
            if non_response <= 0:
                raise ValueError("Non-response rate must be greater than 0.")
            if design_effect < 1:
                raise ValueError("Design effect must be at least 1 or higher.")
            if population_size < 30:
                raise ValueError("Population size must be at least 30 for sample size calculation.")
    
            # Call calculation function for sample size
            result = calculate_sample_size(
                sample_design=sample_design,
                population_size=result_population_size,
                proportion=result_proportion,
                margin_of_error=result_margin_of_error,
                non_response=result_non_response,
                design_effect=result_design_effect
            )

            # Display result
            self.ui.ss_hh_result_value.setText(str(result))

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric inputs.")

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()