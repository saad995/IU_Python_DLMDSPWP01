import pandas as pd
from bokeh.plotting import figure, output_file, save, show
from bokeh.models import ColumnDataSource
from sqlalchemy import column
from data_visualizer.data_visualizer import DataVisualizer
from exception_handler import DataProcessingError
from bokeh.palettes import Dark2_5 as palette
import itertools

class BokehDataVisualizer(DataVisualizer):
    """Derived class for data visualization using Pandas"""

    def visualize_data(self, x_train, y_train, ideal_functions, x_test, y_test, mapped_data):
        """Visualizes data using Bokeh"""
        #colors has a list of colors which can be used in plots 
        colors = itertools.cycle(palette) 
        
        try:
            # Create a new plot with a title and axis labels
            p = figure(title="Training Data and Ideal Functions", x_axis_label='x', y_axis_label='y')

            # Plot training data
            for i in range(y_train.shape[1]):
                p.line(x_train, y_train[:, i], legend_label=f'Training y{i+1}', line_width=2, color=next(colors))

            # Plot ideal functions
            for i, ideal_func in enumerate(ideal_functions):
                p.line(x_train, ideal_func, legend_label=f'Ideal Function {i+1}', line_dash='dashed', line_width=2)

            # Create a new plot for test data and its mapping
            p2 = figure(title="Test Data and Mapped Ideal Functions", x_axis_label='x', y_axis_label='y')

            # Plot test data
            p2.circle(x_test, y_test, legend_label='Test Data', size=8, color="red", alpha=0.6)

            # Plot mapped ideal functions
            for i, ideal_func in enumerate(mapped_data):
                p2.line(x_test, ideal_func, legend_label=f'Mapped Ideal Function {i+1}', line_dash='dotted', line_width=2)

            # Organize the layout
            layout = column(p, p2)

            # Save the plot
            # output_file("visualization.html")
            # save(layout)
            show(layout)

        except Exception as e:
            raise DataProcessingError(f"Error visualizing data: {str(e)}")