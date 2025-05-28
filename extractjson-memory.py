import sys
import re
import json
import subprocess
import ipaddress

os.makedirs("results", exist_ok=True)

def is_probable_oid(ip):
    # Some common OID
    oid_prefixes = [
        "1.3.6",    # SNMP/MIB
        "2.5.4",    # X.500
        "2.5.29",   # X.509 extensions
    ]
    return any(ip.startswith(prefix + ".") for prefix in oid_prefixes)

def is_valid_ip(ip):
    try:
        if is_probable_oid(ip):
            print(f"{ip} is a probable oid")
            return False  # probable OID, not used
        ip = ip.strip()
        ip_obj = ipaddress.IPv4Address(ip)

        if (
            ip_obj.is_private or
            ip_obj.is_loopback or
            ip_obj.is_link_local or
            ip_obj.is_multicast or
            ip_obj.is_reserved or
            ip_obj.is_unspecified
        ):
            print(f"{ip} private     -> {ip_obj.is_private}")
            print(f"{ip} loopaback   -> {ip_obj.is_loopback}")
            print(f"{ip} linklocal   -> {ip_obj.is_link_local}")
            print(f"{ip} multicast   -> {ip_obj.is_multicast}")
            print(f"{ip} reserved    -> {ip_obj.is_reserved}")
            print(f"{ip} unspecified -> {ip_obj.is_unspecified}")
            return False
        return True

    except ValueError:
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 extract_ips_json.py memory_dump.img")
        sys.exit(1)

    filename = sys.argv[1]

    # Start strings with -td (offset decimal + string)
    cmd = ['strings', '-td', filename]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"Error when exec strings: {proc.stderr}")
        sys.exit(1)

    lines = proc.stdout.splitlines()

    # Get tuples (offset, contenu)
    lines_data = []

    # Parse each line : "<offset> <string>"
    for line in lines:
        if not line.strip():
            continue
        # Separate offset and other parts with space
        parts = line.split(' ', 1)
        if len(parts) < 2:
            continue
        offset_str, content = parts
        if not offset_str.isdigit():
            continue
        offset = int(offset_str)
        lines_data.append((offset, content))

    # map offset -> index in lines_data quick access
    offset_to_index = {offset: idx for idx, (offset, _) in enumerate(lines_data)}

    # Naive Pattern IP for extraction
    ip_pattern = re.compile(r'(\d{1,3}\.){3}\d{1,3}')

    # Dict result : index=IP, value = list occurrences
    result = {}

    for idx, (offset, content) in enumerate(lines_data):
      # Extract all IPs in the line
      ips = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', content)

      for ip in ips:
        if not is_valid_ip(ip):
            continue  # or print(ip) for debug

        # Prepare occurrence : lines [idx - 2, idx + 2]
        occurrence = {}

        for i in range(idx - 2, idx + 3):  # from idx-2 to idx+2 included
            if 0 <= i < len(lines_data):
                line_offset, line_content = lines_data[i]
                occurrence[line_offset] = line_content
            else:
                occurrence[-1] = None  # out of bound cases

        # Add occurence to the ip list
        if ip not in result:
            result[ip] = []
        result[ip].append(occurrence)

    # Write JSON
    output_file = "results/"+filename + "_ips.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Extraction terminated. Result in {output_file}")

if __name__ == '__main__':
    main()

