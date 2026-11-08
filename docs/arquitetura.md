# Arquitetura do MiniRV

Fluxo: programa hexadecimal → memória de instruções → PC → decodificador →
registradores/ULA → memória de dados → trace.

```mermaid
flowchart LR
    HEX[programa .hex] --> IMEM[Memória de instruções]
    PC[PC] -->|endereço| IMEM
    IMEM -->|palavra 32 bits| DEC[Decodificador]
    DEC -->|rs1, rs2, rd, imm| REG[Registradores x0-x31]
    REG -->|operandos| ALU[ULA]
    DEC -->|imm| ALU
    ALU -->|resultado| REG
    ALU -->|endereço| DMEM[Memória de dados]
    REG -->|valor de STORE| DMEM
    DMEM -->|valor de LOAD| REG
    DEC -. eventos .-> TRACE[(Trace JSON)]
    REG -. eventos .-> TRACE
    PC -. eventos .-> TRACE
```

Estado atual (Semana 01): memória de instruções e de dados ainda não existem como
módulos próprios; a CPU mantém a lista de palavras do programa e o PC internamente.
A memória de dados é prevista para a Semana 06. Os blocos que ainda não existem estão
no diagrama porque fazem parte da arquitetura-alvo.
