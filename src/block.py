def mine_block(miner_address, mempool, utxo_manager, num_txs=5):
    """
   Simulate Mining a block

    1. Select top transactions from mempool
    2. Update UTXO set(remove inputs,add outputs)
    4. Add miner fee as special UTXO
    5. Remove mined transactions from mempool
    """
    
    
    # 1. Select transactions (highest fee first)
    selected_txs = mempool.get_top_transactions(num_txs, utxo_manager)

    if not selected_txs:
        print("No transactions to mine.")
        return

    total_fees = 0.0

    print("\nMining block...")

    for tx in selected_txs:

        input_sum = 0.0
        output_sum = 0.0
        
        # Remove Input UTXOs (prevents double spending)
        for inp in tx.inputs:
            prev_tx = inp["prev_tx"]
            index = inp["index"]

            utxo = utxo_manager.utxo_set[(prev_tx, index)]
            input_sum += utxo["amount"]
            
            # permanently remove spent UTXO
            utxo_manager.remove_utxo(prev_tx, index)
            
        # Add Ouput UTXOs
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
        
        # Remove TX from Mempool
        mempool.remove_transaction(tx.tx_id)
        
        
    # Special miner fee UTXO (COINBASE)
    utxo_manager.add_utxo(
        tx_id="COINBASE",
        index=len(utxo_manager.utxo_set),
        amount=total_fees,
        owner=miner_address
    )

    print("Block mined successfully!")
    print(f"Miner {miner_address} receives {total_fees:.6f} BTC\n")
