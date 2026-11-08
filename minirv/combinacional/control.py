"""Controle por classe de opcode (didático, Semana 04).

1 = ativar/usar; 0 = não ativar. ALUSrc: 0 seleciona registrador, 1 seleciona imediato.
O opcode identifica só a classe; ADD/SUB/AND/OR dentro da classe R são distinguidos por funct3/funct7
(Semana 07).
"""

OPCODE_R = 0b0110011
OPCODE_I = 0b0010011
OPCODE_LOAD = 0b0000011
OPCODE_STORE = 0b0100011
OPCODE_BRANCH = 0b1100011

_CONTROLES = {
    OPCODE_R:      {"classe": "R",      "RegWrite": 1, "ALUSrc": 0, "MemRead": 0, "MemWrite": 0, "Branch": 0},
    OPCODE_I:      {"classe": "I",      "RegWrite": 1, "ALUSrc": 1, "MemRead": 0, "MemWrite": 0, "Branch": 0},
    OPCODE_LOAD:   {"classe": "LOAD",   "RegWrite": 1, "ALUSrc": 1, "MemRead": 1, "MemWrite": 0, "Branch": 0},
    OPCODE_STORE:  {"classe": "STORE",  "RegWrite": 0, "ALUSrc": 1, "MemRead": 0, "MemWrite": 1, "Branch": 0},
    OPCODE_BRANCH: {"classe": "BRANCH", "RegWrite": 0, "ALUSrc": 0, "MemRead": 0, "MemWrite": 0, "Branch": 1},
}


def decode_control(opcode):
    if type(opcode) is not int:
        raise ValueError(f"Opcode deve ser inteiro: {opcode!r}")
    if opcode not in _CONTROLES:
        raise ValueError(f"Opcode não suportado: {opcode:07b}")
    return dict(_CONTROLES[opcode])  # cópia: quem chama não altera a tabela
