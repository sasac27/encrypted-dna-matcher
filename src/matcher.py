# --- src/encrypted_dna_matcher.py ---
import random
import pyseal  # Custom wrapper you built

class EncryptedDNAMatcher:
    def __init__(self):
        self.session = pyseal.PySEALEnvironment()
        self.current_dna_sequence = None
        self.encrypted_dna_sequence = None
        self.current_dna_sequence_length = None
        self.mask_cache = {}  # pattern length -> mask vector

        self.running = True

    def generate_random_dna(self, length=None):
        if length is None:
            length = int(input("Enter length of sequence: "))
        self.current_dna_sequence = [random.randint(0, 3) for _ in range(length)]
        self.current_dna_sequence_length = length

    def encrypt_dna_sequence(self):
        if self.current_dna_sequence is None:
            print("No DNA sequence generated.")
            return
        self.encrypted_dna_sequence = self.session.encrypt_vector(self.current_dna_sequence)
        print("DNA sequence encrypted.")

    def _get_mask(self, pattern_len):
        if pattern_len not in self.mask_cache:
            full_mask = [1.0] * pattern_len + [0.0] * (self.current_dna_sequence_length - pattern_len)
            self.mask_cache[pattern_len] = full_mask
        return self.mask_cache[pattern_len]

    def search_for_pattern(self, pattern):
        pattern_len = len(pattern)
        mask = self._get_mask(pattern_len)
        for i in range(self.current_dna_sequence_length - pattern_len + 1):
            rotated = self.session.rotate_vector(self.encrypted_dna_sequence, i)
            masked = self.session.mask_vector(rotated, mask)
            decrypted = self.session.decrypt_vector(masked)[:pattern_len]
            diff = [a - b for a, b in zip(decrypted, pattern)]
            if sum(d**2 for d in diff) < 0.05:
                return i
        return None

    def search_for_pattern_batched(self, pattern, batch_size=8):
        pattern_len = len(pattern)
        mask = self._get_mask(pattern_len)
        max_start = self.current_dna_sequence_length - pattern_len + 1

        for batch_start in range(0, max_start, batch_size):
            rotated_vectors = []
            masked_vectors = []
            window_indices = range(batch_start, min(batch_start + batch_size, max_start))

            for idx in window_indices:
                rotated = self.session.rotate_vector(self.encrypted_dna_sequence, idx)
                masked = self.session.mask_vector(rotated, mask)
                rotated_vectors.append(rotated)
                masked_vectors.append(masked)

            for masked_vec, idx in zip(masked_vectors, window_indices):
                decrypted = self.session.decrypt_vector(masked_vec)[:pattern_len]
                diff = [a - b for a, b in zip(decrypted, pattern)]
                if sum(d**2 for d in diff) < 0.05:
                    return idx

        return None

    def exit_program(self):
        print("Exiting...")
        self.running = False
