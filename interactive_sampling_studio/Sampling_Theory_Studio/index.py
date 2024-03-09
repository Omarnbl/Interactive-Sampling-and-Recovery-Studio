from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import numpy as np
import pyqtgraph as pg
import pandas as pd
import os
import random
import sys
import  math
from os import path
from reportlab.lib import colors
from reportlab.platypus import *
from PyQt5.QtWidgets import QMessageBox
import scipy.fftpack as fft
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject, pyqtSignal
import scipy.interpolate as interp
import scipy.signal as signal

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
ui, _ = loadUiType('main1.ui')
ui2, _ = loadUiType('mixer.ui')

global shared_signal
shared_signal=[]
global max_mixer_freq
max_mixer_freq=0
class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.event_bus = EventBus()
        self.mixer_window = MixerWindow(self.event_bus)
        self.event_bus.done_button_clicked.connect(self.handle_button_click)
        # INITIALIZATIONS
        self.signal_data = []  # y of the original
        self.new_sample_times = []  # x of the new sampled
        self.interpolated_signal = []  # y of the new sampled
        self.x_values = []  # x of the original
        self.max_freq = 0
        self.f_s=0
        # MAIN WIDGETS
        rgb_color = '#cdcdcd'
        self.main_widget_1 = pg.PlotWidget()
        main_widget_1 = self.findChild(QWidget, 'main_widget_1')
        main_widget_1_layout = QVBoxLayout(main_widget_1)
        main_widget_1_layout.addWidget(self.main_widget_1)
        main_widget_1_layout.setContentsMargins(0, 0, 0, 0)

        self.main_widget_2 = pg.PlotWidget()
        main_widget_2 = self.findChild(QWidget, 'main_widget_2')
        main_widget_2_layout = QVBoxLayout(main_widget_2)
        main_widget_2_layout.addWidget(self.main_widget_2)
        main_widget_2_layout.setContentsMargins(0, 0, 0, 0)

        self.main_widget_3 = pg.PlotWidget()
        main_widget_3 = self.findChild(QWidget, 'main_widget_3')
        main_widget_3_layout = QVBoxLayout(main_widget_3)
        main_widget_3_layout.addWidget(self.main_widget_3)
        main_widget_3_layout.setContentsMargins(0, 0, 0, 0)
        self.main_widget_1.setBackground(rgb_color)
        self.main_widget_3.setBackground(rgb_color)
        self.main_widget_2.setBackground(rgb_color)

        # mixer button
        self.open_mixer_btn = self.findChild(QPushButton, 'open_mixer_btn')
        self.open_mixer_btn.clicked.connect(self.open_mixer_btn_clicked)
        self.import_btn = self.findChild(QPushButton, 'import_btn')
        self.import_btn.clicked.connect(self.import_btn_clicked)

        # slider frequency
        self.main_frequency_slider = self.findChild(QSlider, 'main_frequency_slider')
        self.main_frequency_slider.valueChanged.connect(self.normalized_frequency)
        self.main_frequency_slider.setValue(20)
        # slider noise
        self.main_noise_slider = self.findChild(QSlider, 'main_noise_slider')
        self.main_noise_slider.valueChanged.connect(self.add_noise_to_signal)
        self.freq_from_slider = 2
        self.lcdNumber_normalized = self.findChild(QLCDNumber, 'lcdNumber_normalized')
        self.lcdNumber = self.findChild(QLCDNumber, 'lcdNumber')
        self.mixer_window = None

    def handle_button_click(self):
        # This function will be called when the button in the MixerWindow is clicked
        global shared_signal
        self.signal_data = shared_signal
        self.original_signal_data=shared_signal
        global max_mixer_freq
        self.max_freq = max_mixer_freq
        self.lcdNumber.display(2 * self.max_freq)
        self.x_values = np.linspace(0 , 8, 1000)        # self.mixer_flag=True
        self.plot_o_symbols(2 ,self.signal_data)
        self.main_widget_3.setYRange(0, 1)

    # function to open the MixerWindow
    def open_mixer_btn_clicked(self):
        # if self.mixer_window is None:
        self.mixer_window = MixerWindow(self.event_bus)
        self.mixer_window.show()
    def import_btn_clicked(self):
        self.main_widget_1.clear()
        # self.mixer_flag = False
        self.main_widget_3.setYRange(0,0.5)
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        csv_files, _ = QFileDialog.getOpenFileNames(self, "Open Files", "", "CSV Files (*.csv);;All Files (*)",
                                                    options=options)
        if csv_files:
            try:
                for csv_file in csv_files:
                    with open(csv_file, 'rb') as file:
                        df = pd.read_csv(csv_file)
                        # get the time and amplitude values from the file
                        temp_y_values = df.iloc[:, -1].values
                        temp_x_values = df.iloc[:, 0]
                        self.signal_data = temp_y_values[0:1000]
                        self.x_values = temp_x_values[0:1000]
                        # Generate a random color for the new signal
                        self.original_signal_data=self.signal_data
                        #here pass the value from the slider
                        slider_min = self.main_frequency_slider.minimum()
                        slider_max = self.main_frequency_slider.maximum()
                        midpoint = int((slider_max + slider_min) / 2)
                        # Calculate the max freq of the signal
                        self.max_freq = (1 / (self.x_values[1] - self.x_values[0])) / 2
                        self.main_frequency_slider.setValue(midpoint)
                        self.original_signal_data=self.signal_data
                        #here pass the value from the slider
                        self.main_frequency_slider.setValue(20)
                        self.lcdNumber.display(2 * (self.max_freq))
                        # x_view = 8
                        # self.main_widget_1.setXRange(x_view, 0.25)
                        # self.main_widget_1.setYRange(min(self.signal_data[:x_view]), max(self.signal_data[:x_view]))
                        self.plot_o_symbols(2,self.signal_data)

            except Exception as e:
                print(f'Error reading DAT file: {str(e)}')
    def plot_o_symbols(self,passed_freq,data):
        self.main_widget_1.clear()
        # Generate a random color for the new signal
        color = (50, 50, 250)
        self.main_widget_1.plot(self.x_values, data, pen=pg.mkPen(color=color, width=1))
        freq_from_slider = passed_freq
        f_sample = freq_from_slider * (self.max_freq)
        self.f_s = f_sample
        time_interval = 1 / f_sample
        # need to make it a numpy array so we can get the last value of it
        self.x_values = np.array(self.x_values)
        # Create a new array of sample times based on the new time_interval
        self.new_sample_times = np.arange(0, self.x_values[-1], time_interval)
        # Use linear interpolation to generate the interpolated signal values
        self.interpolated_signal = np.interp(self.new_sample_times, self.x_values, data)
        # Plot the interpolated signal with "o" symbols
        self.main_widget_1.plot(self.new_sample_times, self.interpolated_signal, symbol='o', pen=None, symbolPen=(255, 255, 255, 0), symbolSize=5, symbolBrush=(50, 50, 250, 255))
        self.reconstruct_signal()

    def o_reconsruct_b (self, t, f_sample, x_sample, y_sample):
        # x_values = t //  x_sample = nT // y_sample = x[n] //  f_sample = 1/T
        y_recon = np.zeros_like(t)
        for point in range(len(t)):
            y_recon[point] = np.sum(y_sample * np.sinc((t[point] - x_sample) * f_sample))

        return y_recon
    def reconstruct_signal(self):

        reconstructed_signal = self.o_reconsruct_b(self.x_values,self.f_s,self.new_sample_times,self.interpolated_signal)
        reconstructed_signal = np.array(reconstructed_signal)
        # calculate the error between the two signals
        difference = (self.original_signal_data - reconstructed_signal) ** 2
        self.main_widget_2.clear()
        self.main_widget_2.plot(self.x_values, reconstructed_signal, pen=pg.mkPen(width=1.5,color=(50, 200, 100)))
        self.main_widget_3.clear()
        self.main_widget_3.plot(self.x_values, difference, pen=pg.mkPen(width=1, color=(255, 100, 100)),
                                name="Difference")
    def normalized_frequency(self):
        slider_value = self.main_frequency_slider.value()
        min_frequency = 0  # Minimum value you want
        max_frequency = 10  # Maximum value you want
        # Calculate the corresponding frequency based on the slider value
        freq_from_slider = min_frequency + ((max_frequency - min_frequency) * (slider_value / 100.0))
        # Ensure the frequency is within the range [1, 4]
        freq_from_slider = max(min(freq_from_slider, max_frequency), min_frequency)
        self.lcdNumber_normalized.display(freq_from_slider)
        # Update the slider value to match the calculated frequency
        self.main_frequency_slider.setValue(int((freq_from_slider - min_frequency) / (max_frequency - min_frequency) * 100))

        self.lcdNumber.display(freq_from_slider * (self.max_freq))
        self.plot_o_symbols(freq_from_slider,self.signal_data)

    def add_noise_to_signal(self):
        self.signal_data = self.original_signal_data
        min_snr = 0  # Define your minimum SNR
        max_snr = 1  # Define your maximum SNR
        self.main_noise_slider.setMinimum(0)
        self.main_noise_slider.setMaximum(100)
        # Get the SNR from the slider
        snr = self.main_noise_slider.value()
        power=self.signal_data**2
        signal_avg_power=10*(np.log(np.mean(power)))
        noise_power_db=signal_avg_power-snr
        noise_power =(10 ** (noise_power_db/ 10))
        # Calculate the standard deviation of the noise
        noise_std_dev = np.sqrt(noise_power)
        # Generate noise with the same length as the signal data
        noise = np.random.normal(0, noise_std_dev, len(self.signal_data))
        noise = noise * (snr)
        # Add noise to the signal data
        noisy_signal_data = self.signal_data + noise
        self.signal_data = noisy_signal_data

        self.main_noise_slider.setValue(int(snr))
        try:
            self.plot_o_symbols(self.freq_from_slider, self.signal_data)
            # Return the noisy signal data (or original signal if snr is 0)
            return self.signal_data
        except:
            print(" ")


class EventBus(QObject):
    done_button_clicked = pyqtSignal()
class MixerWindow(QMainWindow, ui2):
    def __init__(self,event_bus):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.event_bus = event_bus
        #ARRAYS TO STORE COMPONENTS
        self.mixer_components=[]
        self.mixer_check_boxes = []
        self.mixer_checked_check_boxes = []
        self.mixer_unchecked_check_boxes = []
        self.string_components=[]
        self.mixer_all_freq=[]
        # FINAL MIXER SIGNAL
        self.final_mixer_signal = []
        # MIXER WIDGET
        rgb_color = '#cdcdcd'
        self.mixer_figure = pg.PlotWidget()
        self.mixer_figure.setBackground(rgb_color)
        # CONNECTING THE MIXER CHANNEL TO ITS WIDGET
        mixer_widget=self.findChild(QWidget,'mixer_widget')
        mixer_layout=QVBoxLayout(mixer_widget)
        mixer_layout.addWidget(self.mixer_figure)
        mixer_layout.setContentsMargins(0, 0, 0, 0)
        # INITALIZING MIXER Q TIMER
        self.mixer_timer = QTimer(self)
        self.mixer_timer.timeout.connect(lambda :self.update_graph_eqn())
        # CONTAINER FOR SCROLL AREA
        self.scroll_area_container = QWidget(self.scrollArea)
        self.scroll_area_container_layout = QVBoxLayout(self.scroll_area_container)
        self.scrollArea.setWidget(self.scroll_area_container)
        # CONNECTING THE LABEL OF THE TOTAL EQN
        self.mixer_total_eqn=self.findChild(QLabel,"mixer_total_eqn")
        # CONNECTING RADIO BUTTONS AND LINE EDITS OF MIXER TO VARIABLES
        self.sine_radio_Button=self.findChild(QRadioButton,'sine_radio_Button')
        self.cosine_radio_Button = self.findChild(QRadioButton, 'cosine_radio_Button')
        self.mixer_amplitude=self.findChild(QLineEdit,'mixer_amplitude')
        self.mixer_frequency=self.findChild(QLineEdit,'mixer_frequency')
        self.mixer_phase_shift=self.findChild(QLineEdit,'mixer_phase_shift')
        self.mixer_vertical_shift=self.findChild(QLineEdit,'mixer_vertical_shift')
        #DECLARING GLOBAL AMPLITUDE,ANGULAR FREQ,PHASE SHIFT,VERTICAL SHIFT
        self.wave_type=''
        self.amplitude_value=0
        self.frequency_value=0
        self.phase_shift_value=0
        self.vertical_shift_value=0
        #ADD BUTTON
        self.mixer_add_btn = self.findChild(QPushButton, 'mixer_add_btn')
        self.mixer_add_btn.clicked.connect(lambda :self.mixer_add_component())
        #DONE BUTTON
        self.mixer_done_btn = self.findChild(QPushButton, 'mixer_done_btn')
        self.mixer_done_btn.clicked.connect(lambda :self.import_mixer_signal())
        self.mixer_done_btn.clicked.connect(self.emit_done_button_clicked)

    def emit_done_button_clicked(self):
        # Emit the custom signal
        self.event_bus.done_button_clicked.emit()
    def mixer_add_component(self):
        valid_input = True
        if self.sine_radio_Button.isChecked():
            self.wave_type = 'sine'
        elif self.cosine_radio_Button.isChecked():
            self.wave_type = 'cosine'
        else:
            valid_input = False
        try:
            self.amplitude_value = float(self.mixer_amplitude.text())
        except ValueError:
            valid_input = False
        try:
            self.frequency_value = float(self.mixer_frequency.text())
            self.mixer_all_freq.append(self.frequency_value)
        except ValueError:
            valid_input = False
        try:
            self.phase_shift_value = float(self.mixer_phase_shift.text())
        except ValueError:
            valid_input = False
        try:
            self.vertical_shift_value = float(self.mixer_vertical_shift.text())
        except ValueError:
            valid_input = False
        if valid_input:
            x_values = np.linspace(0, 8, 1000)
            component=self.generate_sinusoidal(self.wave_type, self.amplitude_value, self.frequency_value*2*np.pi, self.phase_shift_value, self.vertical_shift_value,x_values)
            self.mixer_components.append(component)
            self.show_component()
        else:
            self.show_error_message("Invalid Data")
    def generate_sinusoidal(self,wave_type, amplitude, frequency, phase_shift, vertical_shift,x_values):
        if wave_type == 'sine':
            y_values = (amplitude * np.sin(frequency * x_values + phase_shift) + vertical_shift)
        elif wave_type == 'cosine':
            y_values = (amplitude * np.cos(frequency * x_values + phase_shift) + vertical_shift)
        else:
            raise ValueError("Invalid wave type. Use 'sine' or 'cosine'.")
        return y_values
    def show_component(self):
        if self.wave_type == 'sine':
            component=str(self.amplitude_value)+"sin(2Π "+'('+str(self.frequency_value)+')'+"X+"+str(self.phase_shift_value)+")+"+str(self.vertical_shift_value)
            component=component.replace("+-",'-')
            if component[0]!='-':
                component=' +'+component
            self.string_components.append(component)
        elif self.wave_type == 'cosine':
            component=str(self.amplitude_value)+"cos(2Π "+'('+str(self.frequency_value)+')'+"X+"+str(self.phase_shift_value)+")+"+str(self.vertical_shift_value)
            component = component.replace("+-", '-')
            if component[0]!='-':
                component=' +'+component
            self.string_components.append(component)
        self.mixer_amplitude.clear()
        self.mixer_frequency.clear()
        self.mixer_phase_shift.clear()
        self.mixer_vertical_shift.clear()
        self.show_group_box(component)
    def show_group_box(self,component):
        # SHOWING SIGNAL COMPONENTS
        components_groupbox = QGroupBox()
        components_groupbox.setStyleSheet("QGroupBox {border: 2px solid gray; background-color: #ffffff;}")
        components_groupbox.setTitle(f"{component}")
        self.mixer_check_boxes.append(QCheckBox("show", components_groupbox))
        self.mixer_check_boxes[len(self.mixer_check_boxes) - 1].setChecked(True)
        vbox_layout = QVBoxLayout(components_groupbox)
        vbox_layout.addWidget(self.mixer_check_boxes[len(self.mixer_check_boxes) - 1])
        components_groupbox.setLayout(vbox_layout)
        self.scroll_area_container_layout.addWidget(components_groupbox)
        self.scrollArea.setWidgetResizable(True)
        # UPDATE GRAPH FUNCTION TIMER
        self.mixer_timer.start(100)
    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(message)
        msg.setWindowTitle("Error")
        msg.exec_()
    def update_graph_eqn(self):
        self.mixer_figure.clear()
        current_total_eqn="Total eqn: "
        for checkbox in range (len(self.mixer_check_boxes)):
            if self.mixer_check_boxes[checkbox].isChecked():
                current_total_eqn=current_total_eqn+str(self.string_components[checkbox])
                self.mixer_checked_check_boxes.append(self.mixer_components[checkbox])
        x_values = np.linspace(0, 8, 1000)
        y_values = np.zeros(1000)
        for component in self.mixer_checked_check_boxes:
            y_values += component
        self.mixer_figure.plot(x_values, y_values, pen=pg.mkPen(width=1.5,color=(50, 200, 100)))
        self.mixer_checked_check_boxes.clear()
        self.mixer_total_eqn.setText(current_total_eqn)
        self.final_mixer_signal=y_values
    def import_mixer_signal(self):
        global shared_signal
        shared_signal=self.final_mixer_signal
        global max_mixer_freq
        try:
            max_mixer_freq=max(self.mixer_all_freq)
        except ValueError:
            pass
        self.close()

def main():
    app = QApplication(sys.argv)
    main = MainApp()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()