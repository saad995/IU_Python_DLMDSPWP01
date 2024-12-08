from bokeh.layouts import column
from bokeh.plotting import figure, show, output_file, save
from data_visualizer.data_visualizer import DataVisualizer
from exception_handler import DataProcessingError

class BokehDataVisualizer(DataVisualizer):
    """Derived class for data visualization using Pandas"""

    def visualize_data(self, x_train, y_train, ideal_functions, x_test, y_test, mapped_data, current_dateTime):
        """Visualizes data using Bokeh"""
        layout = column()
        
        try:
            for i in range(y_train.shape[1]):
                # Create a new plot with a title and axis labels
                p = figure(title=f"Training Data (y{i+1}) and Ideal Function ({ideal_functions.columns[i+1]})", x_axis_label='x', y_axis_label='y')

                # Plot training data
                p.line(x_train, y_train[:, i], legend_label=f'Training data y{i+1}', line_width=2, color='red')

                # Plot ideal functions
                p.line(x_train, ideal_functions[ideal_functions.columns[i+1]], legend_label=f'Ideal function {ideal_functions.columns[i+1]}', line_dash='dashed', line_width=2, color='green')

                # Organize the layout
                layout.children.append(p)

            # Create a new plot for test data and its mapping
            p2 = figure(title="Test Data and Mapped Ideal Functions", x_axis_label='x', y_axis_label='y')

            # Plot test data
            p2.line(x_test, y_test, legend_label='Test Data',line_width=2, color="red")
            # p2.circle(x_test, y_test, legend_label='Test Data', size=8, color="red", alpha=0.6)

            # Plot mapped ideal functions
            p2.line(mapped_data['X (test func)'], mapped_data['ideal_func_val'], legend_label=f'Mapped Ideal Function', line_dash='dashed', line_width=2, color="green")

            # Organize the layout
            layout.children.append(p2)

            # Save the plot
            output_file(f"./graphs/graph_plotting_{current_dateTime}.html")
            save(layout)

            show(layout)

        except Exception as e:
            raise DataProcessingError(f"Error visualizing data: {str(e)}")