import pymysql,subprocess,sys

from bottle import route, run, request, get,template,post
from IPython.display import HTML, Javascript
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='pass@1234', db='world')

c = conn.cursor()




import os


@route("/cvhandler", method="post")
def formhandler():
    import os
   
    data = request.files.get('upload')

    cwd1 = os.getcwd()+"/"+"resumes"
    cwd=os.getcwd()

   
    filesToRemove = [os.path.join(cwd1,f) for f in os.listdir(cwd1)]
    for f in filesToRemove:
        os.remove(f)
    data.save(cwd+"/"+"resumes",overwrite=True)
     
    if data and data.file:
        raw = data.file.read() # This is dangerous for big files
        filename = data.filename
        print("the file is  {0} the length is{1} ".format(filename,len(raw)))
        import sys
        import subprocess

       
        p= subprocess.call(['python', 'resumeParser.py',filename])
        from win32com.client.gencache import EnsureDispatch
        from win32com.client import constants
        import pandas as pd
        
        if os.path.exists("Cv_output.html"):
          print("enter output")  
          os.remove("Cv_output.html")
        df = os.getcwd()+"/"+"Cv_parser_output.xlsx"
        
       
        datsets=pd.read_excel(df,na_values=" NaN")
        datsets.fillna("", inplace = True)
        print(datsets,"datasets")
        
        datsets.dropna(how='any')    #to drop if any value in the row has a nan
        datsets.dropna(how='all') 
        
        datsets.style.set_properties(**{'font-size': '11pt', 'font-family': 'Calibri','border-collapse': 'collapse','border': '1px solid black'}).render()
        datsets.columns = ['Sr.no','Extension',   'FileName',   'Name'  , 'Email',   'Phone' ,' Date of birth', 'Addresses' ,'C.A institute',  'C.A year',   'C.A line',   'ICWA institute',   'ICWA year',    'ICWA line' ,'   B.COM institute', 'B.COM line', 'M.COM institute' ,'   M.COM year', 'M.COM line',' MBA institute',    'MBA-year', 'MBA-line', 'Degree' ,'Softskill','Workexperience' ,'Overall Experience']
        Details = datsets.loc[:,"Extension":"Addresses"]
        Education = datsets.loc[:,"C.A institute":"Degree"]
    
        Work_experience = datsets.loc[:,"Softskill":"Overall Experience"]
       
        Details=Details.T
        Education=Education.T
        Work_experience=Work_experience.T
     

        pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>
        pd.set_option('display.max_columns', None)  # or 1000
        pd.set_option('display.max_rows', None)  # or 1000
        pd.set_option('display.max_colwidth', -1)  # or 199
        pd.describe_option('display')

        html_string = '''
        <html>
        <style>
        
        </style>


        <link rel=stylesheet type=text/css href="{{ url_for('static', filename='style.css') }}">
        <h1 align="center" style = "background-color: grey; color: white">Curriculum Vitae Parser</h1>
        <h2><u>Details</u></h2>
        
          {table}
  

        </html>

        '''
        html_string1 = '''
        <html>
        <link rel=stylesheet type=text/css href="{{ url_for('static', filename='style.css') }}">
        <h2><u>Educations</u></h2>
        
          {table}
  

        </html>
'''
        html_string2 = '''
        <html>
        <link rel=stylesheet type=text/css href="{{ url_for('static', filename='style.css') }}">
        <h2><u>Work Experiences</u></h2>
        
          {table}
  

        </html>
        '''



         # OUTPUT AN HTML FILE
        with open('Cv_output.html', 'w') as f:
            f.write(html_string.format(table=Details.to_html(classes='my_class').replace('<th>','<th style = "background-color: lightgreen" >').replace('<h2></h2>','<h2>Details</h2> ')+html_string1.format(table=Education.to_html(classes='my_class').replace('<th>','<th style = "background-color: lightgreen" >').replace('<h2>','<h2>Education Details'))+html_string2.format(table=Work_experience.to_html(classes='my_class').replace('<th>','<th style = "background-color: lightgreen" >').replace('\t',' ').replace('\n',''))))
            print("over")
        Javascript('''$('.my_class tbody tr').filter(':last').css('background-color', 'red');
                   ''')    
      
        return template('Cv_output.html')


                # datsets.to_html('Cv_output.html',header='Cv_parser_output')
        # return template('Cv_output.html')
      

        # This you can change it to whatever you want to get

        # Play with this

        # Use the .to_html() to get your table in html
        
      
        
        




@route('/')
def index():

    #refereshing the mulitple duration for the link
    #response = "<head><meta http-equiv='refresh' content='5'></head>"

     #database connection
     #   c.execute("select * from runstats")
     #  data = c.fetchall()

    picture_name = 'cv.jpg'
    return template('upload.html', picture=picture_name)
    
	
	
#engine = create_engine('mysql+mysqlconnector://temp_vscan:temp_vscan@192.168.202.24:3306/temp_vscan')
#runstats.to_sql(name='Runstats', con=engine, if_exists='append', index=False)



run(host='localhost', port=8080, debug=True)  


# from __future__ import unicode_literals
# from bottle import Bottle, request, response
# from mypkg import analyse_data


# # http://www.reddit.com/r/learnpython/comments/1037g5/whats_the_best_lightweight_web_framework_for/
# # http://bottlepy.org/docs/dev/tutorial.html
# app = Bottle()


# template = """<html>
# <head><title>Home</title></head>
# <body>
# <h1>Upload a file</h1>
# <form method="POST" enctype="multipart/form-data" action="/">
# <label>Level:</label> <input type="text" name="level" value="42"><br>
# <input type="file" name="uploadfile" /><br>
# <input type="submit" value="Submit" />
# </form>
# </body>
# </html>"""


# @app.get('/')
# def home():
#     return template


# @app.post('/')
# def upload():
#     # A file-like object open for reading.
#     upload_file = request.POST['uploadfile']
#     level = int(request.POST['level'])
    
#     # Your analyse_data function takes a file-like object and returns a new
#     # file-like object ready for reading.
#     converted_file = analyse_data(data=upload_file.file, level=level)
#     response.set_header('Content-Type', 'text/csv')
#     response.set_header('Content-Disposition', 'attachment; filename=converted.csv')
    
#     # Return a file-like object.
#     return converted_file


# if __name__ == "__main__":
#     app.run(debug=True)