import re
from itertools import islice
PATTERN=re.compile(r'-?\d\.?\d*[Ee][+-]?\d+')


def getdata2(line,fin,n, data=None,pattern=PATTERN):            
   
    if data==None:
        data=list(pattern.findall(line))
    else:
        data=data   
    if n>1:
        lines=list(islice(fin, n-1))
        for l in lines:
            data.extend(pattern.findall(l))
            if len(pattern.findall(l))==0:
                temp_list=[float(i) for i in data]
                temp_list.append(l.strip())
                return temp_list        
    return [ float(i) for i in data]


def getdata(line, fin, n, data=None, pattern=PATTERN):
    # Initialize data list if not provided
    if data is None:
        data = list(pattern.findall(line))
    # Use 'else' to avoid redundant assignment
    else:
        data = data
    
    # Check if more lines need to be read
    if n > 1:
        # Read 'n-1' lines
        lines = [next(fin) for _ in range(n-1)]
        # Extend data with values from each line
        for l in lines:
            data.extend(pattern.findall(l))
            # Check if the line contains any valid data
            if not pattern.findall(l):
                # If no data found, convert and return the data list
                return [float(i) for i in data] + [l.strip()]
    # If no further lines need to be read, return the data list
    return [float(i) for i in data]



def printDataItem(TFEMmod:list[str], _item, _ini=0, _noRows=0,format=0):   
    _NoParts = len(_item)
    if format==0:
        for x in range(_ini, _NoParts):
            if _noRows == 4 and x <= _NoParts:
                TFEMmod.append("\n")
                TFEMmod.append("        ")
                _noRows = 0
            _number = _item[x]
            TFEMmod.append(f'  {_number:1.8E}')
            _noRows += 1
    if format==1:
        for x in range(_ini, _NoParts):
            if _noRows == 4 and x <= _NoParts:
                TFEMmod.append("\n")
                TFEMmod.append("        ")
                _noRows = 0
            _number = _item[x]
            if _number < 0:
                TFEMmod.append(f' {_number:1.8E}')
            else:
                TFEMmod.append(f'  {_number:1.8E}')
            _noRows += 1

def printDataItem_neg(TFEMmod:list[str], _item, _ini=0, _noRows=0,format=0):   
    _NoParts = len(_item)
    if format==0:
        for x in range(_ini, _NoParts):
            if _noRows == 4 and x <= _NoParts:
                TFEMmod.append("\n")
                TFEMmod.append("        ")
                _noRows = 0
            _number = _item[x]
            TFEMmod.append(f' {_number: 1.8E}')
            _noRows += 1
    if format==1:
        for x in range(_ini, _NoParts):
            if _noRows == 4 and x <= _NoParts:
                TFEMmod.append("\n")
                TFEMmod.append("        ")
                _noRows = 0
            _number = _item[x]
            if _number < 0:
                TFEMmod.append(f'{_number: 1.8E}')
            else:
                TFEMmod.append(f'  {_number:1.8E}')
            _noRows += 1







def append_lines_to_file(lines, file_path):
    """
    Append lines from a list to a text file.

    Args:
    - lines: A list of strings representing the lines to append.
    - file_path: Path to the text file.

    Returns:
    - None
    """
    try:
        with open(file_path, 'a', buffering=1192) as file:
            file.writelines(lines)
        
    except Exception as e:
        print("An error occurred:", str(e))