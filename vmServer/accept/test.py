import subprocess
p=subprocess.Popen(['powershell.exe',"execute\\action\\code\\action.ps1"],stdout=subprocess.PIPE)
out,err=p.communicate()
encoding = 'utf-8'
print(out.decode(encoding))
print(err.decode(encoding))
print("YOLO")