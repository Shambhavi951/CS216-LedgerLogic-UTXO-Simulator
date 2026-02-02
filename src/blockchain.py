from block import Block

class Blockchain:
    def __init__(self):
        self.blocks = {}      # hash → Block
        self.height = {}      # hash → height
        self.heads = set()    # competing chain tips

        # Genesis block
        genesis = Block(
            block_id="GENESIS",
            prev_hash=None,
            transactions=[],
            miner="network"
        )

        self.blocks[genesis.hash] = genesis
        self.height[genesis.hash] = 0
        self.heads.add(genesis.hash)

    def add_block(self, block):
        if block.prev_hash not in self.blocks:
            print("Orphan block rejected")
            return

        self.blocks[block.hash] = block
        self.height[block.hash] = self.height[block.prev_hash] + 1

        # fork handling
        if block.prev_hash in self.heads:
            self.heads.remove(block.prev_hash)

        self.heads.add(block.hash)

    def get_longest_chain_head(self):
        longest = None
        max_height = -1

        for head in self.heads:
            if self.height[head] > max_height:
                max_height = self.height[head]
                longest = head

        return longest

    def show_chains(self):
        print("\nCompeting Chains")
        for head in self.heads:
            print(f"Head: {head} | Height: {self.height[head]}")
