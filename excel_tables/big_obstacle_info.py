from excel_tables.obstacle_info import ObstacleInfo


class BigObstacleInfo(ObstacleInfo):
    """
    Class for handling big obstacle information in Excel files.

    Attributes:
        WORKSHEET_NUMBER (int): The worksheet number to be used in the Excel file.
        COLUMN_NAME (int): The column number for obstacle names.
        COLUMN_WORKER (int): The column number for worker names.
        ROW_FIRST_OBSTACLE (int): The row number where the first obstacle is located.
    """
    WORKSHEET_NUMBER = 0
    COLUMN_NAME = 8
    COLUMN_WORKER = 13
    ROW_FIRST_OBSTACLE = 3

    # KLATKI, combo
    # kratownica góra dół / kratownica - krzyżówka tras
    # ściana skośna / ukośna a skośna x2
    # mega zasieki
    # chomikator puste
    # Literówka we wspinaniu

    # przejście A?
    # subaru?
