
import argparse
from datetime import datetime
from reputation_tool.utils.config_loader import load_domains_from_file, get_api_token
from reputation_tool.tools.reporting_tool import ReportingClass
from reputation_tool.tools.stress_tool import RankingClass


def main():
    """
    handler for CLI stress tool. it will receive needed arguments, validate them and trigger the stress test

    """
    parser = argparse.ArgumentParser(description="Reputation Tool")
    parser.add_argument("--parallel-requests", type=int, default=1, help="Number of threads to run in parallel")
    parser.add_argument("--domains-num", type=int, default=1000, help="Number of domains to use (max 5000)")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout in seconds")
    parser.add_argument("--domains-file", type=str, help="File with list of domains")
    parser.add_argument("--url", type=str, default="https://microcks.gin.dev.securingsam.io/rest/Reputation+API/1.0.0"
                                                   "/domain/ranking/")
    parser.add_argument("--log-level", type=str, default="INFO", help="Choose desired logging level")
    args = parser.parse_args()

    execution = []
    api_token = get_api_token()

    if args.domains_file is None:
        domains = load_domains_from_file()
    else:
        domains = load_domains_from_file(args.domains_file)

    if len(domains) > 5000:
        raise AssertionError("No more then 5000 domains can be tested at each execution")

    session_timestamp = datetime.now().strftime("%d_%m_%Y_%H.%M.%S")

    domains_ranking = RankingClass(api_token, domains, args.url, time_stamp=session_timestamp, level=args.log_level)
    try:
        execution = domains_ranking.run(args.parallel_requests, args.timeout, args.domains_num)
    finally:
        raw_results = domains_ranking.get_test_results()
        domains_ranking.close()

    reporter = ReportingClass(raw_results, execution)
    reporter.print_results()
    reporter.write_to_csv(time_stamp=session_timestamp)

    reporter.zip_logs_and_results(time_stamp=session_timestamp)


if __name__ == "__main__":
    main()
