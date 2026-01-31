# IMPORTS
from os.path import abspath

def addVoidHosts(current_host :str):
    
    file_target = r"c:\windows\system32\drivers\etc\hosts"
    data = abspath(r'Script\System\Hosts\hosts.data')

    data_content = ''
    try:
        with open(data, 'r') as f:
            data_content = f.read()
            f.close()
    except PermissionError as e:
        print(e)
    
    current_host_lines = current_host.splitlines()

    for line in data_content.splitlines():
        new_line = f'127.0.0.1\t{line}'
        if new_line not in current_host_lines:
            current_host_lines.append(new_line)
    
    response = ''
    for line in current_host_lines:
        response += f'{line}\n'
    response = response.rstrip('\n') 
    
    try:
        with open(file_target, 'w') as f:
            f.write(response)
            f.close()
    except PermissionError as e:
        print(e)

def script():
    file_target = r"c:\windows\system32\drivers\etc\hosts"
    content = ""
    try:
        with open(file_target, "r") as f:
            content = f.read()
            f.close()
    except PermissionError as e:
        print(e)

    response = ""

    try:
        for line in content.splitlines():
            if not line.startswith("#"):
                response += line 
                response += "\n"
    except PermissionError as e:
        print(e)

    addVoidHosts(response)
    

    with open(file_target, "a") as f:
        f.write(response)
        f.close()
