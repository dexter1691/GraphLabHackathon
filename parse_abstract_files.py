__author__ = 'dexter'

import graphlab as gl
import os
import config as cfg
import re
import csv

csv_file = open('/home/dexter/workspace/GraphLabHackathon/abstract_data.csv', 'wb')
csv_writer = csv.writer(csv_file, delimiter='\t')

header_list = ['ID', 'Title','Authors','Year','Abstract', 'Email','Pages','Venue',
                'EmailName']
csv_writer.writerow(header_list)


def parse_content(content, year):
    id =  re.findall('Paper: h?H?ep-th/(.*)', content)

    title = re.findall('Title: (.*)', content)
    title[0] = re.sub('\$(.*)\$','', title[0])

    authors = re.findall('Authors?: (.*)', content)

    prog = re.compile(r"\\\\")
    abstract = prog.split(content)
    abstract[2] =  re.sub(r'\n|\$(.*)\$','', abstract[2])
    abstract[2] =  re.sub(r'\s+',' ', abstract[2])

    email = re.findall('From: (\S*@\S*) ', content)

    pages = re.findall("Comments: (?:\D*)(\d*)\s?[p,P].*", content)
    #print pages

    venue = re.findall("Journal-ref: ([a-z, A-z, .]*) ", content)
    #print venue

    '''
    if (len(authors) == 0 or len(pages) < 1 or len(venue)==0):
        print '------------------------------------'
        print content
        print '------------------------------------'
    '''
    row_content_list = [str(id[0]),title[0],(authors[0] if len(authors) > 0 else 'None' ), year,abstract[2],(email[0] if len(email)>0 else 'None'),(pages[0] if len(pages) > 0 else 'None'),(venue[0] if len(venue) >=1 else 'None'),'None']
    #csv_file.write(str(id[0])+'    '+title[0]+'    '+ (authors[0] if len(authors) > 0 else 'None' ) + '    ' + year + '    ' + '    ' + abstract[2] + '    ' + (email[0] if len(email)>0 else 'None')+'    '+(pages[0] if len(pages) > 0 else 'None') + '    '+(venue[0] if len(venue) >=1 else 'None') +'    ' + 'None\n')
    csv_writer.writerow(row_content_list)

def iterateOverDirectory(dir):
    if os.path.exists(dir):
        for subpath in sorted(os.listdir(dir)):
            full_sub_path = os.path.join(dir, subpath)
            print full_sub_path
            if os.path.isdir(full_sub_path):
                for files in sorted(os.listdir(full_sub_path)):
                    content = open(str(os.path.join(full_sub_path, files)))
                    parse_content(content.read(), subpath)
            

iterateOverDirectory(cfg.abs_dir)
csv_file.close()
