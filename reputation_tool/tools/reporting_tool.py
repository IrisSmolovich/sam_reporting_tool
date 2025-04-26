
import os
import zipfile
import time
import csv
from pathlib import Path


class ReportingClass:
    """
    Reporting tool to handle print-outs in terminal, storing information in CSV and compression to ZIP
    """
    def __init__(self, results, execution):
        self.raw_results = results
        self.total_requests = results["total_requests"]
        self.failed_requests = results["failed_requests"]
        self.response_times = results["max_response_time"]
        self.execution = execution

    def print_results(self) -> None:
        """
        reports results to terminal
        """
        print("Test has finished!")
        print(f"Unique total tested domains: {len(self.execution)}")
        print(f"Total requests: {self.raw_results["total_requests"]}")
        print(f"Successful requests: {self.raw_results["total_requests"]}-{self.raw_results["failed_requests"]}")
        print(f"Failed requests: {self.raw_results["failed_requests"]}")
        print(f"Failed percentage: {self.raw_results["error_rate"]:.2f}%")
        print(f"Average time: {self.raw_results["avg"]:.4f}s")
        print(f"Max time: {self.raw_results["max_response_time"]:.4f}s")
        print(f"P90 time: {self.raw_results["p90"]:.4f}s")

    def write_to_csv(self, time_stamp):
        """
        extracts results to csv file
        """
        directory = Path(__file__).resolve().parent.parent / "logs"
        filename = directory / f"stress_results_{time_stamp}.csv"
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Total Domains", "Total Requests", "Successful", "Failed", "ErrorRate", "Average", "Max",
                             "P90"])

            writer.writerow([
                len(self.execution),
                self.total_requests,
                self.raw_results["total_requests"]-self.raw_results["failed_requests"],
                self.failed_requests,
                self.raw_results["error_rate"],
                self.raw_results["avg"],
                self.raw_results["max_response_time"],
                self.raw_results["p90"]
            ])

    def zip_logs_and_results(self, time_stamp, max_wait=10):
        """
        Compress existing log file and csv file into one zip.
        After zipping, delete the original files to prevent duplication.
        """
        directory = Path(__file__).resolve().parent.parent / "logs"
        log_dir = Path(directory)

        log_file = log_dir / f"stress_test_logs_{time_stamp}.log"
        csv_file = log_dir / f"stress_results_{time_stamp}.csv"

        zip_file = log_dir / f"stress_test_{time_stamp}.zip"

        start_time = time.time()
        while True:
            if os.path.exists(log_file) and os.path.exists(csv_file):
                break

            if time.time() - start_time > max_wait:
                print(f"Max wait time of {max_wait} seconds exceeded. Exiting.")
                break
            time.sleep(1)

        try:
            with zipfile.ZipFile(zip_file, "w", compression=zipfile.ZIP_DEFLATED) as zip:
                zip.write(log_file, arcname=log_file.name)
                zip.write(csv_file, arcname=csv_file.name)

            log_file.unlink()
            csv_file.unlink()

            print(f"Saved zip archive: {zip_file}")

        except Exception as e:
            print(f"Error while zipping the files: {e}")
