
import re
def compare(file1:str,file2:str,num:int)->bool:

    with open(file1, 'r') as file1, open(file2, 'r') as file2:
        for line_num, (line1, line2) in enumerate(zip(file1, file2), start=1):
            if line1 != line2:
                print(f"Difference found at line {line_num}:")
                print(f"File 1: {line1.strip()}")
                print(f"File 2: {line2.strip()}\n")
            if line_num>num:
                return

    
    print("Comparison completed.")



def compare2(file1:str, start1:int, file2:str, start2:int, num:int) -> bool:
    """
    Compare two text files line by line, starting from specified line numbers.
    
    Args:
        file1 (str): Path to the first text file.
        start1 (int): Line number in file1 to start comparison from.
        file2 (str): Path to the second text file.
        start2 (int): Line number in file2 to start comparison from.
        num (int): Number of lines to compare.
        
    Returns:
        bool: True if comparison completes successfully, False otherwise.
    """
    def normalize_scientific_notation(line):
        # Convert all scientific notation to lowercase to ensure equality
       
        return re.sub(r'(\d+\.\d+)[eE](\+\d+)', lambda x: f"{x.group(1).lower()}e{x.group(2)}", line)


    with open(file1, 'r') as file1, open(file2, 'r') as file2:
        # Skip lines until start1 and start2
        for _ in range(start1 - 1):
            next(file1)
        for _ in range(start2 - 1):
            next(file2)
        
        for line_num, (line1, line2) in enumerate(zip(file1, file2), start=max(start1, start2)):
            if normalize_scientific_notation(line1.strip()) != normalize_scientific_notation(line2.strip()):
                print(f"Difference found at line {line_num}:")
                print(f"File 1: {line1.strip()}")
                print(f"File 2: {line2.strip()}\n")
                print("stopp")
            if line_num >= max(start1 + num - 1, start2 + num - 1):
                print("Comparison completed.")
                return True
    print("Comparison completed.")
    return False

def compare3(file1:str, start1:int, file2:str, start2:int, num:int, output_file:str) -> bool:
    """
    Compare two text files line by line, starting from specified line numbers, and write the comparison results to a text file.

    Args:
        file1 (str): Path to the first text file.
        start1 (int): Line number in file1 to start comparison from.
        file2 (str): Path to the second text file.
        start2 (int): Line number in file2 to start comparison from.
        num (int): Number of lines to compare.
        output_file (str): Path to the output text file.

    Returns:
        bool: True if comparison completes successfully, False otherwise.
    """
    with open(file1, 'r') as f1, open(file2, 'r') as f2, open(output_file, 'w') as output:
        # Skip lines until start1 and start2
        for _ in range(start1 - 1):
            next(f1)
        for _ in range(start2 - 1):
            next(f2)

        for line_num, (line1, line2) in enumerate(zip(f1, f2), start=max(start1, start2)):
            if line1.strip() != line2.strip():
                output.write(f"Difference found at line {line_num}:\n")
                output.write(f"File 1: {line1.strip()}\n")
                output.write(f"File 2: {line2.strip()}\n\n")
            if line_num >= max(start1 + num - 1, start2 + num - 1):
                output.write("Comparison completed.\n")
                return True
    output.write("Comparison completed.\n")
    return False