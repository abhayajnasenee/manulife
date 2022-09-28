import zipfile
import os
import csv
import shutil


def process(filename):
    """
    Extracts the input zip file.
    Traverse through all the csv file present inside the extracted folder and fetch the distinct source_ip.
    Fetch the enviroment value from the file name ,which is static for all the records for a file.
    Generate a combined csv file with two columns source_ip and environment.

    params : Input zip file name
    """

    try:
        #extracting the zip file to the target folder
        targetdirname = filename.replace('.zip','')
        print (f"file will be extracted to the folder {targetdirname}")

        with zipfile.ZipFile(filename,"r") as zip_ref:
            zip_ref.extractall(targetdirname)

        #traverse through target directory to fetch the source ip from the file
        
        consolidated_data = []

        for file in os.listdir(targetdirname):

            filenamewithpath = f"{targetdirname}/{file}"
            #forming the environment variable from the filename
            env_name = ' '.join([i for i in file.replace('.csv', '').split(' ') if i.isalpha()])
            print (f"envionment name  is {env_name} for the file {file}")
            with open (filenamewithpath, 'r') as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)
                iplst = list(set([row[0] for row in data[1:]]))
                finaldata = [ [ip,env_name] for ip in iplst ]
                consolidated_data.extend(finaldata)

        #writing to "combined.csv"  file 
        with open ('Combined.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            header = ['Source IP', 'Environment']
            writer.writerow(header)
            writer.writerows(consolidated_data)

        #removing the extracted directory
        shutil.rmtree(targetdirname)

    except Exception as e:
        print (f"Failure With Error :{str(e)}")

if __name__ == "__main__":

    zipfilename = 'Samplecsvfile.zip'
    process(zipfilename)
