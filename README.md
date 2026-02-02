
**CS216 – Bitcoin Transaction & UTXO Simulator**

**Overview**
This repository contains the implementation of a Bitcoin Transaction and UTXO Simulator developed as part of the CS216: Introduction to Blockchain course assignment. The project simulates the core mechanisms of Bitcoin’s transaction system, focusing on the UTXO model, transaction validation, mempool management, mining, and double-spending prevention.

All mandatory test cases and bonus objectives specified in the assignment have been successfully implemented and verified.

**Features Implemented**

1.UTXO Manager
- Maintains the global UTXO set
- Adds and removes UTXOs on transaction confirmation
- Computes balance for a given address
- Retrieves all UTXOs owned by an address
- Supports efficient lookup of unspent outputs

2.Transaction Structure and Validation
- Implements transaction inputs and outputs as per specification
- Enforces all validation rules including double-spend checks, fee calculation, and conflict detection

3.Mempool Management
- Stores valid unconfirmed transactions
- Prevents double spending using spent UTXO tracking
- Removes confirmed transactions after mining

4.Mining Simulation
- Selects transactions from the mempool based on fee
- Updates the UTXO set permanently
- Allocates collected fees to the miner

5.Double-Spending Prevention
- Detects double spending within a transaction and across the mempool
- Simulates race attacks using the first-seen rule


**How to Run**
- Python 3.8 or higher required
- Run: python src/main.py

Notes:-
This is a local simulation with no networking or real cryptography.

**TEAM MEMBERS**
Shambhavi S Vijay 240041034 MnC,
Vaishnavi Ventrapragada 240002078 EE,
Priyanshi Mahto 240002057 EE,
Devanshi Mahto 240001023 CSE

