# mem-ipcatalog
An offline IP extractor and catalog tool for forensic memory analysis.

# Architecture

Two pythons scripts to extract and catalog IP addresses from memory dump :
- extractjson-memory.py : All start with a "strings" command ! Output a jsonfile with all publics ip addresses referenced. Each key is an IP and its value contain a tab with all occurrences found in the dump with in key the line number and in value the text. 
- filter\_ips\_by\_occurrences.py : Output a jsonfile which contains only the choosen number of IP occurrences. If you want for example all IP address referenced just one time, it can do it. 

# Get Started

## Install requirements :
```
pip install -r requirements.txt
```
## Extract IP addresses
```
python3 extract_ips_json.py memory_dump.img
```
This output in result folder the global json file.

## Filter IP adresses by occurences
```
python3 filter_ips_by_occurrence.py memory_dump.img_ips.json 3
```
Here, we used 3 but it can be another INT number.

# Todo 
- Add option to filter reverse IP adresses
- Add high level script with interface to facilitate program usage.
- Improve performance: actually a lot of memory (~32GB) is needed to analyse 8GB of memory dump
