import tenseal as ts

context = ts.context(
    ts.SCHEME_TYPE.CKKS, #Encryption scheme
    poly_modulus_degree=8192, #Polynomial modulus degree (standard)
    coeff_mod_bit_sizes=[60, 40, 40 , 60] #Size of modulus chain
)
context.global_scale = 2**40
context.generate_galois_keys()

#Encrypt
num = float((input("Enter a number; ")))  #Wrapped a list since CKKS works on vectors
num_list = [num]
encrypted_num = ts.ckks_vector(context, num_list)

#Decrypt
decrypted_number = encrypted_num.decrypt()

print("Decrypted result: ", decrypted_number)