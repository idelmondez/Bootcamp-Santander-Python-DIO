import textwrap
NOTAS_VALIDAS = [200, 100, 50, 20, 10, 5, 2]

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = "".join(filter(str.isdigit, cpf))
        self.endereco = endereco

class Conta:
    AGENCIA_PADRAO = "0001"

    def __init__(self, usuario, numero_conta):
        self.agencia = Conta.AGENCIA_PADRAO
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0
        self.extrato = ""
        self.numero_saques = 0
        self.limite_saques = 3
        self.limite_saque = 500

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito:\tR$ {valor:.2f}\n"
            print("Depósito realizado com sucesso!")
        else:
            print("Operação falhou! Valor inválido.")

    def pode_sacar_com_notas(self, valor):
        restante = int(valor)
        for nota in NOTAS_VALIDAS:
            qtd, restante = divmod(restante, nota)
        return restante == 0

    def sacar(self, valor):
        if valor <= 0:
            print("Operação falhou! Valor inválido.")
        elif valor > self.saldo:
            print("Operação falhou! Saldo insuficiente.")
        elif valor > self.limite_saque:
            print("Operação falhou! Valor do saque excede limite.")
        elif self.numero_saques >= self.limite_saques:
            print("Operação falhou! Número máximo de saques excedido.")
        elif not self.pode_sacar_com_notas(valor):
            print("Operação falhou! Valor não disponível em notas válidas (2,5,10,20,50,100,200).")
        else:
            self.saldo -= valor
            self.extrato += f"Saque:\t\tR$ {valor:.2f}\n"
            self.numero_saques += 1
            print("Saque realizado com sucesso!")

    def exibir_extrato(self):
        print("\n========== EXTRATO ==========")
        print("Não foram realizadas movimentações." if not self.extrato else self.extrato)
        print(f"\nSaldo:\t\tR$ {self.saldo:.2f}")
        print("=============================")


class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []
        self.proximo_numero_conta = 1

    def criar_usuario(self):
        cpf = input("Informe o CPF (somente números): ").strip()
        if self.filtrar_usuario(cpf):
            print("Já existe usuário com esse CPF!")
            return
        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro - bairro - cidade/sigla estado): ")
        usuario = Usuario(nome, data_nascimento, cpf, endereco)
        self.usuarios.append(usuario)
        print("Usuário criado com sucesso!")

    def filtrar_usuario(self, cpf):
        cpf = "".join(filter(str.isdigit, cpf))
        for usuario in self.usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None

    def criar_conta(self):
        cpf = input("Informe o CPF do usuário: ").strip()
        usuario = self.filtrar_usuario(cpf)
        if not usuario:
            print("Usuário não encontrado. Criação de conta encerrada.")
            return
        conta = Conta(usuario, self.proximo_numero_conta)
        self.contas.append(conta)
        self.proximo_numero_conta += 1
        print(f"Conta criada com sucesso! Número da conta: {conta.numero_conta}")

    def listar_contas(self):
        if not self.contas:
            print("Nenhuma conta cadastrada.")
            return
        for conta in self.contas:
            linha = f"""
Agência:\t{conta.agencia}
C/C:\t\t{conta.numero_conta}
Titular:\t{conta.usuario.nome}
CPF:\t\t{conta.usuario.cpf}
"""
            print(textwrap.dedent(linha))
            print("=" * 50)

def main():
    banco = Banco()
    while True:
        opcao = input("""
[d] Depositar
[s] Sacar
[e] Extrato
[u] Novo Usuário
[c] Nova Conta
[l] Listar Contas
[q] Sair
=> """).strip()
        if opcao == "d":
            numero = int(input("Informe o número da conta: "))
            conta = next((c for c in banco.contas if c.numero_conta == numero), None)
            if conta:
                valor = float(input("Informe o valor do depósito: "))
                conta.depositar(valor)
            else:
                print("Conta não encontrada.")
        elif opcao == "s":
            numero = int(input("Informe o número da conta: "))
            conta = next((c for c in banco.contas if c.numero_conta == numero), None)
            if conta:
                valor = float(input("Informe o valor do saque: "))
                conta.sacar(valor)
            else:
                print("Conta não encontrada.")
        elif opcao == "e":
            numero = int(input("Informe o número da conta: "))
            conta = next((c for c in banco.contas if c.numero_conta == numero), None)
            if conta:
                conta.exibir_extrato()
            else:
                print("Conta não encontrada.")
        elif opcao == "u":
            banco.criar_usuario()
        elif opcao == "c":
            banco.criar_conta()
        elif opcao == "l":
            banco.listar_contas()
        elif opcao == "q":
            break
        else:
            print("Opção inválida. Selecione novamente.")

main()