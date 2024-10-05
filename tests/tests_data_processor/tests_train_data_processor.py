import unittest
import pandas as pd
from data_processor.train_data_processor import TrainDataProcessor

class TestTrainDataProcessor(unittest.TestCase):

    def test_process(self):
        data = pd.DataFrame({'X': [1, 2, 3], 'Y': [4, 5, 6]})
        processor = TrainDataProcessor(data)
        result = processor.process()
        pd.testing.assert_frame_equal(result, data)

    def test_calculate_deviations(self):
        train_data = pd.DataFrame({'X': [1, 2, 3], 'Y1': [4, 5, 6]})
        ideal_data = pd.DataFrame({'X': [1, 2, 3], 'I1': [4.1, 5.1, 6.1]})
        processor = TrainDataProcessor(train_data)
        deviations = processor.calculate_deviations(ideal_data)
        expected_deviation = pd.Series([0.03], index=['I1'])
        pd.testing.assert_series_equal(deviations.iloc[0], expected_deviation)

    def test_cluster_ideal_functions(self):
        ideal_data = pd.DataFrame({'X': [1, 2, 3], 'I1': [4, 5, 6], 'I2': [4.1, 5.1, 6.1], 'I3': [10, 11, 12]})
        processor = TrainDataProcessor(ideal_data)
        kmeans = processor.cluster_ideal_functions(ideal_data, n_clusters=2)
        self.assertEqual(len(set(kmeans.labels_)), 2)

if __name__ == '__main__':
    unittest.main()