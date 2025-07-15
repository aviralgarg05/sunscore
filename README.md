# SunScore - Solar Irradiance Data Collector

A comprehensive Python application for collecting and processing solar irradiance data from the NREL NSRDB API for US ZIP codes.

## Features

- **Multi-source Data Collection**: Fetches solar irradiance data (GHI, DNI, DHI) using ZIP codes or geographic grids
- **Intelligent Grid Sampling**: Generates random points within ZIP code polygons for comprehensive coverage
- **Data Processing Pipeline**: Converts raw solar data to structured CSV format with timestamps
- **Error Handling**: Robust retry logic and unsupported region detection
- **Flexible Configuration**: Environment-based configuration for different deployment scenarios

## Project Structure

```
sunscore/
├── main.py                              # Main application entry point
├── config.py                            # Configuration management
├── zip_loader.py                        # ZIP code data loading utilities
├── zip_grid.py                          # Geographic grid generation
├── nsrdb.py                             # NREL NSRDB API client
├── solar_db.py                          # Solar data storage utilities
├── convert_raw_to_structured_csv.py     # Data conversion utilities
├── requirements.txt                     # Python dependencies
└── README.md                            # Project documentation
```

## Prerequisites

- Python 3.8+
- NREL NSRDB API key (free registration at [developer.nrel.gov](https://developer.nrel.gov))
- ZIP codes CSV file or shapefile data for geographic boundaries

## Installation

1. Clone the repository:
```bash
git clone https://github.com/aviralgarg05/sunscore.git
cd sunscore
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment configuration:
```bash
cp .env.example .env
# Edit .env with your API credentials
```

## Configuration

Create a `.env` file with the following variables:

```env
NSRDB_API_KEY=your_nrel_api_key_here
NSRDB_EMAIL=your_email@example.com
NSRDB_YEAR=2024
ZIP_DATA_FILE=zip_codes.csv
```

## Usage

### Basic Data Collection
```bash
python main.py
```

### Data Format Conversion
```bash
python convert_raw_to_structured_csv.py
```

## API Rate Limits

The application respects NREL API rate limits with:
- 1-second delays between requests
- Automatic retry logic (3 attempts)
- Graceful handling of 403 Forbidden responses

## Output Files

- `solar_data.csv`: Main structured output with timestamp data
- `raw_solar_data.csv`: Raw API responses
- `solar_data_structured.csv`: Processed data with timestamps

## Supported Regions

The application automatically excludes unsupported US territories:
- Puerto Rico (PR)
- US Virgin Islands (VI)
- Guam (GU)
- American Samoa (AS)
- Northern Mariana Islands (MP)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Create an issue on GitHub
- Check NREL NSRDB documentation for API-related questions
