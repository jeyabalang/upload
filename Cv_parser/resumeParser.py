#!/usr/bin/env python
import pandas as pd
import nltk, os, subprocess, code, glob, re, traceback, sys, inspect
from time import clock, sleep
from pprint import pprint
import json
import zipfile
# import ner
from convertPDFToText import convertPDFToText
from convertDocxToText import convertDocxToText
from bottle import template
from convertRtfToText import convertRtfToText



class exportToCSV_and_exportToExcel:
    def __init__(self, fileName='resultsCSV.txt', resetFile=False):
        headers = ['FILE NAME',
               'NAME',
               'EMAIL1', 'EMAIL2', 'EMAIL3', 'EMAIL4',
               'PHONE1', 'PHONE2', 'PHONE3', 'PHONE4',
               'INSTITUTES1','YEARS1',
               'INSTITUTES2','YEARS2',
               'INSTITUTES3','YEARS3',
               'INSTITUTES4','YEARS4',
               'INSTITUTES5','YEARS5',
               'EXPERIENCE',
               'DEGREES','DATE OF BIRTH',"addresses"
               ]
        if not os.path.isfile(fileName) or resetFile:
            # Will create/reset the file as per the evaluation of above condition
            fOut = open(fileName, 'w')
            fOut.close()
        fIn = open(fileName) ########### Open file if file already present
        inString = fIn.read()
        fIn.close()
        if len(inString) <= 0: ######### If File already exsists but is empty, it adds the header
            fOut = open(fileName, 'w')
            fOut.write(','.join(headers)+'\n')
            fOut.close()

    def write(self, infoDict):
        if os.path.exists("resultsCSV.txt"):
          os.remove("resultsCSV.txt")
        fOut = open('resultsCSV.txt', 'a+')
        # Individual elements are dictionaries
        writeString = ''
        try:
            writeString += str(infoDict['fileName']) + ','
            writeString += str(infoDict['name']) + ','
            
            if infoDict['email']:
                writeString += str(','.join(infoDict['email'][:4])) + ','
            if len(infoDict['email']) < 4:
                writeString += ','*(4-len(infoDict['email']))
            if infoDict['phone']:
                writeString += str(','.join(infoDict['phone'][:4])) + ','
            if len(infoDict['phone']) < 4:
                writeString += ','*(4-len(infoDict['phone']))            
            writeString += str(infoDict['%sinstitute'%'c\\.?a'])+","
            writeString +=str(infoDict['%syear'%'c\\.?a'])+","
            writeString += str(infoDict['%sinstitute'%'b\\.?com'])+","
            writeString +=str(infoDict['%syear'%'b\\.?com'])+","
            writeString += str(infoDict['%sinstitute'%'icwa'])+","
            writeString +=str(infoDict['%syear'%'icwa'])+","
            writeString += str(infoDict['%sinstitute'%'m\\.?com'])+","
            writeString +=str(infoDict['%syear'%'m\\.?com'])+","
            writeString += str(infoDict['%sinstitute'%'mba'])+","
            writeString +=str(infoDict['%syear'%'mba'])+","
            writeString += str(infoDict['experience']) + ','
            writeString += str(infoDict['work_experience']) + ','
            writeString += str(infoDict['skill']) + ','
                       
            writeString += str(infoDict['degree']) + ','
            writeString += str(infoDict['dateofbirth']) + ',' # For the remaining elements
         
            writeString += str(infoDict['addresses']) + ',' # For the remaining elements
            
            fOut.write(writeString)
        except:
            fOut.write('FAILED_TO_WRITE\n')
        fOut.close()
        print(infoDict,"excel")

       
        dict_df = pd.DataFrame({ key:pd.Series(value) for key, value in infoDict.items() })

        dict_df
        df = (dict_df.T)


        print (df)
        if os.path.exists("Cv_parser_output.xlsx"):
          os.remove("Cv_parser_output.xlsx")
    

        dict_df.to_excel('Cv_parser_output.xlsx')

        return infoDict
        
class Parse():
    # List (of dictionaries) that will store all of the values
    # For processing purposes
    information=[]
    inputString = ''
    tokens = []
    lines = []
    sentences = []
  
    def __init__(self, filename,verbose=False):
        print(self.inputString,"text")
        print('Starting Programme')
        fields = ["name", "address", "email", "phone", "mobile", "telephone", "residence status","experience","degree","cainstitute","cayear","caline","b.cominstitute","b.comyear","b.comline","icwainstitue","icwayear","icwaline","m.cominstitute","m.comyear","m.comline","mbainstitute","mbayear","mbaline"]

        doc_files = glob.glob("resumes/*.doc")
        docx_files = glob.glob("resumes/*.docx")
        pdf_files = glob.glob("resumes/*.pdf")
        rtf_files = glob.glob("resumes/*.rtf")
        text_files = glob.glob("resumes/*.txt")
        
        files = set(doc_files+docx_files+pdf_files+rtf_files+text_files)
        print(files,"files")
        files = list(files)

        print ("%d files identified" %len(files))
 
        for f in files:
            print("Reading File %s"%f)
            # info isfile a dictionary that stores all the data obtained from parsing
            info = {}

            self.inputString, info['extension'] = self.readFile(f)           
            info['fileName'] = f
            print (info['extension'],"extension")
            print(self.inputString,"text")
            self.tokenize(self.inputString)

            self.getName(self.inputString, info)

            self.getEmail(self.inputString, info)

            self.getPhone(self.inputString, info)

            self.dateofbirth(self.inputString,info)

            self.addresses(self.inputString,info)


            self.Qualification(self.inputString,info)

            self.technicalskill(self.inputString,info)

            print("work_experience")
            self.work_experience(self.inputString,info)

            self.getExperience(self.inputString,info)
           

            print(info,"information") 
            del info['otherNameHits']
            if info['m\.?comline']:
               continue
            else:     
             del info['m\.?comline']
           
            print(info,"info")
            csv=exportToCSV_and_exportToExcel()
            csv.write(info)
            self.information.append(info)

    def technicalskill(self,inputString,infoDict):
         infoDict['softskill']=0
         try:
                print(inputString,"string_text")
                pattern = re.compile(r'(((accomplishments)(.+)((?:\n.+)+)(credentials))|((Activities|softskills)(.+)((?:\n.+)+)))',re.I)

                matches = pattern.search(inputString) # Gets all email addresses as a list
                experience = matches.group()
                print(experience,"experience_softskill")
                softskill=experience.splitlines()
                print(softskill[0],"softskill")
                if "Accomplishments\t\t"==softskill[0]:
                    del softskill[0]
                if  "Personal Credentials"==softskill[len(softskill)-1]:
                    del softskill[len(softskill)-1]


                infoDict['softskill'] = softskill
         except Exception as e:
            print (e ) 
          
    def experience_institute(self,inputString,infoDict):
         infoDict['experience']=0
         try:
                pattern = re.compile(r'(?<=experience)(.*)',re.I)
                matches = pattern.search(inputString) # Gets all email addresses as a list
                experience = matches.group()

                infoDict['experience'] = experience
         except Exception as e:
            print (e )
    
    def work_experience(self,inputString,infoDict):
        infoDict['work_experience'] = "None" 
        experiences=[]  
        try:
           import re
           print ("work_experience")
           pattern = re.compile(r'((?:Jan|Feb|Mar|Apr|May|Jun|July|Aug|Sep|Oct|nov|Dec)(\s\d+\s)(~)(\s)(?:Jan|Feb|Mar|Apr|May|Jun|July|Aug|Sep|Oct|nov|Dec)(\s\d+\s)(.*))|((?:Jan|Feb|Mar|Apr|May|Jun|July|Aug|Sep|Oct|nov|Dec)(\s\d+\s)(~)(\s)(present)(.*))|(EXPERIENCE(.+)((?:\n.+)+))')
           match = pattern.findall(inputString)
           print(match,"match")
           infoDict['work_experience']=match
        except Exception as e:
            print (e )
    
    def dateofbirth(self,inputString,infoDict):
        infoDict['Dateofbirth'] = None
        try:
                pattern = re.compile(r'(?<=date of birth)(.*)',re.I)
                matches = pattern.search(inputString) # Gets all email addresses as a list
                dateofbirth = matches.group()

                infoDict['Dateofbirth'] = dateofbirth.replace('Date of Birth','')
        except Exception as e:
            print (e )
    
    def addresses(self,inputString,infoDict):
        infoDict['addresses'] = None
        try:
                pattern = re.compile(r'(?<=Address)(.*)',re.I)
                matches = pattern.search(inputString) # Gets all email addresses as a list
                if pattern:
                    addresses = matches.group()
                    if addresses:
                        infoDict['addresses'] = addresses.replace('Permanent Address','')
        except Exception as e:
            print (e )

    def readFile(self, fileName):
        '''
        Read a file given its name as a string.
        Modules required: os
        UNIX packages required: antiword, ps2ascii
        '''
        extension = fileName.split(".")[-1]
        if extension == "txt":
            f = open(fileName, 'r')
            string = f.read()
            f.close() 
            print(string)
            return string, extension
        elif extension == "doc":
            # Run a shell command and store the output as a string
            # Antiword is used for extracting data out of Word docs. Does not work with docx, pdf etc.
            return subprocess.Popen(['antiword', fileName], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0], extension
        elif extension == "docx":
            try:
                return convertDocxToText(fileName), extension
            except:
                return ''
                pass
        elif extension == "rtf":
           try:
            print("enter")
            return convertRtfToText(fileName), extension
           except:
               return ''
               pass
        elif extension == "pdf":
            # ps2ascii converst pdf to ascii text
            # May have a potential formatting loss for unicode characters
            # return os.system(("ps2ascii %s") (fileName))
            try:
                return convertPDFToText(fileName), extension
            except:
                return ''
                pass
        else:
            print ('Unsupported format')
            return '', ''

    def preprocess(self, document):
        '''
        Information Extraction: Preprocess a document with the necessary POS tagging.
        Returns three lists, one with tokens, one with POS tagged lines, one with POS tagged sentences.
        Modules required: nltk
        '''
        try:
            # Try to get rid of special characters
            # try:
            #     document = document.decode('ascii', 'ignore')

            # except:
            #     document = document.encode('ascii', 'ignore')
            # Newlines are one element of structure in the data
            # Helps limit the context and breaks up the data as is intended in resumes - i.e., into points
            lines = [el.strip() for el in document.split("\n") if len(el) > 0]  # Splitting on the basis of newlines 
            print(lines,"lines")
            lines = [nltk.word_tokenize(el) for el in lines]    # Tokenize the individual lines
            print(lines,"word")
            lines = [nltk.pos_tag(el) for el in lines]  # Tag them
            print(lines,"lines_pos *")
            # Below approach is slightly different because it splits sentences not just on the basis of newlines, but also full stops 
            # - (barring abbreviations etc.)
            # But it fails miserably at predicting names, so currently using it only for tokenization of the whole document
            sentences = nltk.sent_tokenize(document)    # Split/Tokenize into sentences (List of strings)
            sentences = [nltk.word_tokenize(sent) for sent in sentences]    # Split/Tokenize sentences into words (List of lists of strings)
            tokens = sentences
            sentences = [nltk.pos_tag(sent) for sent in sentences]    # Tag the tokens - list of lists of tuples - each tuple is (<word>, <tag>)
            # Next 4 lines convert  tokens from a list of list of strings to a list of strings; basically stitches them together
            dummy = []
            for el in tokens:
                dummy += el
            tokens = dummy
            # tokens - words extracted from the doc, lines - split only based on newlines (may have more than one sentence)
            # sentences - split on the basis of rules of grammar
            return tokens, lines, sentences
        except Exception as e:
            print (e )

    def tokenize(self, inputString):
        try:
            self.tokens, self.lines, self.sentences = self.preprocess(inputString)
            return self.tokens, self.lines, self.sentences
        except Exception as e:
            print (e)
    def getEmail(self, inputString, infoDict, debug=False): 
        '''
        Given an input string, returns possible matches for emails. Uses regular expression based matching.
        Needs an input string, a dictionary where values are being stored, and an optional parameter for debugging.
        Modules required: clock from time, code.
        '''

        try:
            pattern = re.compile(r'\S*@\S*')
            matches = pattern.findall(inputString) # Gets all email addresses as a list
            email = matches
        except Exception as e:
            print (e)

        infoDict['Email'] = email

        if debug:
            print ("\n", pprint(infoDict), "\n")
            code.interact(local=locals())
        return email

    def getPhone(self, inputString, infoDict, debug=False):
        '''
        Given an input string, returns possible matches for phone numbers. Uses regular expression based matching.
        Needs an input string, a dictionary where values are being stored, and an optional parameter for debugging.
        Modules required: clock from time, code.
        '''

        try:
            pattern = re.compile(r'([+(]?\d+[)\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d*[ \t\r\f\v]*)')
                # Understanding the above regex
                # +91 or (91) -> [+(]? \d+ -?
                # Metacharacters have to be escaped with \ outside of character classes; inside only hyphen has to be escaped
                # hyphen has to be escaped inside the character class if you're not incidication a range
                # General number formats are 123 456 7890 or 12345 67890 or 1234567890 or 123-456-7890, hence 3 or more digits
                # Amendment to above - some also have (0000) 00 00 00 kind of format
                # \s* is any whitespace character - careful, use [ \t\r\f\v]* instead since newlines are trouble
            match = pattern.findall(inputString)
            # match = [re.sub(r'\s', '', el) for el in match]
                # Get rid of random whitespaces - helps with getting rid of 6 digits or fewer (e.g. pin codes) strings
            # substitute the characters we don't want just for the purpose of checking
            match = [re.sub(r'[,.]', '', el) for el in match if len(re.sub(r'[()\-.,\s+]', '', el))>6]
                # Taking care of years, eg. 2001-2004 etc.
            match = [re.sub(r'\D$', '', el).strip() for el in match]
                # $ matches end of string. This takes care of random trailing non-digit characters. \D is non-digit characters
            match = [el for el in match if len(re.sub(r'\D','',el)) <= 15]
                # Remove number strings that are greater than 15 digits
            try:
                for el in list(match):
                    # Create a copy of the list since you're iterating over it
                    if len(el.split('-')) > 3: continue # Year format YYYY-MM-DD
                    for x in el.split("-"):
                        try:
                            # Error catching is necessary because of possibility of stray non-number characters
                            # if int(re.sub(r'\D', '', x.strip())) in range(1900, 2100):
                            if x.strip()[-4:].isdigit():
                                if int(x.strip()[-4:]) in range(1900, 2100):
                                    # Don't combine the two if statements to avoid a type conversion error
                                    match.remove(el)
                        except:
                            pass
            except:
                pass
            number = match
        except:
            pass

        infoDict['Phone'] = number

        if debug:
            print ("\n", pprint(infoDict), "\n")
            code.interact(local=locals())
        return number

    def getName(self, inputString, infoDict, debug=False):
        '''
        Given an input string, returns possible matches for names. Uses regular expression based matching.
        Needs an input string, a dictionary where values are being stored, and an optional parameter for debugging.
        Modules required: clock from time, code.
        '''

        # Reads Indian Names from the file, reduce all to lower case for easy comparision [Name lists]
        indianNames = open("allNames.txt", "r").read().lower()
        # Lookup in a set is much faster
        indianNames = set(indianNames.split())
        

        # otherNameHits = []
        nameHits = []
        name = None

        try:
            tokens, lines, sentences = self.preprocess(inputString)
            tokens, lines, sentences = self.tokens, self.lines, self.sentences
            # Try a regex chunk parser
            # grammar = r'NAME: {<NN.*><NN.*>|<NN.*><NN.*><NN.*>}'
            grammar = r'NAME: {<NN.*><NN.*><NN.*>*}'
            # Noun phrase chunk is made out of two or three tags of type NN. (ie NN, NNP etc.) - typical of a name. {2,3} won't work, hence the syntax
            # Note the correction to the rule. Change has been made later.
            chunkParser = nltk.RegexpParser(grammar)
            all_chunked_tokens = []
            print(lines,tokens,sentences,"lines")
            for tagged_tokens in lines:
                # Creates a parse tree
                if len(tagged_tokens) == 0: continue # Prevent it from printing warnings
                chunked_tokens = chunkParser.parse(tagged_tokens)
                all_chunked_tokens.append(chunked_tokens)
                for subtree in chunked_tokens.subtrees():
                    #  or subtree.label() == 'S' include in if condition if required
                    if subtree.label() == 'NAME':
                        for ind, leaf in enumerate(subtree.leaves()):
                            if leaf[0].lower() in indianNames and 'NN' in leaf[1]:
                                # Case insensitive matching, as indianNames have names in lowercase
                                # Take only noun-tagged tokens
                                # Surname is not in the name list, hence if match is achieved add all noun-type tokens
                                # Pick upto 3 noun entities
                                hit = " ".join([el[0] for el in subtree.leaves()[ind:ind+3]])
                                # Check for the presence of commas, colons, digits - usually markers of non-named entities 
                                if re.compile(r'[\d,:]').search(hit): continue
                                nameHits.append(hit)
                                # Need to iterate through rest of the leaves because of possible mis-matches
            # Going for the first name hit
            if len(nameHits) > 0:
                nameHits = [re.sub(r'[^a-zA-Z \-]', '', el).strip() for el in nameHits] 
                name = " ".join([el[0].upper()+el[1:].lower() for el in nameHits[0].split() if len(el)>0])
                otherNameHits = nameHits[1:]

        except Exception as e:
            print (traceback.format_exc())
            print (e)         

        infoDict['name'] = name
        infoDict['otherNameHits'] = otherNameHits

        if debug:
            print ("\n", pprint(infoDict), "\n")
            code.interact(local=locals())
        return name, otherNameHits  
    

    def getExperience(self,inputString,infoDict,debug=False):

        print("experience")
        try:
            for sentence in self.lines:#find the index of the sentence where the degree is find and then analyse that sentence
                    sen=" ".join([words[0].lower() for words in sentence])
                    print(sen,"sentence") #string of words in sentence
                    if re.search('experience',sen):
                        sen_tokenised= nltk.word_tokenize(sen)
                        tagged = nltk.pos_tag(sen_tokenised)
                        print(tagged,"tagged")
                        entities = nltk.chunk.ne_chunk(tagged)
                        print(entities,"entities")
                        for subtree in entities.subtrees():
                            for leaf in subtree.leaves():
                                if leaf[1]=='CD':
                                    experience=leaf[0]
                                    print(experience)
        except Exception as e:
            print (traceback.format_exc())
            print (e) 
        if experience:
            infoDict['experience'] = experience
        else:
            infoDict['experience']=0
        if debug:
            print ("\n", pprint(infoDict), "\n")
            code.interact(local=locals())
        return experience


        

    def getQualification(self,inputString,infoDict,D1,D2):
        #key=list(qualification.keys())
        qualification={'institute':'','year':''}
        print(inputString,infoDict,D1,D2,"parameters of getQualification")

        nameofinstitutes=open('nameofinstitutes.txt','r').read().lower()#open file which contains keywords like institutes,university usually  fond in institute names
        nameofinstitues=set(nameofinstitutes.split())
        
        print(nameofinstitues,"nameofinstitues")
        instiregex=r'INSTI: {<DT.>?<NNP.*>+<IN.*>?<NNP.*>?}'
        print(instiregex,"instiregex")
        chunkParser = nltk.RegexpParser(instiregex)
        print(chunkParser,"chunkParser")
        print("==================================")
        print("inputString",inputString)
        print("infoDict",infoDict)

        print("==================================")
        try:           
            index=[]
            line=[]
            print ("text",self.lines)
            print(D1,D2,"D2")#saves all the lines where it finds the word of that education
            for ind, sentence in enumerate(self.lines):#find the index of the sentence where the degree is find and then analyse that sentence
                sen=" ".join([words[0].lower() for words in sentence]) #string of words
                print("sen",sen)
                if re.search(D1,sen) or re.search(D2,sen):
                    index.append(ind)
                    print(ind,"ind")  #list of all indexes where word Ca lies
            if index:#only finds for Ca rank and CA year if it finds the word Ca in the document
                print(index)
                for indextocheck in index:#checks all nearby lines where it founds the degree word.ex-'CA'
                    print(indextocheck,"indextocheck")
                    for i in [indextocheck,indextocheck+1]: #checks the line with the keyword and just the next line to it
                        try:
                            try:
                                print(i)
                                wordstr=" ".join(words[0] for words in self.lines[i])#string of that particular line
                                print(wordstr,"wordstrz")
                            except:
                                wordstr=""
                            #if re.search(r'\D\d{1,3}\D',wordstr.lower()) and qualification['rank']=='':
                                    #qualification['rank']=re.findall(r'\D\d{1,3}\D',wordstr.lower())
                                    #line.append(wordstr)
                            if re.search(r'\b[21][09][8901][0-9]',wordstr.lower()) and qualification['year']=='':

                                    qualification['year']=re.findall(r'\b[21][09][8901][0-9]',wordstr.lower())
                                    line.append(wordstr)
                                    print(line,"line")
                            chunked_line = chunkParser.parse(self.lines[i])#regex chunk for searching univ name
                            print(chunked_line,"chunked_line")
                            for subtree in chunked_line.subtrees():
                                    if subtree.label()=='INSTI':
                                        for ind,leaves in enumerate(subtree):
                                            if leaves[0].lower() in nameofinstitutes and leaves[1]=='NNP' and qualification['institute']=='':
                                                qualification['institute']=' '.join([words[0]for words in subtree.leaves()])
                                                line.append(wordstr)
                                                print(line,"append list ")
                                
                        except Exception as e:
                            print (traceback.format_exc())

            if D1=='c\.?a':
                infoDict['%sinstitute'%D1] ="I.C.A.I"
            else:
                if qualification['institute']:
                    infoDict['%sinstitute'%D1] = str(qualification['institute'])
                else:
                    infoDict['%sinstitute'%D1] = "NULL"
            if qualification['year']:
                infoDict['%syear'%D1] = int(qualification['year'][0])
            else:
                infoDict['%syear'%D1] =0
            infoDict['%sline'%D1]=list(set(line))
        except Exception as e:
            print (traceback.format_exc())
            print (e) 


    def Qualification(self,inputString,infoDict,debug=False):
    
        #Q={'CAinformation':'','ICWAinformation':'','B.Cominformation':'','M.Cominformation':'','MBAinformation':''}
        degre=[]
        #degree1=open('degree.txt','r').read().lower()#string to read from the txt file which contains all the degrees
        #degree=set(el for el in degree1.split('\n'))#saves all the degrees seperated by new lines,degree name contains both abbreviation and full names check file
        #qualification1={'CAline':'','CAcollege':'','CArank':'','CAyear':''}
        
        jayatemp=self.getQualification(self.inputString,infoDict,'c\.?a','chartered accountant')
        
        print(infoDict,"getQualification")
        print(infoDict['%sline'%'c\.?a'],"infoDict['%sline'%'c\.?a']")
        if infoDict['%sline'%'c\.?a']:
         degre.append('ca')
        self.getQualification(self.inputString,infoDict,'icwa','icwa')
        if infoDict['%sline'%'icwa']:
         degre.append('icwa')
        self.getQualification(self.inputString,infoDict,'b\.?com','bachelor of commerce')
        if infoDict['%sline'%'b\.?com']:
         degre.append('b.com')
        self.getQualification(self.inputString,infoDict,'m\.?com','masters of commerce')
        if infoDict['%sline'%'m\.?com']:
         degre.append('m.com') 
        self.getQualification(self.inputString,infoDict,'mba','mba')
        if infoDict['%sline'%'mba']:
         degre.append('mba')
        if degre:
            print(degre,"degre")
            infoDict['degree'] = degre
        else:
            infoDict['degree'] = "NONE"
        if debug:
            print ("\n", pprint(infoDict), "\n")
            code.interact(local=locals())
        return infoDict['degree']


if __name__ == "__main__":
    verbose = False
    if "-v" in str(sys.argv):
        verbose = True
    file=sys.argv[1]    
    print(file,"filename")
    p = Parse(verbose,file)
