class UTXOManager :
 # Store UTXOs as dictionary : (tx_id , index ) -> (amount , owner )
    def __init__ ( self ) :
       self.utxo_set = {}

    def add_utxo ( self , tx_id : str , index : int , amount : float , owner :str ) :
       """ Add a new UTXO to the set ."""
       self.utxo_set[(tx_id,index)]={
          "amount":amount,
          "owner":owner
       }

    def remove_utxo ( self , tx_id : str , index : int ) :
       """ Remove a UTXO ( when spent )."""

       if (tx_id,index) in self.utxo_set:
         del self.utxo_set[(tx_id,index)]


    def get_balance ( self , owner : str ) -> float :
       """ Calculate total balance for an address ."""
       balance =0.0
       for utxo in self.utxo_set.values():
          if utxo["owner"]==owner:
             balance +=utxo["amount"]
       return balance

    def exists ( self , tx_id : str , index : int ) -> bool :
       """ Check if UTXO exists and is unspent ."""
       return (tx_id,index) in self.utxo_set


    def view_utxos(self):
      """
      Display all current UTXOs
      """
      if not self.utxo_set:
        print("UTXO set is empty.")
        return

      print("\nCurrent UTXO Set")
      for (tx_id, index), utxo in self.utxo_set.items():
        print(
            f"({tx_id}, {index}) → "
            f"{utxo['amount']} BTC | Owner: {utxo['owner']}"
        )
      print()

    def get_utxos_for_owner ( self , owner : str ) -> list :
      """ Get all UTXOs owned by an address ."""
      result=[]
      for(tx_id,index), utxo in self.utxo_set.items():
         if utxo["owner"]==owner:result.append((tx_id,index,utxo["amount"]))
      return result

    def __str__(self):
       """Print the UTXO set"""

       if not self.utxo_set:
           return "UTXO set is empty."
       lines=["Currect UTXO set"]

       for(tx_id,index),utxo in self.utxo_set.items():
          lines.append(
             f"({tx_id},{index}) ->{utxo['amount']} BTC | Owner : {utxo['owner']}"
          )
       return "\n".join(lines)