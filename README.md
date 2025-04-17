# 🗺️ Excel to Google My Maps Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

## 📋 Overview

Excel to Google My Maps Converter is a powerful tool that transforms your Excel data into interactive Google My Maps. This application streamlines the process of visualizing geographical data, making it perfect for course planning, area analysis, and obstacle mapping.

## ✨ Features

- 🔄 **Excel Integration**: Seamlessly import data from Excel spreadsheets
- 🗺️ **Google My Maps Export**: Generate shareable Google My Maps links
- 🚧 **Obstacle Mapping**: Visualize obstacles and areas on your maps
- 📊 **Course Planning**: Design and visualize routes and courses
- 🖥️ **User-Friendly GUI**: Intuitive interface for all experience levels

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/excel-to-google-my-maps.git
cd excel-to-google-my-maps
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Usage

1. Launch the application:

```bash
python main.py
```

2. Follow the GUI prompts to:
   - Select your Excel file
   - Configure map settings
   - Generate your Google My Maps link

## 📊 Data Format

Your Excel file should follow specific formatting guidelines for optimal results:

- **Areas**: Define geographical areas with coordinates
- **Courses**: Specify routes with waypoints
- **Obstacles**: List obstacles with location data

For detailed formatting instructions, see the [Data Format Guide](docs/data-format.md).

## 🛠️ Technical Details

### Project Structure

```
├── GoogleMyMaps/       # Google Maps API integration
├── excel_tables/       # Excel data processing
├── gui_interface/      # User interface components
├── main.py             # Application entry point
└── requirements.txt    # Dependencies
```

### Dependencies

- beautifulsoup4: HTML/XML parsing
- requests: HTTP requests
- openpyxl: Excel file handling
- shapely: Geometric operations
- pyjsparser: JavaScript parsing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Google My Maps](https://www.google.com/maps/about/mymaps/)
- [OpenPyXL](https://openpyxl.readthedocs.io/)
- [Shapely](https://shapely.readthedocs.io/)

## 📞 Contact

For questions or support, please open an issue or contact [your-email@example.com](mailto:your-email@example.com).

---

<p align="center">
  Made with ❤️ by Mateusz Grzech @Mateusz-7 & Adrian Burakowski @7Adrian
</p>
