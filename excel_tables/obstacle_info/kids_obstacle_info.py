from excel_tables.obstacle_info.obstacle_info import ObstacleInfo


class KidsObstacleInfo(ObstacleInfo):
    """
    Class for handling obstacle information specifically for kids in Excel files.

    This class is responsible for extracting and managing information about obstacles
    for the kids' course from a specific worksheet in the Excel file.

    Attributes:
        WORKSHEET_NUMBER (int): The worksheet number to be used in the Excel file (0-based).
        COLUMN_NAME (int): The column number for obstacle names.
        COLUMN_WORKER (int): The column number for worker names.
        ROW_FIRST_OBSTACLE (int): The row number where the first obstacle is located.
    """
    WORKSHEET_NUMBER = 1
    COLUMN_NAME = 3
    COLUMN_WORKER = 7
    ROW_FIRST_OBSTACLE = 3

    # inżynier -> technik
    # siatka gagaDka
    # brak siatki z workiem
    # brak zasieki
    # ślizg pusty

    # klatka weryfikator?
    # mini lodowa / lodowa?
