#!/usr/bin/env python

# python program to compare multiple files with multiple columns to find common and unique lines for each file

import os, sys
import argparse


description="python program to find unique and common data lines by one or multiple columns"
usage='''
python find_uniq_common_datalines.py --files file1.txt file2.txt file3.txt --common
python find_uniq_common_datalines.py --files file1.txt file2.txt file3.txt --exactly 1
python find_uniq_common_datalines.py --files file1.txt file2.txt file3.txt --exactly 2
python find_uniq_common_datalines.py --files file1.txt file2.txt file3.txt --atmost 2
python find_uniq_common_datalines.py --files file1.txt file2.txt file3.txt --atleast 2
'''
parser = argparse.ArgumentParser(description=description, usage=usage)

parser.add_argument("--files", "-f", dest="files", nargs='+',  action="store",help="Input files ")
group1 = parser.add_mutually_exclusive_group()
# group1.add_argument("--unique", action="store_true", default=False, dest="unique", help="Find unique data lines")
group1.add_argument("--common", action="store_true", dest="common", help="Find common data lines")
group2 = parser.add_mutually_exclusive_group()
group2.add_argument("--atleast", action="store", type=int, dest="atleast", help="Find data present in at least N files")
group2.add_argument("--exactly", action="store", type=int, dest="exactly", help="Find data present in exactly N files")
group2.add_argument("--atmost", action="store", type=int, dest="atmost", help="Find data present in max N files")

# parser.print_usage()
option = parser.parse_args()
# print(option)

class common_uniq_snp_positions():
    ''' find common and unique snp positions 
    input file format
    chr position    ID  refbase altbase more_columns
    1   100 .   A   T   qual    format  sample Gene
    2   10000   .   T   C   qual    format  sample Gene
    '''

    def __init__(self, infiles):
        self.infiles = infiles
        self.all_lines = {}
        self.number_of_files = len(infiles)
        self.atleast=1

    def all(self):

        ''' create dictionary object with indices from col1 (chr) and col2 (position) 
        returns: dict object
        '''
        for fn in self.infiles:
            with open(fn) as f:
                for line in f:
                    line=line.strip()
                    if line == "":
                        continue
                    else:
                        data = line.split()
                        col1=data[0]
                        col2=data[1]
                        if col1 in self.all_lines.keys():
                            if col2 in self.all_lines[col1].keys():
                                self.all_lines[col1][col2]["count"] +=1
                                # self.all_lines[col1][col2]["line"].add(line)
                                self.all_lines[col1][col2]["file"].append(fn)
                            else:
                                self.all_lines[col1].update({col2:{"count":1, "file":[fn]}} )
                        else:
                            self.all_lines[col1] = {col2:{ "count":1, "file":[fn]}}
        
    
    def get_common(self):

        ''' get common snps by chr and position '''
        print("Getting common snps present in all input files")
        for key1 in self.all_lines.keys():
            for key2 in self.all_lines[key1].keys():
                if int(self.all_lines[key1][key2]["count"]) == self.number_of_files:
                    print(key1 + "\t" + key2)
        
    
    def get_atleast(self, atleast=1):

        ''' get unique snps by chr and position '''
        print("Getting at least")
        self.atleast = atleast
        for key1 in self.all_lines.keys():
            for key2 in self.all_lines[key1].keys():
                if int(self.all_lines[key1][key2]["count"] ) >= self.atleast:
                    print(key1 + "\t" + key2 + "\tin file(s):" + ",".join(self.all_lines[key1][key2]["file"]))

    def get_exactly(self, exactly=1):
        ''' get the snps that are exactly N times among the files '''
        print("Getting exactly")
        self.exactly = exactly
        for key1 in self.all_lines.keys():
            for key2 in self.all_lines[key1].keys():
                if int(self.all_lines[key1][key2]["count"] ) == self.exactly:
                    print(key1 + "\t" + key2 + "\tin file(s):" + ",".join(self.all_lines[key1][key2]["file"]))
    
    def get_atmost(self, atmost=1):
        ''' get the snp positions that are occurring at most N times among the files '''

        print("Getting at most")
        self.atmost = atmost
        for key1 in self.all_lines.keys():
            for key2 in self.all_lines[key1].keys():
                if int(self.all_lines[key1][key2]["count"] ) <= self.atmost:
                    print(key1 + "\t" + key2 + "\tin file(s):" + ",".join(self.all_lines[key1][key2]["file"]))


if __name__ =='__main__':
    myobj = common_uniq_snp_positions(option.files)
    myobj.all()  # call the func named all

    if option.atleast:
        myobj.get_atleast(option.atleast)
    elif option.exactly:
        myobj.get_exactly(option.exactly)
    elif option.atmost:
        myobj.get_atmost(option.atmost)
    else:
        pass

    if option.common == True:
        myobj.get_common()
    else:
        pass

