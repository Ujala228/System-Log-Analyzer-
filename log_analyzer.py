import os
import re
import csv
from datetime import datetime

# Regular expression to parse typical log formats: [YYYY-MM-DD HH:MM:SS] LEVEL: Message
LOG_PATTERN = re.compile(r'\[(?P<timestamp>.*?)\]\s+(?P<level>INFO|WARNING|ERROR):\s+(?P<message>.*)', re.IGNORECASE)

def load_log_file(file_path):
    """Reads the log file safely and returns the lines."""
    if not os.path.exists(file_path):
        print(f"\n[!] Error: The file '{file_path}' does not exist.")
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if not lines:
                print("\n[!] Warning: The file is empty.")
            return lines
    except Exception as e:
        print(f"\n[!] Error reading file: {e}")
        return []

def parse_logs(log_lines):
    """Parses raw log lines into structured dictionaries using regex."""
    parsed_data = []
    for line in log_lines:
        match = LOG_PATTERN.search(line)
        if match:
            parsed_data.append({
                'timestamp': match.group('timestamp').strip(),
                'level': match.group('level').upper(),
                'message': match.group('message').strip()
            })
    return parsed_data

def generate_counts(parsed_logs):
    """Counts the frequency of each log level."""
    counts = {'INFO': 0, 'WARNING': 0, 'ERROR': 0}
    for log in parsed_logs:
        level = log['level']
        if level in counts:
            counts[level] += 1
    return counts

def search_logs(parsed_logs, keyword):
    """Searches for a case-insensitive keyword in log messages."""
    return [log for log in parsed_logs if keyword.lower() in log['message'].lower()]

def filter_logs(parsed_logs, level):
    """Filters logs by a specific level."""
    return [log for log in parsed_logs if log['level'] == level.upper()]

def save_report(parsed_logs, counts, output_filename="log_report.txt"):
    """Generates and saves the final summary report."""
    if not parsed_logs:
        print("\n[!] No data available to generate a report.")
        return

    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write("=========================================\n")
            f.write("         SYSTEM LOG ANALYZER REPORT      \n")
            f.write(f"         Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=========================================\n\n")
            
            f.write("--- LOG SUMMARY ---\n")
            f.write(f"Total Logs Parsed: {len(parsed_logs)}\n")
            f.write(f"Total INFO:        {counts['INFO']}\n")
            f.write(f"Total WARNINGs:   {counts['WARNING']}\n")
            f.write(f"Total ERRORs:     {counts['ERROR']}\n\n")
            
            f.write("--- DETAILED LOGS ---\n")
            for log in parsed_logs:
                f.write(f"[{log['timestamp']}] {log['level']}: {log['message']}\n")
                
        print(f"\n[+] Report successfully saved to '{output_filename}'")
    except Exception as e:
        print(f"\n[!] Failed to save report: {e}")

def main():
    raw_logs = []
    parsed_logs = []
    
    while True:
        print("\n=== Log Analyzer & Report Generator ===")
        print("1. Load Log File")
        print("2. Analyze Logs (Show Counts)")
        print("3. Search Logs by Keyword")
        print("4. Filter Logs by Level")
        print("5. Generate & Save Report")
        print("6. Exit")
        
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == '1':
            path = input("Enter path to log file (e.g., sample.log): ").strip()
            raw_logs = load_log_file(path)
            if raw_logs:
                parsed_logs = parse_logs(raw_logs)
                print(f"[+] Loaded {len(raw_logs)} lines. Successfully parsed {len(parsed_logs)} logs.")
                
        elif choice == '2':
            if not parsed_logs:
                print("[!] Please load and parse a valid log file first.")
                continue
            counts = generate_counts(parsed_logs)
            print("\n--- Analysis Result ---")
            print(f"Total Logs Processed: {len(parsed_logs)}")
            for lvl, cnt in counts.items():
                print(f"{lvl}: {cnt}")
                
        elif choice == '3':
            if not parsed_logs:
                print("[!] Please load a log file first.")
                continue
            kw = input("Enter keyword to search: ").strip()
            results = search_logs(parsed_logs, kw)
            print(f"\n[+] Found {len(results)} matching entries:")
            for r in results[:10]:  # Limit display to top 10
                print(f"[{r['timestamp']}] {r['level']}: {r['message']}")
                
        elif choice == '4':
            if not parsed_logs:
                print("[!] Please load a log file first.")
                continue
            lvl = input("Enter level to filter (INFO, WARNING, ERROR): ").strip().upper()
            if lvl in ['INFO', 'WARNING', 'ERROR']:
                results = filter_logs(parsed_logs, lvl)
                print(f"\n[+] Found {len(results)} logs with level {lvl}:")
                for r in results[:10]:
                    print(f"[{r['timestamp']}] {r['message']}")
            else:
                print("[!] Invalid log level.")
                
        elif choice == '5':
            if not parsed_logs:
                print("[!] No data to generate a report. Load a file first.")
                continue
            counts = generate_counts(parsed_logs)
            out_file = input("Enter output report filename (default: log_report.txt): ").strip()
            if odds := out_file:
                save_report(parsed_logs, counts, odds)
            else:
                save_report(parsed_logs, counts)
                
        elif choice == '6':
            print("\nExiting program. Goodbye!")
            break
        else:
            print("[!] Invalid choice. Please select between 1 and 6.")

if __name__ == "__main__":
    main() 