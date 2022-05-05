### By Pedro Lucero, 2022 ###
### Small Code to translate between numeric systems ###
# Can do binary, octal, decimal and hexadecimal
# Format is: num,current_system,desired_system
# Example: 10,BIN,DEC should return "2"

hex_values = {"A":"10", "B":"11", "C":"12", "D":"13", "E":"14", "F":"15"}
bases = {"BIN":2, "OCT":8, "DEC":10, "HEX":16}

def get_input(prompt):
    
    while True:
        response = input(prompt)
        if response.isnumeric():        
            break
        print("\n\tRespuesta inválida\n")
    return response

def from_decimal(in_num, f_base):
    in_num = int(in_num)
    result_digit = str(in_num%f_base)
    
    if int(result_digit) > 9:
        result_digit = [key for key, value in hex_values.items() if value == result_digit][0]
     
    if in_num//f_base == 0:
        return result_digit

    return from_decimal(in_num//f_base, f_base) + result_digit


def to_decimal(in_num, o_base):
    result = 0
    o_base = bases[o_base]
    
        
    for exp, digit in enumerate(in_num[::-1]):
        if not digit.isnumeric(): # Should only run if number is HEX
            digit = hex_values[digit]
            
        result += int(digit)*(o_base**exp)
    
    return str(result)
    
    
def main_loop():
    result = ""
    
    entry = input("\nNúmero,Sistema_original,Sistema_final:\n>>>")
    entry = entry.split(",")
    
    if "DEC" not in [entry[1],entry[2]]:
        result = to_decimal(entry[0], entry[1])
        result = from_decimal(result, bases[entry[2]])
        print(f"\n\tResultado: {result}")
        
    elif entry[1] == "DEC":
        result = from_decimal(entry[0], bases[entry[2]])
        print(f"\n Resultado: {result}")
        
    elif entry[2] == "DEC":
        result = to_decimal(entry[0], entry[1])
        print(f"\n Resultado: {result}")

if __name__ == "__main__":
    
    while True:
    
        main_loop()
        if not input("Repetir? (Y/N)").capitalize() == "Y":
            break
    
    print("\tFinalizado")
    
