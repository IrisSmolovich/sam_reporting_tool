
# **Reputation Stress Test Tool**

A CLI tool desgined to perform stress tests on a reputation service by sending concurrent API requests.

## Installation 

#### Clone the repo and navigate to the relevant folder
`git clone sam_reporting_tool`
`cd SAMReputationTool`

#### Install the package locally
`pip install -e`

## How to trigger a test

#### Run the following command:

reptest --parallel-requests <number> --domains-num <number> --timeout <seconds> --log-level <level>

#### exmaple:
reptest --parallel-requests 1000 --domains-num 50 --timeout 30 --log-level INFO

## 📄 Command Options

Option	Description
--parallel-requests	Number of concurrent API calls
--domains-num	Total number of domains to test
--timeout	Total test duration (in seconds)
--domains-file  Directory to list of domains to be tested
--url   Alternative URL to send API requests to
--log-level	Logging level (INFO, DEBUG, ERROR)

