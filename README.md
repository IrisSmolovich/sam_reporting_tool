
# **Reputation Stress Test Tool**

A CLI tool desgined to perform stress tests on a reputation service by sending concurrent API requests.

## 📥 Installation 

#### Clone the repo and navigate to the relevant folder
`git clone sam_reporting_tool`
`cd SAMReputationTool`

#### Install the package locally
`pip install -e`

#### Make sure you have .env file locally that with: 
`API_TOKEN=value`

## 🚀 How to trigger a test

#### Run the following command:

cli_stress_tool [options]

#### Exmaple:
`reptest --parallel-requests <number> --domains-num <number> --timeout <seconds> --log-level <level>`
`reptest --parallel-requests 1000 --domains-num 50 --timeout 30 --log-level INFO`

## 📄 Command Options

| Option                | Description                                     | Default Value                                                                       |
|------------------- ---|-------------------------------------------------|-------------------------------------------------------------------------------------|
| `--parallel-requests` | Number of concurrent API calls                  | 1                                                                                   |
| `--domains-num`       | Total number of domains to test                 | 1000                                                                                |
| `--timeout`           | Total test duration (in seconds)                | 30                                                                                  |
| `--domains-file`      | Directory to list of domains to be tested       | `domains.yaml`                                                                      |
| `--url`               | Alternative URL to send API requests to         | `https://microcks.gin.dev.securingsam.io/rest/Reputation+API/1.0.0/domain/ranking/` |
| `--log-level`         | Logging level (INFO, DEBUG, ERROR)              | `INFO`                                                                              |

