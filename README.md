
# **Reputation Stress Test Tool**

A CLI tool designed to perform stress tests on a reputation service by sending concurrent API requests.

## Installation 

#### Clone the repo and navigate to the relevant folder
```bash
git clone sam_reporting_tool
cd sam_reporting_tool
```

#### Install the package locally
`pip install -e .`

#### Make sure you have .env file locally with: 
`API_TOKEN=value`

## How to trigger a test

#### Run the following command:

reptest [options]

#### Example:
```bash
reptest --parallel-requests <number> --domains-num <number> --timeout <seconds> --log-level <level>
reptest --parallel-requests 1000 --domains-num 50 --timeout 30 --log-level INFO
```

## Command Options

- **`--parallel-requests`**: Number of concurrent API calls.  
  **Default Value**: `1`

- **`--domains-num`**: Total number of domains to test.  
  **Default Value**: `1000`

- **`--timeout`**: Total test duration (in seconds).  
  **Default Value**: `30`

- **`--domains-file`**: Directory to list of domains to be tested.  
  **Default Value**: `domains.yaml`

- **`--url`**: URL to send API requests to.  
  **Default Value**: `https://microcks.gin.dev.securingsam.io/rest/Reputation+API/1.0.0/domain/ranking/`

- **`--log-level`**: Logging level (INFO, DEBUG, ERROR).  
  **Default Value**: `INFO`
