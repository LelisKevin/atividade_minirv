# Diagrama do ciclo de instrução (Semana 06)

Fonte editável em texto (Mermaid), versionada junto; o GitHub a renderiza como imagem.
Os cinco estados são uma decomposição didática, **não um pipeline**.

```mermaid
flowchart LR
    PC[PC] -->|endereço 32b| IMEM[Memória de instruções]
    IMEM -->|palavra 32b| CTRL[Controle / decodificação]
    CTRL -. RegWrite .-> REG[Registradores]
    CTRL -. ALUSrc .-> MUX{{MUX}}
    CTRL -. MemRead / MemWrite .-> DMEM[Memória de dados]
    REG -->|operando A| ALU[ULA]
    REG -->|operando B| MUX
    CTRL -->|imediato| MUX
    MUX --> ALU
    ALU -->|resultado| REG
    ALU -->|endereço efetivo| DMEM
    REG -->|valor de STORE| DMEM
    DMEM -->|valor de LOAD| REG
    REG -. WRITEBACK: PC + 4 .-> PC
```

```mermaid
stateDiagram-v2
    [*] --> FETCH
    FETCH --> DECODE: palavra lida
    DECODE --> EXECUTE: sinais e operandos
    EXECUTE --> MEMORY: resultado / endereço
    MEMORY --> WRITEBACK: dado (se houver)
    WRITEBACK --> FETCH: PC ← PC + 4
    WRITEBACK --> [*]: PC fora da memória de instruções
```

Setas contínuas = endereço e dados; tracejadas = sinais de controle.
