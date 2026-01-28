from utxo_manager import UTXOManager
from transaction import Transaction

class Mempool:
    def __init__(self, max_size=50):
        # Store unconfirmed transactions
        self.transactions = []          # list of Transaction objects

        # Track UTXOs spent by mempool transactions
        self.spent_utxos = set()         # (prev_tx, index)

        self.max_size = max_size

    def add_transaction(self, tx, utxo_manager):
        """
        Validate and add transaction.
        Return (success, message).
        """

        # Check mempool size
        if len(self.transactions) >= self.max_size:
            return False, "Mempool full"

        # Full validation
        if not tx.validation(utxo_manager, self):
            return False, "Transaction validation failed"

        # Add transaction
        self.transactions.append(tx)

        # Mark inputs as spent in mempool
        for inp in tx.inputs:
            key = (inp["prev_tx"], inp["index"])
            self.spent_utxos.add(key)

        return True, "Transaction added to mempool"

    
    def remove_transaction(self, tx_id: str):
        """
        Remove transaction (when mined).
        """

        for tx in self.transactions:
            if tx.tx_id == tx_id:
                # Free the UTXOs it was spending
                for inp in tx.inputs:
                    key = (inp["prev_tx"], inp["index"])
                    if key in self.spent_utxos:
                        self.spent_utxos.remove(key)

                self.transactions.remove(tx)
                return True
        return False


    def get_top_transactions(self, n: int, utxo_manager):
        """
        Return top N transactions by fee (highest first).
        """

        tx_fees = []
        for tx in self.transactions:
            ok, fee = tx.fee_check(utxo_manager)
            if ok:
                tx_fees.append((fee, tx))

        # Sort by fee descending
        tx_fees.sort(key=lambda x: x[0], reverse=True)

        # Return only transactions
        return [tx for _, tx in tx_fees[:n]]

    def clear(self):
        """
        Clear all transactions (e.g., after block mining in toy model).
        """
        self.transactions.clear()
        self.spent_utxos.clear()
