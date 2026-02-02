from utxo_manager import UTXOManager
from transaction import Transaction
from mempool import Mempool
from block import mine_block, Block
from blockchain import Blockchain

# Helper printing functions

def print_test_details(test_name, tx, expected_accept, actual_result):
    success, message = actual_result

    print(f"\n{test_name}")
    print("-" * len(test_name))

    print("\nINPUT TRANSACTION:")
    print("  Inputs:")
    for inp in tx.inputs:
        print(
            f"    ({inp['prev_tx']}, {inp['index']}) "
            f"Owner: {inp['owner']}"
        )

    print("  Outputs:")
    for out in tx.outputs:
        print(
            f"    {out['amount']} BTC → {out['address']}"
        )

    print("\nEXPECTED RESULT:")
    print("  ACCEPTED" if expected_accept else "  REJECTED")

    print("\nACTUAL RESULT:")
    if success:
        print("  ACCEPTED")
    else:
        print("  REJECTED")
        print("  Error message:", message)

    passed = (success == expected_accept)

    print("\nFINAL RESULT:")
    print(" ", "PASSED" if passed else "FAILED")


def setup():
    utxo = UTXOManager()
    mempool = Mempool()
    chain = Blockchain()

    # Genesis UTXOs
    utxo.add_utxo("genesis", 0, 50.0, "Alice")
    utxo.add_utxo("genesis", 1, 30.0, "Bob")
    utxo.add_utxo("genesis", 2, 20.0, "Charlie")
    utxo.add_utxo("genesis", 3, 10.0, "David")
    utxo.add_utxo("genesis", 4, 5.0, "Eve")

    return utxo, mempool, chain

# TEST CASES
def test_basic_transaction():
    utxo, mempool, _ = setup()

    tx = Transaction(
        "tx1",
        inputs=[{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        outputs=[
            {"amount": 10, "address": "Bob"},
            {"amount": 39.999, "address": "Alice"}
        ]
    )

    result = mempool.add_transaction(tx, utxo)
    print_test_details("Test 1 – Basic Valid Transaction", tx, True, result)


def test_multiple_inputs():
    utxo, mempool, _ = setup()

    tx = Transaction(
        "tx2",
        inputs=[
            {"prev_tx": "genesis", "index": 0, "owner": "Alice"},
            {"prev_tx": "genesis", "index": 2, "owner": "Charlie"}
        ],
        outputs=[{"amount": 60, "address": "Bob"}]
    )

    result = mempool.add_transaction(tx, utxo)
    print_test_details("Test 2 – Multiple Inputs", tx, True, result)


def test_double_spend_same_tx():
    utxo, mempool, _ = setup()

    tx = Transaction(
        "tx3",
        inputs=[
            {"prev_tx": "genesis", "index": 0, "owner": "Alice"},
            {"prev_tx": "genesis", "index": 0, "owner": "Alice"}
        ],
        outputs=[{"amount": 10, "address": "Bob"}]
    )

    result = mempool.add_transaction(tx, utxo)
    print_test_details("Test 3 – Double Spend in Same Transaction", tx, False, result)


def test_mempool_double_spend():
    utxo, mempool, _ = setup()

    tx1 = Transaction(
        "tx4a",
        inputs=[{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        outputs=[{"amount": 10, "address": "Bob"}]
    )

    tx2 = Transaction(
        "tx4b",
        inputs=[{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        outputs=[{"amount": 10, "address": "Charlie"}]
    )

    mempool.add_transaction(tx1, utxo)
    result = mempool.add_transaction(tx2, utxo)

    print_test_details("Test 4 – Mempool Double Spend", tx2, False, result)


def test_insufficient_funds():
    utxo, mempool, _ = setup()

    tx = Transaction(
        "tx5",
        inputs=[{"prev_tx": "genesis", "index": 1, "owner": "Bob"}],
        outputs=[{"amount": 35, "address": "Alice"}]
    )

    result = mempool.add_transaction(tx, utxo)
    print_test_details("Test 5 – Insufficient Funds", tx, False, result)


def test_negative_output():
    utxo, mempool, _ = setup()

    tx = Transaction(
        "tx6",
        inputs=[{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        outputs=[{"amount": -5, "address": "Bob"}]
    )

    result = mempool.add_transaction(tx, utxo)
    print_test_details("Test 6 – Negative Output", tx, False, result)


def test_zero_fee():
    utxo, mempool, _ = setup()

    tx = Transaction(
        "tx7",
        inputs=[{"prev_tx": "genesis", "index": 4, "owner": "Eve"}],
        outputs=[{"amount": 5.0, "address": "Alice"}]
    )

    result = mempool.add_transaction(tx, utxo)
    print_test_details("Test 7 – Zero Fee Transaction", tx, True, result)


def test_race_attack():
    utxo, mempool, _ = setup()

    low_fee = Transaction(
        "tx8_low",
        inputs=[{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        outputs=[{"amount": 49.999, "address": "Bob"}]
    )

    high_fee = Transaction(
        "tx8_high",
        inputs=[{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        outputs=[{"amount": 40, "address": "Charlie"}]
    )

    mempool.add_transaction(low_fee, utxo)
    result = mempool.add_transaction(high_fee, utxo)

    print_test_details("Test 8 – Race Attack (First Seen Rule)", high_fee, False, result)


def test_mining_flow():
    utxo, mempool, _ = setup()

    tx = Transaction(
        "tx9",
        inputs=[{"prev_tx": "genesis", "index": 3, "owner": "David"}],
        outputs=[{"amount": 9.999, "address": "Alice"}]
    )

    print("\nTest 9 – Complete Mining Flow")

    print("\nINPUT:")
    for inp in tx.inputs:
        print(inp)
    for out in tx.outputs:
        print(out)

    mempool.add_transaction(tx, utxo)
    mine_block("Miner1", mempool, utxo)

    balance = utxo.get_balance("Miner1")

    print("\nEXPECTED: Miner should receive transaction fee")
    print("ACTUAL: Miner balance =", balance)

    print("\nFINAL RESULT:")
    print(" ", "PASSED" if balance > 0 else "FAILED")


def test_fork_handling():
    _, _, chain = setup()

    print("\nTest 10 – Fork Resolution")

    head = chain.get_longest_chain_head()

    b1 = Block("A", head, [], "MinerA")
    b2 = Block("B", head, [], "MinerB")

    chain.add_block(b1)
    chain.add_block(b2)

    b3 = Block("C", b2.hash, [], "MinerC")
    chain.add_block(b3)

    winner = chain.get_longest_chain_head()

    print("Expected longest chain head: ", b3.hash)
    print("Actual longest chain head:   ", winner)

    print("\nFINAL RESULT:")
    print(" ", "PASSED" if winner == b3.hash else "FAILED")


# Run all tests

def run_all_tests():
    print("\n=== RUNNING ALL TEST SCENARIOS ===\n")

    test_basic_transaction()
    test_multiple_inputs()
    test_double_spend_same_tx()
    test_mempool_double_spend()
    test_insufficient_funds()
    test_negative_output()
    test_zero_fee()
    test_race_attack()
    test_mining_flow()
    test_fork_handling()

    print("\n=== ALL TESTS COMPLETED ===\n")


if __name__ == "__main__":
    run_all_tests()
