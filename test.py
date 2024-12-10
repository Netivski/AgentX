from dataclasses import dataclass, field
import random

def soma(a: int, b: int) -> int:
    return int(a)+int(b)

def soma(a: str) -> int:
    return 10

def getInt() -> int:
    return random.randint(10, 20)

@dataclass
class Pessoa:
    nome: str
    idade: int
    turma: str
    num: int

    def defineNum(self, num: int):
        self.num = num

@dataclass
class Estudante(Pessoa):
    nota: int

    def defineNota(self, nota: int):
        self.nota = nota


@dataclass
class Professor(Pessoa):
    grau: str
    


e = Estudante("Zé", 18, "A", 23, -1)
e.defineNota(3)
e.defineNum(21)

p = Professor("Quim", 67, "Z", 31, "I")
p.defineNum(45)

q = Pessoa("Maria", 45, "F", 21)
q.defineNum(52)

print(isinstance(q, Estudante))
print(isinstance(q, Professor))
print(isinstance(q, Pessoa))