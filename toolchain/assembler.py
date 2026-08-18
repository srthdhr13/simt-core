opcodes = {
    'ADD' :'00001',
    'MUL' : '00010',
    'MAD' : '00011',
    'MOV' : '00100',
    'MOVS' : '00101',
    'LD'  : '01000',
    'ST' : '01001',
    'CMP' : '10000',
    'BAR' :  '10001',
    'RET' : '10010'}


registers = {
    "R0" : "000",
    "R1" : "001",
    "R2" : "010",
    "R3" : "011",
    "R4" : "100",
    "R5" : "101",
    "R6" : "110",
    "R7" : "111",
}


specialregs = {
    "%tid" : "000",
    "%wid" : "001"
}

conditionmap = {
    'EQ' :'00',
    'NE' :'01',
    'LT' :'10',
    'GT' :'11',
}


file = open("/home/sruthidhar/projects/gpu2/updated_proj/program.asm" , "r") #add file path
output_file = open("/home/sruthidhar/projects/gpu2/updated_proj/program.hex" , "w") #add file path 


lineslist = []

for line in file:
    line = line.split("//")[0].strip()
    lineslist.append(line)

instlist = []

for inst in lineslist:
    if inst == "" :
        continue 
    else : 
        clean_list = inst.replace(',' , ' ')
        words = clean_list.split()
        instlist.append(words)


for i1 in instlist:
    if '.' in i1[0]:
        parts = i1[0].split('.')
        opcode = parts[0]
        modifier = parts[1]
    else : 
        opcode = i1[0]
        modifier = None 

    if opcode in opcodes:
        op = opcodes[opcode]

        if opcode in ['ADD' , 'MUL' , 'MAD' , 'MOV' , 'MOVS']:
            
            res = '00'

            if opcode in ['ADD' , 'MUL' , 'MAD']:
                rd = registers[i1[1]]
                rs1 = registers[i1[2]]
                rs2 = registers[i1[3]]
                binarystring = op +  rd + rs1 + rs2 + res 

            elif opcode == 'MOV' : 
                rd = registers[i1[1]]
                rs1 = registers[i1[2]]
                rs2 = '000'
                binarystring = op + rd + rs1 + rs2 + res 

            elif opcode == 'MOVS':
                rd = registers[i1[1]]
                rs1 = specialregs[i1[2]]
                rs2 = '000'
                binarystring = op + rd + rs1 + rs2 + res 

        elif opcode in ['LD' , 'ST']:
            unused = '0000'

            if modifier == 'shared':
                mem = '1'
            else : 
                mem = '0'

            if opcode == 'LD':
                datareg = registers[i1[1]]
                addrreg = registers[i1[2].strip('[]')]
                binarystring = op + mem + datareg + addrreg + unused

            elif opcode == 'ST':
                addrreg = registers[i1[1].strip('[]')]
                datareg = registers[i1[2]]
                binarystring = op + mem + datareg + addrreg + unused

        elif opcode in ['CMP' , 'BAR' , 'RET']:
            if opcode == 'CMP':
                cc = conditionmap[modifier]
                rd = registers[i1[1]]
                rs1 = registers[i1[2]]
                rs2 = registers[i1[3]]
                binarystring = op + cc + rd + rs1 + rs2

            elif opcode == 'BAR' :
                binarystring = op + ('0' * 11)

            elif opcode == 'RET':
                binarystring = op + ('0' * 11)
    

        hexstring = hex(int(binarystring , 2))[2:].zfill(4)
        print(opcode, binarystring, hexstring)
        output_file.write(hexstring + "\n")
        
    else:
        print(f"Unknown instruction: {opcode}")
        exit()
         

file.close()
output_file.close()
print("successful")
