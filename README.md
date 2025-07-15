# SunScore - Solar Irradiance Data Collector

A Python application that collects solar irradiance data from the NREL NSRDB API for US ZIP codes and stores it in MongoDB.

## Features

- ✅ Fetches solar irradiance data (GHI, DNI, DHI) for US ZIP codes
- ✅ MongoDB integration for data storage
- ✅ Grid-based sampling within ZIP code boundaries
- ✅ API rate limiting and error handling
- ✅ Docker support for easy deployment
- ✅ Environment-based configuration

## Prerequisites

- Python 3.10+
- MongoDB (local or cloud)
- NREL NSRDB API key (free registration at [developer.nrel.gov](https://developer.nrel.gov))
- US ZIP codes CSV file

## Quick Start

1. **Clone and setup:**
```bash
git clone https://github.com/aviralgarg05/sunscore.git
cd sunscore
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your API key and database settings
```

3. **Setup data:**
```bash
python setup_data.py
```

4. **Run the application:**
```bash
python main.py
```

## Docker Deployment

```bash
# Start with Docker Compose
docker-compose up -d

# Or build and run manually
docker build -t sunscore .
docker run --env-file .env sunscore
```

## Configuration

Required environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `NSRDB_API_KEY` | NREL NSRDB API key | Required |
| `NSRDB_EMAIL` | Email for API requests | Required |
| `NSRDB_YEAR` | Data year to fetch | 2024 |
| `MONGO_URI` | MongoDB connection string | mongodb://localhost:27017 |
| `DATABASE` | Database name | SunscoreData |
| `COLLECTION` | Collection name | SolarReadings |

## Data Sources

- **ZIP Codes**: Download from [SimpleMaps](https://simplemaps.com/data/us-zips)
- **Solar Data**: NREL NSRDB via API

## API Rate Limits

- Respects NREL API rate limits (1000 requests/hour)
- Implements automatic retry logic
- 1-second delay between requests

## Database Schema

Solar readings are stored with this structure:
```json
{
  "latitude": 40.7589,
  "longitude": -73.9851,
  "ghi": 150.5,
  "dni": 200.3,
  "dhi": 75.2,
  "year": "2024",
  "zip_code": "10001",
  "timestamp": "2024-01-01T12:00:00Z",
  "location": {
    "type": "Point",
    "coordinates": [-73.9851, 40.7589]
  }
}
```

## Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run setup for sample data
python setup_data.py

# Run the application
python main.py
```

## License

MIT License
