# yara_scanner
Yara scanner that uses PsExec, CrowdResponse and native OS commands to scan remote hosts simultaneously. 

<p>I was looking for a tool that would scan multiple hosts at the same time using YARA. Every tool that I could find was either utilizing WMIC or over the network communication with a server listening to a specific port.</p>
<p>&nbsp;</p>
<p>This script allows you to scan multiple remote nodes using PsExec and native OS commands. CrowdResponse is used instead of simple YARA due to its reporting capabilities and the ability to scale as it has many features that can be turned on on-demand (just make sure that you edit the script).</p>
<p>&nbsp;</p>
<p>It goes without saying that you have to have rights and be able to run PsExec on remote hosts for this to work. The script will be copying the necessary file, run the command and checking every X minutes (5 minutes by default) to see if the command has finished running. When the command finishes, it copies the files XML files under the folder "results" inside the CrowdResponse directory (read steps below). As a final task, it runs&nbsp;CRConvert.exe to convert the XML files to HTML.</p>
<p>&nbsp;</p>
<h2>Installation</h2>
<p>You will need to follow the below instructions to avoid any errors:</p>
<ol>
<li>Download CrowdResponse (<a href="https://www.crowdstrike.com/wp-content/community-tools/CrowdResponse.zip">https://www.crowdstrike.com/wp-content/community-tools/CrowdResponse.zip</a>).</li>
<li>Extract CrowdResponse under "C:\" or anywhere else you like (Just make sure that you modify the variable at the start of the script).</li>
<li>Create a folder named results under the CrowdResponse directory from step 2.</li>
<li>Copy the PsExec.exe to be in the same directory as the yara_scanner.py.</li>
</ol>
<p>&nbsp;</p>
<h2>Arguments</h2>
<ul>
<li>-f, --file, [*] Specify the file that contains the target hosts/IPs.</li>
<li>-m, --pull,&nbsp; [*] Specify the pulling frequency(in minutes. Default = 5 mins).</li>
<li>-d, --directory, [*] Specify the directory to scan on the remote host(full path).</li>
<li>-y, --yara_files, [*] Specify the directory of the YARA rules (on local host) to use against the remote machines(full path).</li>
</ul>
