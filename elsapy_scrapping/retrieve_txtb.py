#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 14:19:00 2022

@author: odeviron
"""
"""An example program that uses the elsapy module"""
# 328+412+371+430+409+447+508+571+578+567+496+585+697+757+754+793+848+786+953+1051+1163+1448+1433+1616+1629+1713+1849+2145+2147+2388+2443+2400+2700+3368+3582+3968+4299
from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json
from tqdm import tqdm
from pybliometrics.scopus import AbstractRetrieval
#ab = AbstractRetrieval("10.1016/j.softx.2019.100263")
## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])
client.inst_token = config['insttoken']
fini=False
key=config["query"]
for yy in tqdm(range(int(config["min_year"]), int(config["max_year"]))):
    query='TITLE-ABS-KEY('+key+') AND PUBYEAR > '+str(yy-1)+' AND PUBYEAR < '+str(yy+1) 
    myDocSrch = ElsSearch(query,'scopus')
    
    myDocSrch.execute(client,get_all = True)
    
    print (yy,"myDocSrch has", len(myDocSrch.results), "results.")
    #%%
    linesize=60
    output=open('scopus_output2_'+key.replace(' ','_')+str(yy),'w')
#    outpub=open('scopus_list_'+key.replace(', ',',').replace(' ','_')+str(yy),'w')
    for i, res in enumerate(myDocSrch.results):
        if 'error' not in res.keys():
            try:
                a=0
                docid=res['dc:identifier']
                docid= docid[docid.index(':')+1:]
                a='id'
                scp_doc = AbsDoc(scp_id = docid)
                a='Abs'
                if scp_doc.read(client):
                    if 'subject-areas' in scp_doc.data.keys():
                        sub=scp_doc.data['subject-areas']['subject-area']
                    else:
                        sub='None'
                    su='**** '
                    for s in sub:
                        su+=' *'+s['$'].replace(' ','_')
                    a='Subj'
                    abst=scp_doc.data['coredata']['dc:description'].replace('Elsevier','')
                    a='abs'
                    fini=True
            except:
                next
                print('!!!!!!!!! missed,'+a)

                fini=False
            if fini:
                    try:
                        output.write('### '+res['dc:title']+', '+res['prism:doi']+'\n')
                    except:
                        try:
                            output.write('### '+res['dc:title']+'\n')
                        except:
                            output.write('### '+res['prism:doi']+'\n')
                            
                    output.write(su+'\n')
                    abstli=abst.split()
                    # The list of words from the abstract is complete, not truncated
                    len_abs=[len(abst) for abst in abstli]
                    
                    for abst_i in abstli:
                        oo = ""
                        pp = abst_i
                        ppe = pp.encode("ascii", "ignore")
                        if len(ppe.decode())>0:
                            oo+=ppe.decode()+' '
                        output.write(oo)
                    output.write('\n')
 
    output.close()
