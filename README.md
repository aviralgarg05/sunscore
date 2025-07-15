# SunScore - Solar Irradiance Data Collector

A Python application that collects solar irradiance data from the NREL NSRDB API for US ZIP codes.

## Features

- Fetches solar irradiance data (GHI, DNI, DHI) for US ZIP codes
- Processes and stores data in CSV format
- Handles API rate limiting and retries
- Docker support for containerized deployment
- Comprehensive error logging

## Prerequisites

- Python 3.10+
- NREL NSRDB API key (free registration at [developer.nrel.gov](https://developer.nrel.gov))
- US ZIP codes CSV file with columns: zip, lat, lng, state_id, city

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sunscore.git
cd sunscore
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export NSRDB_API_KEY="your_api_key_here"
export USER_EMAIL="your_email@example.com"
export YEAR="2024"
```

4. Place your ZIP codes CSV file as `uszips.csv` in the project root.

## Usage

### Local Development
```bash
python main.py
```

### Docker
```bash
# Build the image
docker build -t sunscore .

# Run with environment variables
docker run -e NSRDB_API_KEY="your_key" -e USER_EMAIL="your_email" sunscore
```

## Configuration

Environment variables:
- `NSRDB_API_KEY`: Your NREL NSRDB API key
- `USER_EMAIL`: Your email address for API requests
- `YEAR`: Data year to fetch (default: 2017)
- `ATTRIBUTES`: Solar attributes to fetch (default: ghi,dni,dhi)

## Output

- `sunscore_data.csv`: Main output file with solar data
- `sunscore_failures.log`: Log of failed ZIP code requests

## API Rate Limits

The application respects NREL API rate limits with 1-second delays between requests and automatic retry logic.

## License

MIT License
