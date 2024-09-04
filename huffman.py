from __future__ import annotations
import heapq
import numpy as np
from sys import getsizeof
from node import Node


class HuffmanCompression:
    def __init__(self, data: str) -> None:

        assert len(data) > 1
        assert all(type(x) == str for x in data)
        self._data = data
        self.tree = None
        self.table = {}
        self._unique_items: list[str] = list(set(data))
        self._frequencies: list[int] = [data.count(x) for x in self._unique_items]
        self._nodes = [
            Node(freq, data)
            for freq, data in zip(self._frequencies, self._unique_items)
        ]

    def build_tree(self):

        heapq.heapify(self._nodes)
        while len(self._nodes) > 1:
            lelem = heapq.heappop(self._nodes)
            relem = heapq.heappop(self._nodes)
            merged_elem = Node(frequency=lelem.frequency + relem.frequency)
            merged_elem.set_left(lelem)
            merged_elem.set_right(relem)
            heapq.heappush(self._nodes, merged_elem)

        self.tree = self._nodes[0]

    def generate_codes(self, tree, encoding=""):
        if tree is not None:
            if tree.data is not None:
                self.table[tree.data] = {
                    "Frequency": tree.frequency,
                    "Code": encoding,
                }
            left_encoding = encoding + "0"
            right_encoding = encoding + "1"
            self.generate_codes(tree.get_left, encoding=left_encoding)
            self.generate_codes(tree.get_right, encoding=right_encoding)

    def compress(self, chunk_length: int = 100):
        self.build_tree()
        self.generate_codes(tree=self.tree)

        self.encoding = "".join([self.table[char]["Code"] for char in self._data])

        chunks = [
            [
                int(self.encoding[pos : pos + chunk_length], 2),
                len(self.encoding[pos : pos + chunk_length]),
            ]
            for pos in range(0, len(self.encoding), chunk_length)
        ]
        return self.table, chunks

    def get_stats(self):
        symbol = list(self.table.keys())
        sum_freq = sum(self._frequencies)
        weights = [
            self.table[data]["Frequency"] / sum_freq for data in self.table.keys()
        ]
        assert sum(weights) == 1

        codewords = [self.table[data]["Code"] for data in self.table.keys()]
        codewords_len = list(map(lambda x: len(x), codewords))

        contrib_weighted_path_len = np.dot(weights, codewords_len)

        probability_budget = np.pow(1 / 2, codewords_len)
        information_content = np.negative(np.log2(weights))
        contrib_entropy = np.dot(probability_budget, information_content)
        efficiency = contrib_entropy / contrib_weighted_path_len
        # print(
        #     f"\n->>\nSymbol: {symbol}\nCodewords: {codewords}\nWeights: {weights}\nNegLog:{information_content}\nProbability budget: {probability_budget}"
        # )
        print(contrib_weighted_path_len, contrib_entropy, efficiency)


def retrieve_data(
    huffman_table,
    encoded_list,
):
    # print(encoded_list)
    binary_encoding = "".join([bin(x[0])[2:].zfill(x[1]) for x in encoded_list])

    return binary_encoding


if __name__ == "__main__":
    from itertools import zip_longest

    data = """God, grant me the serenity to accept the \
        things I cannot change, the courage to change the things I can,\
            and the wisdom to know the difference."""
    # data = """
    # Sed ut perspiciatis unde omnis iste natus error sit voluptatem \
    # accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore \
    # veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit \
    # aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit \
    # amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam \
    # aliquam quaerat voluptatem.
    # """
    # data = "A_DEAD_DAD_CEDED_A_BAD_BABE_A_BEADED_ABACA_BED"
    # data = "abcdefghijklmnopqrstuvwxyz"
    # data = "a quick brown fox jumps on the lazy dog"
    # data = "aaaaabbbbbcccccdddddeeeee"
    ## Compression

    with open("./moby_dick.txt", "r") as file:
        data = "".join(file.readlines())

    huffman_pipeline = HuffmanCompression(data)
    table, chunks = huffman_pipeline.compress(chunk_length=100)
    huffman_pipeline.get_stats()
    binary = retrieve_data(table, chunks)

    print(f"Encoded size: {getsizeof(chunks)}\t Original size:{getsizeof(data)}")
    # print(huffman_pipeline.encoding == binary)
    # print(len(huffman_pipeline.encoding), len(binary))
