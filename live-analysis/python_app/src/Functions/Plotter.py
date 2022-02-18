import matplotlib.pyplot as plt

class Plotter():
    '''
    A class to draw a nice looking live graph with matplotlib.
    '''

    def __init__(self):
        self.__bar_started = False

    def __eventWindowClosed(self):
        '''
        Event hook for when chart window is closed. Should not be publicly accessed.
        '''

        print('closing window')
        self.__bar_started = False

    def isStarted(self):
        '''
        Method to check if a window is open
        '''

        return self.__bar_started

    def closeWindow(self):
        '''
        Method to programatically close chart window.
        '''

        plt.close('all')
        self.__eventWindowClosed()
    
    def drawChart(self, predictions):
        '''
        This method draws and updates the chart displayed on the created window
        based on the prediction probabilities passed to it.

        PARAMETERS:
        predictions: a list that contains the returned contents of the 
        `predict_post()` function of `Request.py`. 
        Expected format: `[status_code, response_body]`
        '''

        # TODO visualise predictions
        print(predictions)

        # check if bar chart has been initialised
        if not self.__bar_started: # if chart is not initialised, create chart
            plt.ion()

            self.__plot_figure = plt.figure(1, figsize=(10,7))
            self.__plot_figure.canvas.mpl_connect('close_event', self.__eventWindowClosed)

            self.__plot_axes = self.__plot_figure.add_subplot(111)
            self.__plot_axes.set_xlim(left=0, right=1)
            self.__plot_axes.set_xlabel('Probability')

            self.__bar_rects = self.__plot_axes.barh(
                predictions[1]['signalNames'], 
                predictions[1]['predictions'],
                color='#ff4e02' if predictions[1]['filtered'] else '#02c4ff'
            )
            self.__bar_started = True

        else: # if chart is initialised, update chart
            ax = self.__plot_axes
            rects = self.__bar_rects

            ax.set_title(f'Filtering: {predictions[1]["filtered"]}')

            for rect, pred in zip(rects, predictions[1]['predictions']):
                rect.set_width(pred)
                rect.set(color='#ff4e02' if predictions[1]['filtered'] else '#02c4ff')
            plt.pause(0.01)

        # update the window
        plt.draw()

# def main():
#     import numpy as np
#     from time import sleep
#     chart = Plotter()
# 
#     for i in range(5):
#         chart.drawChart([200, {
#             'filtered' : True, 
#             'predictions' : np.random.rand(7),
#             'signalNames' : ['a', 'b', 'c', 'd', 'e', 'f', 'g']
#         }])
# 
#         sleep(1)
# 
#     chart.closeWindow()
# 
#     for i in range(5):
#         chart.drawChart([200, {
#             'filtered' : True, 
#             'predictions' : np.random.rand(7),
#             'signalNames' : ['a', 'b', 'c', 'd', 'e', 'f', 'g']
#         }])
# 
#         sleep(1)