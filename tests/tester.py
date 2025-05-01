import random
import pyseal
from src.matcher import EncryptedDNAMatcher

def run_dna_tests(num_tests=1000, match_ratio=0.8, verbose=True, save_failures=False):
    tester = EncryptedDNAMatcher()
    match_test_times = []
    no_match_test_times = []
    passes = 0
    failures = 0

    for test_num in range(1, num_tests + 1):
        is_match_case = random.random() < match_ratio
        k = random.randint(3, 6)
        true_pattern = [random.randint(0, 3) for _ in range(k)]
        L = random.randint(250, 1000)

        if is_match_case:
            test_sequence = [random.randint(0, 3) for _ in range(L - k)]
            while any(test_sequence[i:i + k] == true_pattern for i in range(len(test_sequence) - k + 1)):
                test_sequence = [random.randint(0, 3) for _ in range(L - k)]
            injection_index = random.randint(0, L - k)
            final_sequence = test_sequence[:injection_index] + true_pattern + test_sequence[injection_index:]
            expected_index = injection_index
        else:
            while True:
                final_sequence = [random.randint(0, 3) for _ in range(L)]
                if not any(final_sequence[i:i + k] == true_pattern for i in range(len(final_sequence) - k + 1)):
                    break
            expected_index = None

        tester.set_dna(final_sequence)
        tester.encrypt_dna_sequence()

        import time
        t0 = time.time()
        test_index = tester.search_for_pattern_batched(true_pattern)
        t1 = time.time()

        elapsed = t1 - t0
        if is_match_case:
            match_test_times.append(elapsed)
        else:
            no_match_test_times.append(elapsed)

        if test_index == expected_index:
            passes += 1
            if verbose:
                msg = f"✅ Test {test_num}: OK"
                msg += f". Match at {test_index}" if test_index is not None else ". No match detected."
                print(msg)
        else:
            failures += 1
            print(f"❌ Test {test_num}: FAIL. Found {test_index}, expected {expected_index}. Pattern: {true_pattern}")
            if save_failures:
                with open(f"failed_case_{test_num}.txt", "w") as f:
                    f.write(f"Pattern: {true_pattern}\n")
                    f.write(f"Expected: {expected_index}, Got: {test_index}\n")
                    f.write(f"DNA: {final_sequence}\n")

    print("\n✨ Test Summary:")
    print(f"Passed: {passes}, Failed: {failures}, Accuracy: {passes / num_tests:.2%}")

    if match_test_times:
        avg_match = sum(match_test_times) / len(match_test_times)
        print(f"Average Match Time: {avg_match * 1000:.2f} ms")
    if no_match_test_times:
        avg_nomatch = sum(no_match_test_times) / len(no_match_test_times)
        print(f"Average No-Match Time: {avg_nomatch * 1000:.2f} ms")
    if match_test_times or no_match_test_times:
        total = match_test_times + no_match_test_times
        print(f"Total Time: {sum(total):.2f} sec, Avg Per Test: {sum(total) / len(total) * 1000:.2f} ms")

if __name__ == "__main__":
    run_dna_tests()
