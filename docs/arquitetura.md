# Arquitetura do MiniRV

Fluxo: programa hexadecimal → memória de instruções → PC → decodificador → registradores/ULA →
memória de dados → trace.

```mermaid
flowchart LR
    HEX[programa .hex] --> IMEM[Memória de instruções]
    PC[PC] -->|endereço| IMEM
    IMEM -->|palavra 32 bits| DEC[Decodificador]
    DEC -->|opcode| CTRL[Controle por classe]
    CTRL -. RegWrite, ALUSrc, MemRead, MemWrite, Branch .-> REG
    DEC -->|rs1, rs2, rd| REG[Registradores x0-x31]
    REG -->|operandos| MUX{{MUX ALUSrc}}
    DEC -->|imm| MUX
    MUX --> ALU[ULA]
    REG -->|operando A| ALU
    ALU -->|resultado| REG
    ALU -->|endereço| DMEM[Memória de dados]
    REG -->|valor de STORE| DMEM
    DMEM -->|valor de LOAD| REG
    DEC -. eventos .-> TRACE[(Trace JSON)]
    REG -. eventos .-> TRACE
    PC -. eventos .-> TRACE

    classDef comb fill:#d6ecff,stroke:#2b6cb0,color:#000;
    classDef seq fill:#ffe9c7,stroke:#b7791f,color:#000;
    class DEC,CTRL,MUX,ALU comb;
    class PC,REG,IMEM,DMEM seq;
```

**Legenda:** azul = bloco **combinacional** (a saída depende só das entradas atuais: decodificador,
controle, MUX e ULA); laranja = bloco com **estado** (PC, registradores e memórias).

## Mapa bloco → módulo

| Bloco | Tipo | Módulo | Semana |
| --- | --- | --- | --- |
| Palavra de 32 bits | — | `minirv/word32.py` | 03 |
| Portas, MUX, decoder 2→4, controle por classe | combinacional | `minirv/combinacional/` | 04 |
| Decodificador de instruções | combinacional | `minirv/decoder.py` | 01 (generalizado na 07) |
| Registradores, PC | sequencial | `minirv/registers.py`, `minirv/pc.py` | 01, 05 |
| ULA | combinacional | `minirv/alu.py` | 01, 05 |
| Memórias de instruções e de dados | sequencial | a criar (Semana 06) | 06 |
| Trace | observação | `minirv/trace.py` | 01 |

Estado atual: o PC e a lista de palavras do programa ainda ficam dentro de `cpu.py` e o módulo `pc.py` e as
memórias ainda não existem; eles entram nas Semanas 05 e 06. O diagrama mostra a arquitetura-alvo.
