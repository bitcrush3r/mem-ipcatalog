import sys
import json

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 filter_ips_by_occurrence.py memory_dump.img_ips.json 3")
        sys.exit(1)

    json_file = sys.argv[1]
    try:
        max_occurrences = int(sys.argv[2])
    except ValueError:
        print("Second argument must be INT (occurrences number).")
        sys.exit(1)

    # JSON reading
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        sys.exit(1)

    # Filter and display
    filtered_ips = {ip: occurrences for ip, occurrences in data.items() if len(occurrences) == max_occurrences}

    if not filtered_ips:
        print(f"No IP found with occurences = {max_occurrences}.")
    else:
        print(f"IPs with {max_occurrences} occurrences :\n")
        for ip, occurrences in filtered_ips.items():
            print(f"{ip} ({len(occurrences)} occurrence(s))")

    # Save in a file
    output_file = json_file.replace(".json", f"_filtered_max{max_occurrences}.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_ips, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved in {output_file}")

if __name__ == '__main__':
    main()
