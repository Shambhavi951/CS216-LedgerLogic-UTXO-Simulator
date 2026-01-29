from utxo_manager import UTXOManager

class Transaction:
    def __init__(self, tx_id, inputs, outputs):
        self.tx_id = tx_id
        self.inputs = inputs
        self.outputs = outputs
    
    # Check whether referenced UTXOs exist
    def input_exists_check(self,utxo_manager):
        for inp in self.inputs:
            if(not utxo_manager.exists(inp["prev_tx"],inp["index"])):
                return False
        return True
    
    # Check for duplicate inputs inside same transaction
    def double_spend_check(self):
        seen=set()
        for inp in self.inputs:
            key=(inp["prev_tx"],inp["index"])
            if(key in seen):
                return False
            seen.add(key)
        return True
    
    # Check output amounts are non-negative
    def neg_op_check(self,utxo_manager):
        for op in self.outputs:
            if(op["amount"]<0):
                return False
        return True
    
    # Check inputs >= outputs and compute fee
    def fee_check(self,utxo_manager):
        sum_inputs=0
        sum_outputs=0
        for inp in self.inputs:
            utxo=utxo_manager.utxo_set[(inp["prev_tx"],inp["index"])]
            sum_inputs+=utxo["amount"]
        for op in self.outputs:
            sum_outputs+=op["amount"]
        if(sum_inputs>=sum_outputs):
            return True,sum_inputs-sum_outputs
        else:
            return False,-1.0
    
    # Check UTXO not already spent in mempool
    def mempool_conflict_check(self,mempool):
        for inp in self.inputs:
            key=(inp["prev_tx"],inp["index"])
            if(key in mempool.spent_utxos):
                return False
        return True
        
    def validation(self,utxo_manager,mempool):
        if(not self.input_exists_check(utxo_manager)):
            return False
        if(not self.double_spend_check()):
            return False
        if(not self.neg_op_check(utxo_manager)):
            return False
        if(not self.mempool_conflict_check(mempool)):
            return False
        ans,_=self.fee_check(utxo_manager)
        if(not ans):
            return False
        return True
