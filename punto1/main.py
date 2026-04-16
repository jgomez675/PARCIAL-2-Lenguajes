from interpreter import Interpreter

def main():
    interpreter = Interpreter()

    print("=" * 50)
    print("   SISTEMA CRUD NoSQL - INTÉRPRETE")
    print("=" * 50)

    while True:
        command = input(">> ")

        if command.upper() == "EXIT":
            break

        result = interpreter.execute(command)

        print("\nRESULTADO:")
        print(result)
        print("-" * 50)

if __name__ == "__main__":
    main()
