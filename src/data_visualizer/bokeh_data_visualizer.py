from bokeh.layouts import column
from bokeh.plotting import figure, show, output_file, save
from data_visualizer.data_visualizer import data_visualizer
from exception_handler import DataVisualizationError


class bokeh_data_visualizer(data_visualizer):
    """Derived class for data visualization using Bokeh"""

    def visualize_data(self, x_train, y_train, ideal_functions, x_test, y_test, mapped_data, current_dateTime):
        """Visualizes data using Bokeh"""
        layout = column()

        try:
            for i in range(y_train.shape[1]):
                # Create a new plot with a title and axis labels
                p = figure(title=f"Train Function (y{i+1}) and Ideal Function ({
                           ideal_functions.columns[i+1]})", x_axis_label='x', y_axis_label='y')

                # Plot training data
                p.line(x_train, y_train[:, i], legend_label=f'Train function y{
                       i+1}', line_width=2, color='red')

                # Plot ideal functions
                p.line(x_train, ideal_functions[ideal_functions.columns[i+1]], legend_label=f'Ideal function {
                       ideal_functions.columns[i+1]}', line_dash='dashed', line_width=2, color='green')

                # Organize the layout
                layout.children.append(p)

            # Create a new plot for test data and its mapping
            p2 = figure(title="Complete Test Function Data VS Mapped Ideal Function",
                        x_axis_label='x', y_axis_label='y')

            # Plot test data
            p2.line(x_test, y_test, legend_label='Test Function',
                    line_width=2, color="red")

            # Plot mapped ideal functions
            p2.line(mapped_data['X (test func)'], mapped_data['ideal_func_val'],
                    legend_label=f'Mapped Ideal Function', line_dash='dashed', line_width=2, color="green")

            # Organize the layout
            layout.children.append(p2)

            # Create a new plot for test data and its mapping
            p3 = figure(title="Partial Test Function Data (mapped one's only) VS Mapped Ideal Function",
                        x_axis_label='x', y_axis_label='y')

            # Plot test data
            p3.line(mapped_data['X (test func)'], mapped_data['Y (test func)'], legend_label='Test Function',
                    line_width=2, color="red")

            # Plot mapped ideal functions
            p3.line(mapped_data['X (test func)'], mapped_data['ideal_func_val'],
                    legend_label=f'Mapped Ideal Function', line_dash='dashed', line_width=2, color="green")

            # Organize the layout
            layout.children.append(p3)

            # Save the plot
            output_file(f"./graphs/graph_plotting_{current_dateTime}.html")
            save(layout)

            show(layout)

        except Exception as e:
            raise DataVisualizationError(f"Error visualizing data: {str(e)}")
