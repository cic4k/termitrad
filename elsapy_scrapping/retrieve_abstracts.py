from elsapy.elsclient import ElsClient
from elsapy.elsdoc import AbsDoc
from elsapy.elssearch import ElsSearch
from datetime import datetime
import json
import utils
from tqdm import tqdm
import csv

## Load configuration
con_file = open("config_keys.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])
client.inst_token = config['insttoken']

freqs, total_words_num = utils.frequency_sorted(config['keys'])
i = _ = 0
min_freq = 10

keys_to_search = [_[0] for _ in freqs if _[1] >= min_freq]
print(f"Searching for: {keys_to_search}, Min freq: {min_freq}")
formatted_keys_to_search = " OR ".join([f"TITLE-ABS-KEY({_})" for _ in keys_to_search])

now = datetime.now()
time = f"{now.day}-{now.month}-{now.year}_{now.hour}:{now.minute}:{now.second}"
output_file_base = f"{config['index']}_{time}_{config['min_year']}_{config['max_year']}_{config['lang']}"


output_file = f"{output_file_base}.keys"
with open(output_file, "w") as file:
    file.write(f"{config['keys']}\n")
    file.write(f"{keys_to_search}")

output_file = f"{output_file_base}.tsv"
with open(output_file, 'w', newline='') as tsvfile:
    writer = csv.DictWriter(tsvfile, fieldnames=["docid", "doi", "year", "title", "abstract", "keywords", "areas"],
                            dialect="unix", delimiter="\t")
    writer.writeheader()


for year in range(int(config["min_year"]), int(config["max_year"])+1):
    errors = []
    entries = []
    query = f"({formatted_keys_to_search}) AND PUBYEAR > {year-1} AND PUBYEAR < {year+1} AND LANGUAGE({config['lang']}) AND (SUBJAREA(AGRI) OR SUBJAREA(ENVI))"
    myDocSrch = ElsSearch(query, config['index'])
    myDocSrch.execute(client, get_all=True)
    print(f"I've found {len(myDocSrch.results)} articles for {year}.")
    for i, res in enumerate(tqdm(myDocSrch.results)):
        if "error" in res.keys():
            continue

        entry = {}
        docid = res['dc:identifier'].split(":")[-1]
        scp_doc = AbsDoc(scp_id=docid)

        doi = title = abstract = ""
        keywords = []
        areas = []

        try:
            if scp_doc.read(client):
                title = scp_doc.data['coredata']['dc:title']
                keywords = [_["$"] for _ in scp_doc.data.get("authkeywords", {}).get("author-keyword", [])]
                areas = [_["$"] for _ in scp_doc.data.get("subject-areas", {}).get("subject-area", [])]
                abstract = scp_doc.data['coredata']['dc:description']
                doi = scp_doc.data['coredata']['prism:doi']
        except:
            errors.append(docid)
        finally:
            entry = {
                "docid": docid,
                "doi": doi,
                "year": year,
                "title": title,
                "abstract": abstract,
                "keywords": ";".join(keywords),
                "areas": ";".join(areas)
            }
        if len(keywords) != 0 and len(abstract) != 0:
            entries.append(entry)
    print(f"{len(errors)} retrieved errors for {year}: {errors}")
    print(f"Writing {len(entries)} entries.")

    with open(output_file, 'a', newline='') as tsvfile:
        writer = csv.DictWriter(tsvfile, fieldnames=["docid", "doi", "year", "title", "abstract", "keywords", "areas"],
                                dialect="unix", delimiter="\t")
        for entry in entries:
            writer.writerow(entry)



