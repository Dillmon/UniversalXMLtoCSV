# -*- coding: utf-8 -*-
"""
Created on Mon May 13 10:46:13 2019

@author: dmohotti

This script reads the main xml file and each xml path inside the main xml file. It also reads the xml files that
are inside the user defined inDir directory.
Then this script will create a csv table for each xml file found, and will
output the csv files in a user defined output directory. 

This can be used to extract data from RSM xml files or for any other application where data needs to be quickly grabbed from 
xml files. 

To use this script, paste the linux path of the mainXML file into the variable mainXML(below)
and/or place any xml file into the directory of your choice and place the path of that directory into the 
inDir variable (below) and then run the script using python3. This program will read all paths inside quotes that are 
inside the path of the mainXML variable, and place them in a list of xml files to be converted. It will also add any xml files 
that are in the inDir directory to this list. No input arguments needed. 

*This script will not convert short 1 element xml files into csv files. 
Comments from the xml file are not included in the CSV file.
Contact me at dmohotti@sfwmd.gov if these values are important or if
there is an xml file that has crashed the program so I can fix bugs or add features.
"""

import os, re
from string import digits
import os.path
from os import path


#def split_string_on_multiple_separators(input_string, separators):
#    sepstring = ''
#    for sep in separators:
#        if sep != separators[-1]:
#            sepstring = sepstring + sep + '|'
#        if sep == separators[-1]:
#            sepstring = sepstring + sep
#    return re.split(sepstring,input_string)

temp_ex_el_n = []

def split_string_on_multiple_separators(input_string, separators):
    buffer = [input_string]
    for sep in separators:
        strings = buffer
        buffer = []  # reset the buffer
        for s in strings:
            buffer = buffer + [e for e in s.split(sep) if e]
#    for valn in ex_el_n: 
#        temp_ex_el_n.append(valn.replace(' ',''))
    for valb in range(len(buffer)):
        if buffer[valb] in input_string:
#            print('this buffer is past if 1',file=text_file)
            for valex in ex_el_n:
#                print(valex+buffer[valb],file=text_file)
                if valex + buffer[valb] in input_string:
                    buffer[valb] = valex + buffer[valb]
#                    print('this buffer is past if 2',file=text_file)
    return buffer

mainXML = ''


#All input is within this
##############################################################################################################################
#Input Main xml file path here (any file with xml paths inside quotes)
mainXML = '/nw/hesm_nas/projects/MWD_SouthDade/MDRSM/workdir/ruben/COP/ECB19RR/run_mdrsm_ECB19_AVG.xml'
#mainXML = '/nw/hesm_nas/projects/MWD_SouthDade/RSMGL_SouthDade/workdirs/rnovoa/RSMGL_SouthDade/COP/ECB19/main_ECB19.xml'
#Input Directory (place xml files that you want to convert to csv in this folder)
inDir = '/nw/hesm_nas/workdirs/dmohotti/newtransecttool/Indirforcsv/'
#Output Directory (all output will go to this folder)
outDir = '/nw/hesm_nas/workdirs/dmohotti/newtransecttool/Outdirforcsv/'  
##############################################################################################################################



remove_digits = str.maketrans('', '', digits)

if path.exists(mainXML):
    dirname = os.path.dirname(mainXML)
    if path.exists(dirname):
        os.chdir(dirname)
        print(dirname)
        print('cwd',os.getcwd())
#if not os.path.exists(dirname+'/Outdirforcsv'):
#    os.makedirs(dirname+'/Outdirforcsv')

pathList = []

for file in os.listdir(inDir):
    if file.endswith('.xml'):
        print('xmlfile',file)
        pathList.append(inDir + file)

txtpath = outDir + 'output.txt'
count = 0
#Get xml file paths
with open(txtpath, 'w') as text_file:
    if path.exists(mainXML):
        with open(mainXML) as fp:  
           for cnt, line in enumerate(fp, start=1):
               if "xml" in line:
                   xmlPath = re.findall(r'"([^"]*)"', line)
                   for pathl in xmlPath:
                       if "xml" in pathl:
                           pathList.append(pathl)
                           count = count + 1
                           print(f'count: ', count, pathl, file=text_file)

    for pathm in pathList:
        filename = pathm.split('/')
        filename = filename[-1]
        filename = filename.split('.')
        filename = filename[0]
        print('filename',filename)
        with open(pathm) as file:
    #Clean data by removing comments and end of line characters
            data = file.read().replace('\n', '')
            datawocomments = re.sub("(<!--.*?-->)", "", data, flags=re.DOTALL)
    #        print(data)
            sqbracket = datawocomments[datawocomments.find("[")+1:datawocomments.find("]")]
            pattern = r'\[.*?\]'
            datawocomments = re.sub(pattern, '', datawocomments)
#            datawocomments = re.sub("([.*?])", "", datawocomments, flags=re.DOTALL)
            datawocomments = datawocomments.replace("><","> <")
            datawocomments = datawocomments.replace('"/>', '" />')
            datawocomments = datawocomments.replace('">', '" >')
            datawocomments = datawocomments.replace('>', '> ')
            datawocomments = datawocomments.replace('</', ' </')
#            datawocomments = datawocomments.replace("<!ENTITY ","<")
#            datawocomments = datawocomments.replace("SYSTEM ","SYSTEM=")
            datawocomments = ' '.join(datawocomments.split())
            datawocomments = datawocomments.replace(" = ","=")
            datawocomments = datawocomments.replace("= ","=")
            datawocomments = datawocomments.replace(" =","=")       
            datawocomments = datawocomments.replace('=" ','="')
            datawocomments = datawocomments.replace("'", '"')             
            ecmlistmother = [i for i in datawocomments.split() if '<' in i or '=' in i]
            oelistdeterminer = [i for i in datawocomments.split() if '<' in i or '/>' in i]
            listwcomments = [i for i in data.split() if '<' in i]
            listwocomments = [i for i in datawocomments.split() if '<' in i and '/' not in i]
    #        print(instances)
            print('path: ', pathm, '\nlist no comments: ', listwocomments, file=text_file)
            print('ecmlistmother', ecmlistmother, file=text_file)
    #Figure out if file should be turned into csv file and what the first external element is if turned into one
            if len(listwocomments) > 0:
                morethan1 = 0    
                for listno4 in listwocomments:
                    if listwocomments.count(listno4) > 1:
                        morethan1 = 1
                        break
                firstel = 0
                if listwocomments.count(listwocomments[0]) == 1:
                    firstel = 1
                if len(listwocomments) > 2 and morethan1 == 1:
                    for listno in range(len(listwocomments)):

                        if listwocomments.count(listwocomments[listno]) > 1 or listwocomments.count(listwocomments[listno + 1]) > 1 and firstel == 0:
                            ex_el = listwocomments[listno]
                            no_ex_el = listwocomments.count(ex_el)
                            jex_el = ex_el.replace('<','')
                            jex_el = jex_el.replace('>','')
                            print('gay1')
                            print('listno',listno)
                            if listwocomments.count(listwocomments[listno+1]) > listwocomments.count(listwocomments[listno]) and listwocomments.count(listwocomments[listno]) <= 1:
                                ex_el = listwocomments[listno+1]
                                no_ex_el = listwocomments.count(ex_el)
                                jex_el = ex_el.replace('<','')
                                jex_el = jex_el.replace('>','')
                                print('gay2')
                                break
                            break

                else:
                    ex_el = 'none'
                    print('FILE IS TO SHORT!!! DOES NOT NEED TO BE TURNED INTO A CSV FILE!!!!!')
            else:
                ex_el = 'none'
                print('NOTHING HERE')
            
    
    #get substring using the external element
            if ex_el != 'none':
                if '>' not in ex_el:
                    ex_el = ex_el + ' '
                    
                ex_el_n = []
#                ex_el_n.append(ex_el)
#                fex_el = ex_el.replace('<','')

                substring = datawocomments.split(ex_el)
                
               
                ex_el_list = []
                sortlist= []
#                print(substring)
                for lval in substring:
                    ex_el_list.append(len(str(lval)))
                ex_el_list2 = ex_el_list
                print('ex_el_list', ex_el_list2, file=text_file)
                sortlist = ex_el_list
                sortlist = sorted(sortlist)
                print('ex_el', ex_el,'sortlist',sortlist)
                length_max = sortlist[-1]
                length2max = sortlist[-2]
                print('max length', length_max, 'ex_el_list last', ex_el_list[-1])
                print('path',pathm)
                print('length max', length_max, 'second length match', length2max,'endof substring', len(substring[-1]))
#                print('ex_el_list', ex_el_list)
                print('\n\n\nnext, substring',substring, file=text_file)
                #Find extra external elements
                print('length of each element',ex_el_list2,'\n external element list', ex_el_n, 'sortlist', sortlist, file=text_file)
                print('length2max', length2max, 'length of last', len(substring[-1]), file=text_file)
                print('oelistdeterminer',oelistdeterminer,file=text_file)
                exeld = 0
                for val in range(len(oelistdeterminer)):
                    if oelistdeterminer[val].startswith('<') and exeld == 0 and '/>' not in  oelistdeterminer[val] and '</' not in oelistdeterminer[val] and '!' not in oelistdeterminer[val]:
                        hex_el = oelistdeterminer[val]
                        jhex_el = hex_el.replace('<','')
                        jhex_el = jhex_el.replace('>','')
                        if hex_el not in ex_el_n:
                            ex_el_n.append(hex_el)
                        exeld = exeld + 1
                        continue
                    if oelistdeterminer[val].startswith('<') and '/>' not in  oelistdeterminer[val] and '</' not in oelistdeterminer[val] and jhex_el not in oelistdeterminer[val] and '!' not in oelistdeterminer[val]:
                        exeld = exeld + 1
                        continue
                    if oelistdeterminer[val].startswith('</') and '!' not in oelistdeterminer[val]:
                        exeld = exeld - 1
                        continue
                    if '/>' == oelistdeterminer[val] and '!' not in oelistdeterminer[val]:
                        exeld = exeld - 1
                        continue
                    if '!' in oelistdeterminer[val]:
                        continue
                for val in range(len(ex_el_n)):
                    if '>' not in ex_el_n[val] and not str(ex_el_n[val]).endswith(' '):
                        ex_el_n[val] = ex_el_n[val] + ' '
                substring = split_string_on_multiple_separators(datawocomments, ex_el_n)
                print('ex_el_n',ex_el_n, file=text_file)
                print('substring#1',substring, file=text_file)
                    
                        
                        

                
                for val in range(len(ex_el_n)):
                    if '>' not in ex_el_n[val] and not str(ex_el_n[val]).endswith(' '):
                        ex_el_n[val] = ex_el_n[val] + ' '
                if not any(val in substring[0] for val in ex_el_n):
                    title = substring[0]
                else:
                    title = ' '
                title2 = str("".join(map(str,ex_el_n)))
#                if '!' in substring[0] or substring[0] == '':

                if not any(val in substring[0] for val in ex_el_n):
                    del substring[0]

                    
                for val in range(len(ex_el_n)):
                    if str(ex_el_n[val]).endswith(' '):
                        ex_el_n.append(ex_el_n[val].strip())                   



                substringmarker = [i for i in datawocomments.split() if i in ex_el_n]
                
                print('substringmarker', substringmarker, file=text_file)
                print('length of substringmarker', len(substringmarker), file=text_file)
                print('length of each element',ex_el_list,'\n external element list', ex_el_n, file=text_file)
                print(f'\n path:', 'path', pathm,'\n','\n','\n','ex_el', ex_el, file=text_file)
                print('substring', substring, '\nlen of substring', len(substring), file=text_file)
                if len(substringmarker) != len(substring):
                    print('substringmarker and substring do not match', file=text_file)

                    
                headerlist = []
                for val in range(len(substring)):
                    oe = substringmarker[val]
                    ece = [i for i in substring[val].split() if '<' in i or '=' in i or '/>' in i]
#                    print('ece', ece, file=text_file)
#                    headeritem = oe
                    ciel = ''
                    eclist = [str(oe)]
#                    print('substringmarker', substringmarker, file=text_file)
                    for val2 in range(len(ece)):
                        print('val2',val2,'ece',ece[val2],'eclist',eclist,'ece-1', eclist[-1])
#                        print('headerlist',headerlist,file=text_file)
                        if '=' in ece[val2]:
                            ee = ece[val2].split('=')[0]
                            headeritem = ciel + '__' + ee
#                            print('headeritem', headeritem, file=text_file)
                            if headeritem not in headerlist:
                                headerlist.append(headeritem)  
#                                print('headerlist',headerlist, file=text_file)
                        if '<' in ece[val2] and '/' not in ece[val2]:
                            ec = ece[val2].split('<')[1]
                            ec = ''.join([i for i in ec if not i.isdigit()])
                            ec = ec.replace('>','')
                            ciel = ciel + '__' + ec
                            print('ciel1',ciel)
                            eclist.append(ec)
                        if '/' in ece[val2] and '>' in ece[val2] and eclist[-1] in ece[val2] and '=' not in ece[val2]:
                            ec = ece[val2].split('<')[1]
                            k = ciel.rfind('__' + eclist[-1])
                            ciel = ciel[:k] + ""
                            print('ciel2',ciel)
                            eclist.remove(eclist[-1])
                        if ece[val2] == '/>':
                            k = ciel.rfind('__' + eclist[-1])
                            ciel = ciel[:k] + ""
                            print('ciel3',ciel)
                            eclist.remove(eclist[-1])
#                        print('eclist', eclist, file=text_file)       
                print('headerlist', headerlist)
                print('eclist', eclist)
                headerlist.append('extralist name')
                headerlist.append('extralist')            


                with open(outDir + filename + '.csv', 'w') as ofile:
                    ofile.write(title+'\n')
                    ofile.write(title2 +'\n')
                    for val in headerlist[:-1]:
                        ofile.write(val+',')
                    ofile.write(headerlist[-1])
                    
                    equalcarrotmatch = []
                    lvariables = []
                    subsubstring = 0
                    while subsubstring < len(substring):
                        equalcarrotmatch = [i for i in substring[subsubstring].split() if '<' in i or '=' in i or '/>' in i]
                        equalcarrotmatchc = [i for i in substring[subsubstring].split() if '<' in i]
                        equalcarrotmatche = [i for i in substring[subsubstring].split() if '=' in i]
                        equalcarrotmatchq = re.findall('="' + '(.*?)' +  '"', substring[subsubstring])
                        lvariables = []
                        ecindexl=[]
#                        if len(equalcarrotmatch) > 0:
#                            if '</' in equalcarrotmatch[-1]:
#                                matchx = equalcarrotmatch[-1].replace('</','')
#                                matchx = matchx.replace('>','')
#                                for val in ex_el_n:
#                                    if matchx in val and equalcarrotmatch.count(val) == 0:
#                                        equalcarrotmatch.insert(0,val)
#                                        break
                                        
                        for val6 in range(len(equalcarrotmatch)):
                            if '=' in equalcarrotmatch[val6]:
                                variable = equalcarrotmatch[val6].split('=')
                                lvariables.append(variable[0])
                                ecindex = val6
                                ecindexl.append(ecindex)
    
                        print('equalcarrotmatch', equalcarrotmatch, file=text_file)
                        print('equalcarrotmatchc', equalcarrotmatchc, file=text_file)
                        print('equalcarrotmatche', equalcarrotmatche, file=text_file)
                        print('equalcarrotmatchq', equalcarrotmatchq, file=text_file)
                        print('lvariables', lvariables, file=text_file)
                        print('ecindexl',ecindexl, file=text_file)
                        print('length of equalcarrot and quoted and lvariables and original', len(equalcarrotmatche), len(equalcarrotmatchq),len(lvariables), len(equalcarrotmatch), file=text_file)
                        if len(equalcarrotmatche) != len(equalcarrotmatchq):
                            print('equalcarrotmatche and equalcarrotmatchq do not match',file=text_file)
                        print('headerlist', headerlist, file=text_file)
#                        for val in range(len(equalcarrotmatche)):
#                            if equalcarrotmatchq[val] not in equalcarrotmatche[val]:
#                                print('equalcarrotmatche and equalcarrotmatchq do  not match',equalcarrotmatchq[val],equalcarrotmatche[val],file=text_file)
    #                    subsubstring = subsubstring + 1
    #                    print('subsubstring', subsubstring, 'substring', file=text_file)
                        

                        ecmlist = []
                        for lval in equalcarrotmatch:
#                            if str(lval).startswith('<') and '>' in lval and '/' not in lval:
                            if str(lval).startswith('<') and '/' not in lval:
                                if lval not in ecmlist:
                                    ecmlist.append(lval)
                        countlist = []
                        countlist3 = []
                        for ecmval in ecmlist:
                            count2 = equalcarrotmatch.count(ecmval)
                            countlist.append(count2)
                            countlist3.append(0)
#                        print('ecmlist : ', ecmlist, 'countlist: ', countlist,'countlist3',countlist3, file=text_file)
                        num = 0
    #                    morenum = 0
                        cl3 = 0
                        valvarit = 0

                        values= []
                        headeritems = []
                        oe = substringmarker[subsubstring]
#                        headeritem = oe
                        ciel = ''
                        eclist = [str(oe)]
                        while num < (len(equalcarrotmatch)-1):
#                            for val2 in range(len(equalcarrotmatch)):
                            if '=' in equalcarrotmatch[num]:
                                ee = equalcarrotmatch[num].split('=')[0]
                                headeritem = ciel + '__' + ee
#                                print('headeritem',headeritem,file=text_file)
                                for val9 in range(len(headerlist)):
                                    if headeritem == headerlist[val9]:
#                                        print('ecindexl', ecindexl, 'valvarit',valvarit, file=text_file)
                                        finalval = equalcarrotmatchq[valvarit]
#                                        print(finalval,file=text_file)
#                                        print('finalval',finalval,file=text_file)
                                        values.append(finalval)
                                        headeritems.append(headeritem)
#                                        print('headeritem',headeritem,file=text_file)
                                        valvarit = valvarit + 1

                                        

                            if '<' in equalcarrotmatch[num] and '/' not in equalcarrotmatch[num]:
                                
                                ec = equalcarrotmatch[num].split('<')[1]
                                ec = ''.join([i for i in ec if not i.isdigit()])
                                ec = ec.replace('>','')
                                ciel = ciel + '__' + ec
                                eclist.append(ec)
                            if '/' in equalcarrotmatch[num] and '>' in equalcarrotmatch[num] and eclist[-1] in equalcarrotmatch[num] and '=' not in equalcarrotmatch[num]:
                                ec = equalcarrotmatch[num].split('<')[1]
                                k = ciel.rfind('__' + eclist[-1])
                                ciel = ciel[:k] + ""
                                eclist.remove(eclist[-1])
                            if equalcarrotmatch[num] == '/>':
                                k = ciel.rfind('__' + eclist[-1])
                                ciel = ciel[:k] + ""
                                eclist.remove(eclist[-1])
#                            print('eclist', eclist, file=text_file)    
                                
#                            print('headerlist', headerlist, file=text_file)
#                            headerlist.append('extralist')   
                            
                            
                            if str(equalcarrotmatch[num]).startswith('<') and '/' not in str(equalcarrotmatch[num]): # and '>' in str(equalcarrotmatch[num]):
                                match1 = equalcarrotmatch[num].replace('<','')
                                match1 = match1.replace('>','')
                                print('match1',match1)
                                for val10 in range(num+1,len(equalcarrotmatch)):
                                    print('equalcarrotmatchnum',equalcarrotmatch[num])
                                    print('equalcarrotmatchval10',equalcarrotmatch[val10])
                                    if match1 in equalcarrotmatch[val10] and '=' not in equalcarrotmatch[val10]:
                                        match2 = match1
                                        det = 1
                                        print('matchfound')
                                        break
                                    if '=' in equalcarrotmatch[val10]:
                                        continue
                                    if '=' not in equalcarrotmatch[val10] and match1 not in equalcarrotmatch[val10]:
                                        det = 0
                                        break

#                                for val10 in equalcarrotmatch:
#                                    if val10.startswith('</'):
#                                        match2 = val10.replace('</','')
#                                        match2 = match2.replace('>','')
        #                                if '</' in str(equalcarrotmatch[num+1]) and match2 + '>' in str(equalcarrotmatch[num+1]):
        #                                print('subsubstring', subsubstring, 'num', num, 'equalcarrotmatchnum', equalcarrotmatch[num], equalcarrotmatch[num+1], file=text_file)
        #                                if  equalcarrotmatch[num+1] != equalcarrotmatch[num-1]: #and equalcarrotmatch.count(equalcarrotmatch[num]) > 1:
                                if det == 1 and '!' not in match2:
                                    for ml in range(len(ecmlist)):
                                        if '<' + match2 == ecmlist[ml] or '<' + match2 + '>' == ecmlist[ml]:
                                            cl3 = ml
                                    print('subsubstring', subsubstring, 'num', num, 'equalcarrotmatchnum', equalcarrotmatch[num], equalcarrotmatch[num+1],'match2', match2, file=text_file)
                                    middlestring = re.findall('<' + match2 + '(.*?)' + '</' + match2 + '>', substring[subsubstring])
                                    print('length of middle string: ',len(middlestring), 'cl3', cl3, file=text_file)
    #                                    print('length of middle string: ',len(middlestring), 'cl3', cl3, file=text_file)
                                    print('middlestring',middlestring,file=text_file)
                                    middlestring = middlestring[countlist3[cl3]]
                                    middlestring = ' '.join(middlestring.split())
                                    middlestring = re.sub(r'.*> ', '', middlestring)
                                    print('middlestring:', middlestring, file=text_file)
                                    values.append(match2)
                                    headeritems.append('extralist name')
                                    values.append(middlestring)
                                    headeritems.append('extralist')

                                            
    
    #                                print('countlist3',countlist3[cl3])
                                    countlist3[cl3] = countlist3[cl3] + 1
    #                                print('countlist3',countlist3[cl3])
                                    
                            num = num + 1
#                        print('values',values,file=text_file)
#                        print('headeritems', headeritems, file=text_file)
                        if len(values) != len(headeritems):
                            print('headeritems and values do not match', file=text_file)
                        
                        
                        subnumber2 = headeritems.count('extralist name')
#                        print('number of extralistnames',subnumber2,file=text_file)
                        extralistname = []
                        if subnumber2 >0:
                            for val3 in range(len(headeritems)):
                                if headeritems[val3] == 'extralist name':
                                    extralistname.append(values[val3])   
#                        print('extralistname',extralistname,'len of extralistname', len(extralistname), file=text_file)
                        
                        subnumber = headeritems.count('extralist')
#                        print('numberofextralists', subnumber, file=text_file)
                        extralistlist = []
                        if subnumber > 0:
                            for val3 in range(len(headeritems)):
                                if headeritems[val3] == 'extralist':
                                    extralistlist.append(values[val3])
#                        print('extralistlist', extralistlist,'len of extralistlist', len(extralistlist), file=text_file)
                        
                        print('headeritems',headeritems,file=text_file)
                        print('headerlist',headerlist,file=text_file)
                        print('values', values,file=text_file)
                        print('extralist name', extralistname,file=text_file)
                        print('extralistlist',extralistlist,file=text_file)
                        
                        
                        rowindex = []
#                        if 'extralist' not in headeritems:
                        for val8 in headeritems:
                            for val7 in range(len(headerlist)):
                                if val8 == headerlist[val7]:
                                    rowindex.append(val7)
#                        print('rowindex', rowindex, file=text_file)
                        lastelind = len(headerlist)-1
#                        print('lastelind',lastelind,file=text_file)
                        indbreak = []
                        for indnum in range(len(rowindex)-1):
                            if rowindex[indnum+1] < rowindex[indnum] and rowindex[indnum] != lastelind and rowindex.count(rowindex[indnum+1]) > 1:
                                indbreak.append(indnum)
                        if len(indbreak) > 0:
                            print('indbreak',indbreak,file=text_file)
                        indbreak.append(int(len(rowindex)))
                        for pluslist in range(len(indbreak)):
                            complist = [None] * len(headerlist)
#                            for el in range(len(headerlist)-1):
                            for val in range(len(rowindex[:indbreak[pluslist]])):
                                for el in range(len(headerlist)-1):
                                    if rowindex[val] == el:
#                                        print('val',val,file=text_file)
                                        complist[el] = values[val]
#                            print('complist',complist,file=text_file)
                            if len(extralistlist) == 0:
                                ofile.write('\n')
                                for val in complist[:-1]:
                                    ofile.write(str(val)+',')
                                ofile.write(str(complist[-1])) 
                            else:
                                for val3 in range(len(extralistlist)):
                                    complist[-2] = extralistname[val3]
                                    complist[-1] = extralistlist[val3]
    #                                print('complist',complist,file=text_file) 
                                    ofile.write('\n')
                                    for val in complist[:-1]:
                                        ofile.write(str(val)+',')
                                    ofile.write(str(complist[-1]))
                                                                          
                            
                        subsubstring = subsubstring + 1

            else:
                print(f'FILE IS TO SHORT!!! DOES NOT NEED TO BE TURNED INTO A CSV FILE!!!!! or NOTHING IN FILE!!!',  file=text_file)
