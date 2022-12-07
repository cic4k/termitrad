from elsapy.elsclient import ElsClient
from elsapy.elsdoc import AbsDoc
from elsapy.elssearch import ElsSearch
import json
from tqdm import tqdm
import csv

## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])
client.inst_token = config['insttoken']
fini = False

entries = []
for year in range(int(config["min_year"]), int(config["max_year"])+1):
    errors = []
    query = f"TITLE-ABS-KEY({config['keys']}) AND PUBYEAR = {year} AND LANGUAGE({config['lang']})"
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
        entries.append(entry)
    print(f"{len(errors)} retrieved errors for {year}: {errors}")

output_file = f"{config['index']}_{config['keys'].replace(' ','_')}_{config['min_year']}_{config['max_year']}_{config['lang']}.tsv"
with open(output_file, 'w', newline='') as tsvfile:
    writer = csv.DictWriter(tsvfile, fieldnames=["docid", "doi", "year", "title", "abstract", "keywords", "areas"],
                            dialect="unix", delimiter="\t")
    writer.writeheader()

    for entry in entries:
        writer.writerow(entry)

