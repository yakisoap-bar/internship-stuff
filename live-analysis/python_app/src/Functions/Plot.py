import matplotlib.pyplot as plt

from Functions.Utils import printStatus, printPrediction

class Plotter():
    '''
    A class to draw a nice looking live graph with matplotlib.
    '''

    def __init__(self):
        self.__bar_started = False

    def __eventWindowClosed(self, event):
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

    def drawChart(self, predictions):
        '''
        This method draws and updates the chart displayed on the created window
        based on the prediction probabilities passed to it.

        PARAMETERS:
        predictions: a list that contains the returned contents of the 
        `predict_post()` function of `Request.py`. 
        Expected format: `[status_code, response_body]`
        '''
        # assign variables to data for sanity
        data = predictions[1]

        printPrediction(predictions)

        # check if bar chart has been initialised
        if not self.__bar_started: # if chart is not initialised, create chart
            plt.ion()

            # initialise chart
            self.__plot_figure = plt.figure(1, figsize=(10,7))
            self.__plot_figure.canvas.mpl_connect('close_event', self.__eventWindowClosed)

            # set up chart
            self.__plot_axes = self.__plot_figure.add_subplot(111)
            self.__plot_axes.set_xlim(left=0, right=1)
            self.__plot_axes.set_xlabel('Probability')
            
            # plot first figure
            self.__bar_rects = self.__plot_axes.barh(
                data['signalNames'], 
                data['predictions'],
                color='#ff4e02' if data['filtered'] else '#02c4ff'
            )

            # set title as filtering status
            self.__plot_axes.set_title(f'Filtering: {data["filtered"]}')

            # generate textboxes for each signal for filtered status and prediction numbers
            self.__text_list = [
                self.__plot_axes.text(
                    pred+0.01 if pred < 0.08 else pred-0.01, 
                    i, round(pred, 2), 
                    va='center',
                    color='black',
                    ha='left' if pred < 0.08 else 'right',
                ) 
                for i, pred in enumerate(data['predictions'])
            ]

            if data['filtered']:
                for name, textbox in zip(data['signalNames'], self.__text_list):
                    if name in data['filteredSignals']:
                        textbox.set(
                            backgroundcolor='#ff4e02', 
                            color='white', 
                            x=0.03, 
                            text='Filtered', 
                            ha='left'
                        )

            self.__bar_started = True

        else: # if chart is initialised, update chart
            ax = self.__plot_axes
            rects = self.__bar_rects

            ax.set_title(f'Filtering: {data["filtered"]}')

            # update bar lengths with new data
            for rect, pred in zip(rects, data['predictions']):
                rect.set_width(pred)
                rect.set(color='#ff4e02' if data['filtered'] else '#02c4ff')

            # update signals textboxes
            if not data['filtered'] or len(data['filteredSignals']) == 0:
                for pred, text_box in zip(data['predictions'], self.__text_list):
                    text_box.set(
                        bbox={'alpha' : 0}, 
                        color='black', 
                        text=round(pred, 2), 
                        x=pred+0.01 if pred < 0.08 else pred-0.01, 
                        ha='left' if pred < 0.08 else 'right'
                    )
            else:
                for pred, name, text_box in zip(data['predictions'], data['signalNames'], self.__text_list):
                    if name in data['filteredSignals']:
                        text_box.set(
                            bbox={'alpha' : 1, 'fc' : '#ff4e02', 'ec' : 'none'},
                            color='white', 
                            x=0.03, 
                            text='Filtered', 
                            ha='left'
                        )
                    else:
                        text_box.set(
                            bbox={'alpha' : 0}, 
                            color='black', 
                            text=round(pred, 2), 
                            x=pred+0.01 if pred < 0.08 else pred-0.01, 
                            ha='left' if pred < 0.08 else 'right'
                        )



        # update the window
        plt.pause(0.01)


def main():
    import numpy as np
    from time import sleep
    chart = Plotter()


    # for i in range(10):
    #     chart.drawChart([200, {
    #         'filtered' : True if i == 4 or i > 7 else False, 
    #         'predictions' : np.random.rand(7),
    #         'signalNames' : ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
    #         'filteredSignals' : ['b', 'e', 'f'] if i < 5 else ['a', 'c', 'd']
    #     }])

    #     plt.pause(1)

    chart.drawChart([200, {
        'filtered' : True, 
        'predictions' : [0.234, 0, 0.123141, 0.03634, 0, 0, 0.44365],
        'signalNames' : ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
        'filteredSignals' : ['b', 'e', 'f'],
        # 'filteredSignals' : []
    }])
    
    
    plt.show(block=True)

if __name__ == '__main__':
    main()
