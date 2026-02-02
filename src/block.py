from utxo_manager import UTXOManager
from transaction import Transaction
from mempool import Mempool


def mine_block(miner_address, mempool, utxo_manager, num_txs=5):
    """
    Simulate Mining a block
    1. Select top transactions from mempool
    2. Update UTXO set (remove inputs, add outputs)
    3. Add miner fee as special UTXO
    4. Remove mined transactions from mempool
    """

    selected_txs = mempool.get_top_transactions(num_txs, utxo_manager)

    if not selected_txs:
        print("No transactions to mine.")
        return

    total_fees = 0.0
    print("\nMining block...")

    for tx in selected_txs:

        input_sum = 0.0
        output_sum = 0.0

        # Remove input UTXOs
        for inp in tx.inputs:
            prev_tx = inp["prev_tx"]
            index = inp["index"]

            utxo = utxo_manager.utxo_set.get((prev_tx, index))
            if utxo is None:
                print(f"Missing UTXO ({prev_tx}, {index})")
                continue

            input_sum += utxo["amount"]
            utxo_manager.remove_utxo(prev_tx, index)

        # Add output UTXOs
        for i, out in enumerate(tx.outputs):
            utxo_manager.add_utxo(
                tx.tx_id,
                i,
                out["amount"],
                out["address"]
            )
            output_sum += out["amount"]

        # Transaction fee
        fee = input_sum - output_sum
        total_fees += fee

        # Remove transaction from mempool
        mempool.remove_transaction(tx.tx_id)

    # Coinbase reward
    utxo_manager.add_utxo(
        tx_id="COINBASE",
        index=len(utxo_manager.utxo_set),
        amount=total_fees,
        owner=miner_address
    )

    print("Block mined successfully!")
    print(f"Miner {miner_address} receives {total_fees:.6f} BTC\n")


class Block:
    def __init__(self, block_id, prev_hash, transactions, miner):
        self.block_id = block_id
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.miner = miner

        # Toy hash (allowed by assignment)
        self.hash = f"hash_{block_id}"

    def __str__(self):
        return f"Block {self.block_id} mined by {self.miner}"
