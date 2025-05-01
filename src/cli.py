# --- src/cli.py ---
from matcher import EncryptedDNAMatcher

COMMANDS = {
    "1": "generate_random_dna",
    "2": "encrypt_dna_sequence",
    "3": "interactive_search",
    "5": "exit_program"
}

def interactive_search(matcher):
    pattern = list(map(int, input("Enter a pattern (e.g., 0 1 2): ").split()))
    idx = matcher.search_for_pattern_batched(pattern)
    if idx is not None:
        print(f"✅ Match found at position {idx}")
    else:
        print("❌ No match found.")

def run():
    matcher = EncryptedDNAMatcher()
    matcher.running = True

    while matcher.running:
        print("\nMenu:\n1) Generate DNA sequence\n2) Encrypt\n3) Search Pattern\n5) Exit")
        choice = input("Choose an option: ")
        command_name = COMMANDS.get(choice)
        if command_name:
            if command_name == "interactive_search":
                interactive_search(matcher)
            else:
                getattr(matcher, command_name)()
        else:
            print("Invalid choice")

if __name__ == "__main__":
    run()
