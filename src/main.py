import time
import random


# Utility

def generate_tx_id():
    return f"tx_{int(time.time())}_{random.randint(1000,9999)}"


# Genesis Block

def create_genesis_utxos(utxo_manager):
    utxo_manager.add_utxo("genesis", 0, 50.0, "Alice")
    utxo_manager.add_utxo("genesis", 1, 30.0, "Bob")
    utxo_manager.add_utxo("genesis", 2, 20.0, "Charlie")
    utxo_manager.add_utxo("genesis", 3, 10.0, "David")
    utxo_manager.add_utxo("genesis", 4, 5.0, "Eve")


# Create Transaction


def create_transaction(utxo_manager, mempool):
    valid_addresses = utxo_manager.get_all_addresses()
    sender = input("Enter sender: ").strip()

    if sender not in valid_addresses:
        print("Invalid sender address\n")
        return

    utxos = utxo_manager.get_utxos_for_owner(sender)
    if not utxos:
        print("No UTXOs available.\n")
        return

    balance = sum(u[2] for u in utxos)
    print(f"Available balance: {balance} BTC")

    receiver = input("Enter recipient: ").strip()

    if receiver not in valid_addresses:
        print("Invalid recipient address\n")
        return

    amount = float(input("Enter amount (BTC): "))

    fee = float(input("Enter fee: "))
    total_required = amount + fee

    if balance < total_required:
        print("Insufficient funds\n")
        return

    inputs = []
    input_sum = 0
    i=1

    print("Available UTXOs:")
    for tx_id, index, amt in utxos:
        print(str(i)+".  tx_id: "+tx_id+" index: "+str(index)+" amt: "+str(amt))
        i=i+1

    print("Please enter -1 when done.")
    while (True):
        num= int (input("Enter UTXO number: "))
        if num == -1:
            break
        if num>=i:
            print("Invalid UTXO number")
            continue
        tx_id, index, amt = utxos[num-1]
        inputs.append({
            "prev_tx": tx_id,
            "index": index,
            "owner": sender
        })
        input_sum += amt

    outputs = [
        {"amount": amount, "address": receiver}
    ]

    change = input_sum - total_required
    if change > 0:
        outputs.append({
            "amount": change,
            "address": sender
        })

    tx = Transaction(
        tx_id=generate_tx_id(),
        inputs=inputs,
        outputs=outputs
    )

    success, msg = mempool.add_transaction(tx, utxo_manager)

    if success:
        print("Transaction valid\n")
        ok, fee = tx.fee_check(utxo_manager)
        print(f"Fee: {fee:.6f} BTC")
        print(f"Transaction ID: {tx.tx_id}")
        print(f"Change: {change:.6f} BTC \n")
    else:
        print("Transaction rejected:", msg, "\n")


# Test Scenarios

def run_tests(utxo_manager, mempool):
    print("\n Running Test Scenario: Double Spend")

    utxos = utxo_manager.get_utxos_for_owner("Alice")
    tx_id, index, amt = utxos[0]

    tx1 = Transaction(
        "tx_ds_1",
        inputs=[{"prev_tx": tx_id, "index": index, "owner": "Alice"}],
        outputs=[{"amount": 10, "address": "Bob"}]
    )

    tx2 = Transaction(
        "tx_ds_2",
        inputs=[{"prev_tx": tx_id, "index": index, "owner": "Alice"}],
        outputs=[{"amount": 10, "address": "Charlie"}]
    )

    print("TX1:", mempool.add_transaction(tx1, utxo_manager))
    print("TX2:", mempool.add_transaction(tx2, utxo_manager))
    print()


# Main Program

def main():
    utxo_manager = UTXOManager()
    mempool = Mempool()
    blockchain = Blockchain()

    create_genesis_utxos(utxo_manager)

    print("\n=== Bitcoin Transaction Simulator ===")
    print("Initial UTXOs (Genesis Block):")
    print("- Alice   : 50.0 BTC")
    print("- Bob     : 30.0 BTC")
    print("- Charlie : 20.0 BTC")
    print("- David   : 10.0 BTC")
    print("- Eve     : 5.0 BTC\n")

    while True:
        print("Main Menu:")
        print("1. Create new transaction")
        print("2. View UTXO set")
        print("3. View mempool")
        print("4. Mine block")
        print("5. Run test scenarios")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            create_transaction(utxo_manager, mempool)

        elif choice == "2":
            print("\n", utxo_manager, "\n")

        elif choice == "3":
            print("\n Mempool:")
            mempool.view_mempool()
            print()

        elif choice == "4":
            miner = input("Enter miner name: ")

            selected = mempool.get_top_transactions(5, utxo_manager)

            mine_block(miner, mempool, utxo_manager)

            if selected:
                new_block = Block(
                    block_id=f"B{random.randint(1000,9999)}",
                    prev_hash=blockchain.get_longest_chain_head(),
                    transactions=selected,
                    miner=miner
                )

                blockchain.add_block(new_block)
                blockchain.show_chains()

        elif choice == "5":
            run_all_tests()

        elif choice == "6":
            print("Exit")
            break

        else:
            print("Invalid choice\n")


if __name__ == "__main__":
    main()
