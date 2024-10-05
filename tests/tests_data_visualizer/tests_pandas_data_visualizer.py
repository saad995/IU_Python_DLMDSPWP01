import unittest
import pandas as pd
from data_visualizer.bokeh_data_visualizer import BokehDataVisualizer

class TestBokehDataVisualizer(unittest.TestCase):

    def test_visualize(self):
        visualizer = BokehDataVisualizer()
        train_data = pd.DataFrame({'X': [1, 2, 3], 'Y1': [4, 5, 6]})
        ideal_data = pd.DataFrame({'X': [1, 2, 3], 'I1': [4.1, 5.1, 6.1]})
        test_data = pd.DataFrame({'X': [1, 2], 'Y': [4, 5], 'Ideal Function': ['I1', 'I1']})
        
        # Since Bokeh's `show` function opens a web browser, 
        # we cannot assert on the visual output. 
        # Here we assume if no errors occur, the test is passed.
        try:
            visualizer.visualize(train_data, ideal_data, test_data)
        except Exception as e:
            self.fail(f'Visualization failed with exception {e}')

if __name__ == '__main__':
    unittest.main()