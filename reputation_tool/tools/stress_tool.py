import random
import statistics
from pathlib import Path
from reputation_tool.utils import logger
import requests
import threading
import time


class RankingClass:
    """
    class that handled ranking of domains per given parameters
    """

    def __init__(self, api_token, domains, url, time_stamp, level="INFO"):
        log_dir = Path(__file__).resolve().parent.parent / "logs"
        self.logger = logger.logger_init(log_dir=log_dir, level=level, time_stamp=time_stamp)
        self.api_token = api_token
        self.domains = domains
        self.url = url
        self.domain = None

        self.total_requests = 0
        self.failed_requests = 0
        self.response_times = []

        self.lock = threading.Lock()
        self.stop_event = threading.Event()

    def _build_url(self, domain: str) -> str:
        self.logger.debug("Creating a full url")
        return f"{self.url}{domain}"

    def _get_site_ranking(self, url: str, domain: str) -> str:
        headers = {
            "Authorization": f"Token {self.api_token}",
            "Accept": "application/json"
        }
        self.logger.debug(f"Verify site ranking for domain {domain}")
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                self.logger.error(f"Bad response code is {response.status_code}")
                raise AssertionError(f"Bad status {response.status_code} for {domain}")
            data = response.json()
            if data.get("address") == "null":
                self.logger.error(f"Invalid address 'null' returned for {domain}")
                raise AssertionError(f"Invalid address 'null' returned for {domain}")
            return data
        except requests.RequestException as e:
            self.logger.error(f"Request exception for {domain}: {e}")

    def run(self, threads=10, timeout=30, max_domains=5000) -> list:
        """
        :param threads: how many threads to run in parallel
        :param timeout: maximum timeout for the execution
        :param max_domains: how many maximum domains to check
        :return: list of tested domains
        """
        tested_domains = []
        start_time = time.time()
        end_time = start_time + timeout

        def _thread_task():
            while not self.stop_event.is_set():
                current_time = time.time()
                if current_time > end_time:
                    self.logger.info("Timeout has reached. Tests will stop")
                    break
                with self.lock:
                    if len(tested_domains) < max_domains:
                        domain = random.choice(self.domains)
                        if domain not in tested_domains:
                            self.logger.info(f"Adding a new domain to tested list {domain}")
                            tested_domains.append(domain)
                    else:
                        if not tested_domains:
                            continue
                        domain = random.choice(tested_domains)

                    self.domain = domain

                url = self._build_url(self.domain)
                start = time.time()
                try:
                    self._get_site_ranking(url, self.domain)
                except AssertionError:
                    with self.lock:
                        self.failed_requests += 1
                else:
                    elapsed = time.time() - start
                    with self.lock:
                        self.response_times.append(elapsed)
                finally:
                    with self.lock:
                        self.total_requests += 1

        threads_list = []
        try:
            for _ in range(threads):
                t = threading.Thread(target=_thread_task)
                t.start()
                threads_list.append(t)

            for t in threads_list:
                t.join()
        except KeyboardInterrupt:
            print("KeyboardInterrupt detected! Handling a graceful shutdown")
            self.logger.warning("KeyboardInterrupt detected! Handling a graceful shutdown")
            self.stop_event.set()
            for t in threads_list:
                t.join()
        finally:
            self.stop_event.set()
            self.logger.info("Execution was completed")
            tested_domains = list(set(tested_domains))
            self.logger.debug(f"Domains that were tested are: {tested_domains}")
            return tested_domains

    def get_test_results(self) -> dict:
        """
        Returns a dictionary that contains the test results to be used later
        """
        self.logger.info("Analyzing test results")
        error_rate = (self.failed_requests / self.total_requests * 100) if self.total_requests else 0
        avg = statistics.mean(self.response_times) if self.response_times else 0
        max_time = max(self.response_times) if self.response_times else 0
        p90 = statistics.quantiles(self.response_times, n=10)[8] if len(self.response_times) >= 10 else 0

        results = {
            "domain": self.domain,
            "total_requests": self.total_requests,
            "failed_requests": self.failed_requests,
            "error_rate": error_rate,
            "avg": avg,
            "max_response_time": max_time,
            "p90": p90
        }
        return results

    def close(self):
        """use close_logger() to verify logging has finished after the test"""
        self.logger.remove()
