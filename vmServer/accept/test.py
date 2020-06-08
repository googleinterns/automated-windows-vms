import subprocess
p=subprocess.Popen(['powershell.exe',"execute\\action\\code\\action.ps1"],stdout=subprocess.PIPE)
out,err=p.communicate()
print(out)
print(err)
print("YOLO")