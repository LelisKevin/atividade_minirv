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
| Decodificador de instruções (spec do contrato) | combinacional | `minirv/decoder.py`, `minirv/isa.py` | 01, generalizado na 07 |
| Codificador de instruções | combinacional | `minirv/encoder.py` | 07 |
| Registradores, PC | sequencial | `minirv/registers.py`, `minirv/pc.py` | 01, 05 |
| ULA | combinacional | `minirv/alu.py` | 01, 05 |
| Memória de instruções / de dados | sequencial | `minirv/instruction_memory.py`, `minirv/data_memory.py` | 06 |
| Ciclo FETCH→WRITEBACK (instruções controladas) | controle | `minirv/executor.py` | 06 |
| CPU ADD/ADDI com trace por instrução | integração | `minirv/cpu.py` | 01 |
| Trace | observação | `minirv/trace.py` | 01 |

## O que ainda não existe

A CPU decodifica as 19 instruções do contrato, mas executa só `ADD` e `ADDI`; o executor da Semana 06 roda
apenas as três instruções controladas didáticas. O caminho de dados completo e o montador não fazem parte dos
documentos recebidos (ver `docs/checklist-final.md`).
