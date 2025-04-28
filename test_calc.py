import tenseal as ts


stored_numbers = {}
id = 0
running = True

context = ts.context(
    ts.SCHEME_TYPE.CKKS, #Encryption scheme
    poly_modulus_degree=8192, #Polynomial modulus degree (standard)
    coeff_mod_bit_sizes=[60, 40, 40, 60] #Size of modulus chain
)
context.global_scale = 2**40
context.generate_galois_keys()

while running:
    print("Menu \n1) Encrypt \n2) Add \n3) Multiply \n4) Decrypt \n5) Exit")
    choice = input("Choose an option: ")

    if choice == "1":
        enc_num = ts.ckks_vector(context, [float(input("Enter a number: "))])
        stored_numbers[id] = enc_num
        id += 1
        pass
    elif choice == "2":
        print("Available IDs: ", stored_numbers.keys())
        id1, id2 = map(int, input("Enter 2 IDs: ").split())
        num1, num2 = stored_numbers[id1], stored_numbers[id2]
        sum = num1 + num2
        stored_numbers[id] = sum
        print(f"Stored result as ID {id}")
        id += 1
        pass 
    elif choice == "3":
        print("Available IDs: ", stored_numbers.keys())
        id1, id2 = map(int, input("Enter 2 IDs: ").split())
        num1, num2 = stored_numbers[id1], stored_numbers[id2]
        product = num1 * num2
        stored_numbers[id] = product
        print(f"Stored result as ID {id}")
        id += 1        
        pass 
    elif choice == "4":
        print("Available IDs: ", stored_numbers.keys())
        chosen_id = int(input("Enter an ID to decrypt: "))
        dec_num = stored_numbers[chosen_id].decrypt()
        print(f"Decrypted result: {dec_num}")
        pass
    elif choice == "5":
        running = False
    else:
        print("Invalid choice. Try again")

