menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[u] Novo Usuário
[c] Nova Conta
[l] Listar Contas
[q] Sair
=> """

AGENCIA = "0001"
usuarios = []
contas = []
NOTAS_VALIDAS = [200, 100, 50, 20, 10, 5, 2]

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
    elif not pode_sacar_com_notas(valor):
        print("Operação falhou! O valor não pode ser sacado com notas disponíveis (2, 5, 10, 20, 50, 100, 200).")
    else:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    return saldo, extrato, numero_saques

def pode_sacar_com_notas(valor):
    restante = int(valor)
    for nota in NOTAS_VALIDAS:
        qtd, restante = divmod(restante, nota)
    return restante == 0

def exibir_extrato(saldo, /, *, extrato):
    print("\n========== EXTRATO ==========")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("=============================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ").strip()
    cpf = "".join(filter(str.isdigit, cpf))
    if filtrar_usuario(cpf, usuarios):
        print("Já existe usuário com esse CPF!")
        return
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro - bairro - cidade/sigla estado): ")
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ").strip()
    cpf = "".join(filter(str.isdigit, cpf))
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
        print(f"Conta criada com sucesso! Número da conta: {numero_conta}")
        return conta
    else:
        print("Usuário não encontrado, fluxo de criação de conta encerrado.")
        return None

def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    for conta in contas:
        linha = f"""
Agência:\t{conta['agencia']}
Conta:\t\t{conta['numero_conta']}
Titular:\t{conta['usuario']['nome']}
CPF:\t\t{conta['usuario']['cpf']}
"""
        print(linha)

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    numero_conta = 1
    while True:
        opcao = input(menu)
        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)
        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)
        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)
        elif opcao == "u":
            criar_usuario(usuarios)
        elif opcao == "c":
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
                numero_conta += 1
        elif opcao == "l":
            listar_contas(contas)
        elif opcao == "q":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()