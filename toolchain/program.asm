



MOVS R0, %tid          
MOVS R1, %wid           

ADD  R5, R0, R2         
LD.global R6, [R5]      

ADD  R5, R0, R3         
LD.global R7, [R5]      

MUL  R5, R6, R7         
MAD  R5, R6, R7         
MOV  R6, R5             

ADD  R5, R0, R4         
ST.shared [R5], R6      

BAR                    


LD.shared R5, [R1]      
CMP.GT R7, R6, R5
CMP.LT R7, R6, R5
CMP.EQ R7, R6, R5
CMP.NE R7, R6, R5

BAR                     

ADD R5, R0, R2
ST.global [R5], R6      
RET
