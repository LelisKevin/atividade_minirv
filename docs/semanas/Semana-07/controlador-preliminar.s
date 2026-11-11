# Controlador térmico — programa preliminar (Semana 07)
# NÃO é aceito por um montador completo (isso é da Semana 08); usa apenas as 19 instruções do contrato v1
# (docs/isa/rv32i-subset-v1.md) e a sintaxe da seção 4 dele.
#
# HISTÓRICO SUPERADO: este programa usa o mapa preliminar 0xFFFF0000, incompatível com o mapa MMIO atual
# (0x80000000, 0x80000004 e 0x80000008). Mantido como evidência da Semana 07; não representa a configuração vigente.
# Mapa preliminar de E/S mapeada em memória:
#   base + 0  : leitura da amostra de temperatura (°C, inteiro)
#   base + 4  : atuador   (1 = ligado, 0 = desligado)
#   base + 8  : alarme    (1 = ativo,  0 = inativo)
#   base + 12 : índice da amostra atual (a E/S incrementa a cada ciclo)
#
# Registradores:
#   x10 base da E/S        x11 amostra            x12 estado do atuador (preservado entre iterações)
#   x13 alarme             x14 índice             x15 limite alto (liga)     x16 limite baixo (desliga)
#   x17 limite de alarme   x18 total de amostras  x20 constante 1
#
# Regra (histerese): amostra >= alto -> liga; amostra <= baixo -> desliga; entre os dois -> mantém o estado.
#                    amostra >= limite de alarme -> alarme ativo.

        LUI   x10, 0xFFFF0        # base da E/S mapeada = 0xFFFF0000
        ADDI  x15, x0, 30         # limite alto: liga o atuador
        ADDI  x16, x0, 26         # limite baixo: desliga o atuador
        ADDI  x17, x0, 40         # limite de alarme
        ADDI  x18, x0, 100        # total de amostras
        ADDI  x20, x0, 1          # constante 1
        ADDI  x12, x0, 0          # estado inicial: atuador desligado

loop:
        LW    x11, 0(x10)         # LEITURA: ler amostra
        SLT   x13, x11, x17       # x13 = 1 se amostra < limite de alarme
        XOR   x13, x13, x20       # inverte: x13 = 1 se amostra >= limite de alarme (alarme)
        BLT   x11, x15, abaixo    # DECISÃO: amostra < limite alto ?
        ADDI  x12, x0, 1          # ESTADO: amostra >= alto -> atuador ligado
        JAL   x0, escreve
abaixo:
        BLT   x16, x11, escreve   # baixo < amostra < alto -> mantém o estado (x12 não muda)
        ADDI  x12, x0, 0          # ESTADO: amostra <= baixo -> atuador desligado
escreve:
        SW    x12, 4(x10)         # ESCRITA: atuador
        SW    x13, 8(x10)         # ESCRITA: alarme
        LW    x14, 12(x10)        # ler índice
        BLT   x14, x18, loop      # LAÇO: índice < total ? repete
fim:
        JAL   x0, fim             # fim: laço infinito
