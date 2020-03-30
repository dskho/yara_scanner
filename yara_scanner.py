import subprocess
import argparse
import time

crowdresponseEXE = "C:\\temp\\CrowdResponse.exe"       # Specify the directory of the CrowdResponse executable. **Make sure that you have rights to the folder.
crowdresponseDIR = "C:\\CrowdResponse"
targets = []


def args():
    global file
    global pull
    global directory
    global yara_files
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file", help="[*] Specify the file that contains the target hosts/IPs",required=True)
    parser.add_argument("-m","--pull", help="[*] Specify the pulling frequency(in minutes)",required=False)
    parser.add_argument("-d","--directory", help="[*] Specify the directory to scan on the remote machine(full path)",required=False)   
    parser.add_argument("-y","--yara_files", help="[*] Specify the directory of the yara rules to use against the remote machines(full path)",required=False)
    args = parser.parse_args()
    file = args.file
    pull = args.pull
    directory = args.directory
    yara_files = args.yara_files

args()

def validation(list_1,list_2):                      # This function will be used below to validate if the done list contains all the targets before exits
    return sorted(list_1) == sorted(list_2)

    
with open(file,"r+") as f:      # remove new line from targets after reading from file 
    print("[*] Checking if all targets are alive")
    for i in f:                 #
        x = i.strip("\n")
        targets.append(x)
        task = subprocess.run(f"""psexec.exe -n 3 \\\\{x} ipconfig""",capture_output=True).stdout.decode('utf-8')
        if len(task) <= 200:
            targets.remove(x)
            print(f"    - Removing {x} as it appears offline")
    

if yara_files[-1] == "\\":      # Input validation to avoid errors
    yara_files = yara_files[:-1:]
    
print("\n[+] Copying CrowdResponse on the remote hosts\n")
for x in targets:
    subprocess.run(f"""xcopy {crowdresponseEXE} \\\\{x}\\c$\\Temp\\ /Y""",capture_output=True).stdout.decode('utf-8')     # Copy CrowdResponse on remote machines under C:\Temp
    subprocess.run(f"""xcopy {yara_files}\*.yar \\\\{x}\\c$\\Temp\\ /Y""",capture_output=True).stdout.decode('utf-8')     # Copy CrowdResponse on remote machines under C:\Temp

    
  
        
print("[+] Running CrowdResponse on remote hosts\n")
for x in targets:
    task = subprocess.run(f"""psexec.exe \\\\{x} -d cmd /c "{crowdresponseEXE} @Yara -t {directory} -v -h -s -y C:\\Temp\\ > C:\\temp\\{x}_yara.xml" """,capture_output=True).stdout.decode('utf-8')     # Run psexec command and output results on xml file.





if pull:
    pull = int(pull) * 60  # Converting it to seconds
else:
    pull = 300  # 5 minutes (or 300 seconds)
done = [] 
num = pull // 60     # To get the time in minutes 
while True:   
    for x in targets:
        if x in done:
            continue        
        task = subprocess.run(f"""psexec.exe \\\\{x} tasklist /FI "IMAGENAME eq CrowdResponse*" """,capture_output=True).stdout.decode('utf-8')     # Dirty way to check if CrowdResponse is still running on remote machine
        if "no tasks are running" in task.lower():
            subprocess.run(f"""xcopy \\\\{x}\\c$\\Temp\\{x}_yara.xml {crowdresponseDIR}\\results /Y""",shell=True,capture_output=True).stdout.decode('utf-8')    # If it is not running, assume that the job is finished and try to copy the files that have been generated
            subprocess.run(f"""del \\\\{x}\\c$\\temp\\* /Q""",shell=True,capture_output=True).stdout.decode('utf-8')    # Then delete the files on the remote host
            print(f"    + Remote host {x} is done!")
            done.append(x)      # Add the host to the "Done" list
            
        elif "crowdresponse" in task.lower():
            print("" + f"- {x} is still running")     # Output that the job is still running
            
    if validation(done,targets) == True:
        print("\nAll done!")
        break
    else:
        time.sleep(pull)
        print(f"{num} minute(s) passed\n\n")        
        num = num + (pull // 60) # Add aditionall time to the counter
        
subprocess.run(f"""{crowdresponseDIR}\\CRConvert.exe -f {crowdresponseDIR}\\results\\* -h -o {crowdresponseDIR}\\results\\""",capture_output=True).stdout.decode('utf-8')      # Convert XML in HTML
