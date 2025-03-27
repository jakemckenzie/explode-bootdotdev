import time
import unittest
from src.mypackage.utils.split_delimiter import split_nodes_delimiter
from src.mypackage.nodes.text_node import TextNode, TextType

class TestSplitDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_benchmark(self) -> None:
        test_nodes = []
        for i in range(2**10):
            text = "This is a *test* string with *delimited* text."
            test_nodes.append(TextNode(text, TextType.NORMAL))

        delimiter = "*"
        new_type = TextType.BOLD

        start_time = time.perf_counter()

        result_nodes = split_nodes_delimiter(test_nodes, delimiter, new_type)
        
        end_time = time.perf_counter()
        
        elapsed_time = end_time - start_time      

        print(f"Elapsed Time: {elapsed_time:.6f} seconds")
        print(f"Processed {len(test_nodes)} nodes into {len(result_nodes)} resulting nodes.")
        
        self.assertTrue(len(result_nodes) > 0)

if __name__ == '__main__':
    unittest.main()
