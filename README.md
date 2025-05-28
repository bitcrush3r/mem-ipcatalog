# mem-ipcatalog
An offline IP extractor and catalog tool for forensic memory analysis.

# Architecture

Two pythons scripts to extract and catalog IP addresses from memory dump :
- extractjson-memory.py : Everything starts with a strings command!
This script outputs a JSON file containing all public IP addresses found in the memory dump.
Each key is an IP address, and its value is a list of all occurrences found. Each occurrence includes the line number as the key and the corresponding text as the value.
- filter\_ips\_by\_occurrences.py : This script filters the previously extracted IPs based on how many times they appear.
For example, if you want to extract all IP addresses that appear only once, this tool can do it.

# Get Started

## Install requirements :
```
pip install -r requirements.txt
```
## Extract IP addresses
```
python3 extract_ips_json.py memory_dump.img
```
This command will generate a global JSON file in the result folder.

## Filter IP adresses by occurences
```
python3 filter_ips_by_occurrence.py memory_dump.img_ips.json 3
```
In this example, only IPs that occur 3 times will be included in the output.
You can replace 3 with any integer value.


# Todo 
- Add an option to filter reverse (private) IP addresses
- Create a high-level script with a simple interface to improve usability
- Optimize performance: currently, analyzing an 8GB memory dump requires ~32GB of RAM (there are better ways to improve it)
