.text                       # Seção de código (instruções)
.globl main                 # Declara o ponto de entrada global
main:
    addi x1, x0, 5          # x1 = 0 + 5 -> x1 recebe 5
    addi x2, x0, 7          # x2 = 0 + 7 -> x2 recebe 7
    add  x3, x1, x2         # x3 = x1 + x2 -> x3 recebe 12 (0x0C)
    # Saída limpa no RARS (ecall não pertence ao subconjunto do MiniRV)
    addi a7, x0, 10
    ecall
