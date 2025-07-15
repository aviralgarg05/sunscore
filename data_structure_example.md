# Data Structure Requirements

This project requires specific data files that are too large for Git repositories.

## Required Files (not included in repository)

### 1. ZIP Codes Shapefile
- **File**: `tl_2023_us_zcta520.zip` (503MB)
- **Source**: [US Census Bureau](https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html)
- **Description**: ZCTA (ZIP Code Tabulation Areas) boundaries
- **Location**: Place in project root directory

### 2. ZIP Codes CSV Data
- **File**: `uszips.csv`
- **Required columns**: `zip`, `lat`, `lng`, `state_id`, `city`
- **Source**: Various public datasets or commercial providers

## Sample Data Format

### uszips.csv structure:
```csv
zip,lat,lng,city,state_id,state_name,county_fips,county_name,county_weights,county_names_all,county_fips_all,imprecise,military,timezone
00501,40.8154,-73.0451,Holtsville,NY,New York,36103,Suffolk,36103:1.0,Suffolk,36103,False,False,America/New_York
```

## Setup Instructions

1. Download required data files
2. Place them in the project root directory
3. Ensure files match the expected structure
4. Run the application

## File Size Limitations

These files are excluded from Git due to:
- GitHub's 100MB file size limit
- Large repository size impact
- Licensing considerations for commercial datasets
