import signal
import sys
import argparse
import dns.resolver


# Colors
class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def def_handler(sig, frame):
    print(f"{bcolors.FAIL}\n\n[!] Quiting...\n{bcolors.ENDC}")
    sys.exit(1)


signal.signal(signal.SIGINT, def_handler)


# Function to perform DNS queries
def lookup_records(domain):
    records = {"A": [], "MX": [], "NS": []}

    try:
        for record_type in records.keys():
            response = dns.resolver.resolve(domain, record_type)
            for r in response:
                records[record_type].append(str(r))
    except dns.resolver.NoAnswer:
        print(f"{bcolors.FAIL}[!] No answer for {domain}.{bcolors.ENDC}")
    except dns.resolver.NXDOMAIN:
        print(f"{bcolors.FAIL}[!] The domain {domain} does not exist.{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}[!] Error querying {domain}: {e}{bcolors.ENDC}")

    return records


# Command-line argument parser
def main():
    parser = argparse.ArgumentParser(
        description="DNS Lookup Script for A, MX, and NS records."
    )
    parser.add_argument(
        "-d",
        "--domains",
        nargs="+",
        required=True,
        help="Domains to query, separated by space.",
    )
    args = parser.parse_args()

    for domain in args.domains:
        print(f"\nQuerying {domain}...")
        results = lookup_records(domain)
        for record_type, values in results.items():
            print(
                f"{bcolors.OKGREEN} [*] {record_type} records: {', '.join(values) if values else 'Not found'}{bcolors.ENDC}"
            )


if __name__ == "__main__":
    main()
