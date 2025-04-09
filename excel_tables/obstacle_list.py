import openpyxl as xl
from openpyxl.utils import get_column_letter

from .excel_file import ExcelFile
from GoogleMyMaps.models import *


class ObstacleList(ExcelFile):
    file_name = "LISTA PRZESZKÓD"
    file_path = f"WZORY/{file_name}.xlsx"

    # print_area = ['$A$1:$Y$201'] # Used in previous version

    def __init__(self, google_map: Map):
        super().__init__(self.file_path)
        self.google_map = google_map # Do I need this?
        self.course_layers = [
            layer for layer in self.google_map.layers
            if layer.name.upper().startswith("TRASA") and not layer.name.upper().endswith("KIDS")
        ]
        self.kids_layer = next((layer for layer in self.google_map.layers if layer.name.upper().endswith("KIDS")), None)
        # TODO: Note that courses has to start with TRASA; KIDS ends with KIDS; first layer is the longest course

    def add_headlines(self):
        for course in self.course_layers:
            cell_column = get_column_letter(self.course_layers.index(course) * 3 + 1)
            cell_line = '1'
            cell_value = course.name
            cell_value = cell_value[6:]

            self.ws[cell_column + cell_line] = cell_value

########################################################################################################################
    def save_obstacles_info(self, formula_id: int):
        important_names = ["START", "META", "START KIDS", "META KIDS"]

        formula = self.my_map.formulas[formula_id]
        numbers_column_number = self.my_map.formulas.index(formula) * 3 + 1
        line_offset = self.my_map.number_of_big_obstacles + 1 if "KIDS" in formula.name else 0

        for obstacle_number, obstacle in enumerate(formula.obstacles):
            line_number = 3 + obstacle_number + line_offset

            self.ws[get_column_letter(numbers_column_number) + str(line_number)] = obstacle_number + 1
            self.ws[get_column_letter(numbers_column_number + 1) + str(line_number)] = \
                self.my_map.witch_area_contains_obstacle(obstacle)

            self.ws["S" + str(line_number)] = obstacle.name
            if obstacle.name in important_names:
                self.ws["S" + str(line_number)].font = xl.styles.Font(bold=True, name="Calibri")

            self.ws["T" + str(line_number)] = obstacle.number_of_volunteers if obstacle.number_of_volunteers > 0 else ""
            self.ws["U" + str(line_number)] = obstacle.number_of_judges if obstacle.number_of_judges > 0 else ""
            self.ws["X" + str(line_number)] = obstacle.comment

    def save_obstacles_numbers(self, formula: Formula):
        numbers_column_number = self.my_map.formulas.index(formula) * 3 + 1
        line_offset = self.my_map.number_of_big_obstacles + 1

        number_of_current_layer_obstacle = 0
        while number_of_current_layer_obstacle < formula.number_of_obstacles:
            is_any_found_this_iteration = False
            for obstacle_number, obstacle in enumerate(self.my_map.formulas[0].obstacles):
                if formula.obstacles[number_of_current_layer_obstacle].name == obstacle.name:
                    line_number = 3 + obstacle_number

                    self.ws[get_column_letter(numbers_column_number) + str(line_number)] = \
                        number_of_current_layer_obstacle + 1
                    self.ws[get_column_letter(numbers_column_number + 1) + str(line_number)] = \
                        self.my_map.witch_area_contains_obstacle(obstacle)
                    number_of_current_layer_obstacle += 1
                    is_any_found_this_iteration = True
                    continue

            for obstacle_number, obstacle in enumerate(self.my_map.formulas[-1].obstacles):
                if number_of_current_layer_obstacle == formula.number_of_obstacles:
                    break
                if formula.obstacles[number_of_current_layer_obstacle].name == obstacle.name:
                    line_number = 3 + obstacle_number + line_offset

                    self.ws[get_column_letter(numbers_column_number) + str(line_number)] = \
                        number_of_current_layer_obstacle + 1
                    self.ws[get_column_letter(numbers_column_number + 1) + str(line_number)] = \
                        self.my_map.witch_area_contains_obstacle(obstacle)
                    number_of_current_layer_obstacle += 1
                    is_any_found_this_iteration = True
                    continue

            if not is_any_found_this_iteration:
                number_of_current_layer_obstacle += 1

    def save_all_info(self):
        self.save_obstacles_info(0)
        self.save_obstacles_info(-1)
        for formula in self.my_map.formulas[1:-1]:
            self.save_obstacles_numbers(formula)

    def hide_unnecessary_columns_and_rows(self):
        self.ws.column_dimensions.group(get_column_letter(len(self.my_map.formulas) * 3 + 1),
                                        get_column_letter(18), hidden=True)
        self.ws.row_dimensions.group(self.my_map.number_of_all_obstacles + 4, 200, hidden=True)

    def sum_and_save_number_of_volunteers_and_judges(self):
        self.ws["T201"] = f"=SUM(T3:T200)"
        self.ws["U201"] = f"=SUM(U3:U200)"

    def save_data(self):
        self.add_headlines()
        self.save_all_info()
        self.sum_and_save_number_of_volunteers_and_judges()
        self.hide_unnecessary_columns_and_rows()

    @classmethod
    def create_and_save(cls, google_map: Map):
        obstacle_list = cls(google_map)
        obstacle_list.save_data()
        return obstacle_list