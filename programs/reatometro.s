# Reatometro RISC-V (MiniRV RV32I reduzido)
# MMIO: entrada 0x80000000, sinal 0x80000004, ciclos 0x80000008.

.text
.globl main

main:
    lui  x10, 0x80000
    addi x11, x10, 4
    addi x12, x10, 8

AGUARDA_SINAL:
    lw   x1, 0(x11)
    beq  x1, x0, AGUARDA_SINAL
    addi x3, x0, 0

LOOP_REACAO:
    addi x3, x3, 1
    lw   x1, 0(x10)
    beq  x1, x0, LOOP_REACAO
    sw   x3, 0(x12)

FIM:
    jal  x0, FIM
