
# Sampling-Theory Studio

## Overview

Sampling an analog signal is a critical step in digital signal processing. The Nyquist–Shannon sampling theorem guarantees full signal recovery when sampling with a frequency greater than or equal to the signal's bandwidth. This desktop application illustrates signal sampling and recovery, demonstrating the importance and validation of the Nyquist rate.

## Features

1. **Sample & Recover**: Allows users to load a mid-length signal, visualize and sample it at different frequencies, and recover the original signal using the Whittaker–Shannon interpolation formula. The application displays three graphs: one for the original signal with sampled points, one for the reconstructed signal, and one showing the difference between the original and reconstructed signals.
2. **Load & Compose**: Signals can be loaded from files or composed using a signal mixer. The mixer allows users to add multiple sinusoidal signals of different frequencies and magnitudes, as well as remove components.
3. **Additive Noise**: Users can add noise to the signal with custom signal-to-noise ratio (SNR) levels, with the program illustrating the noise effect on different signal frequencies.
4. **Real-time**: Sampling and recovery are performed in real-time upon user changes, without requiring manual refresh.
5. **Resize**: The application can be resized easily without affecting the user interface.
6. **Different Sampling Scenarios**: Includes at least three synthetic signals generated and saved through the Composer, each addressing different testing scenarios to illustrate various aspects of signal sampling and recovery.

## Code Practice

- Follows best practices for variable and function naming.
- Ensures readability and maintainability of the code.

## Libraries Used

- **PyQt5**: For building the desktop application GUI.
- **pyqtgraph**: For real-time plotting and visualization of signals.
- **pandas**: For data manipulation and statistics generation.
- **matplotlib**: For additional plotting capabilities.
- **scipy**: For scientific computing functions, including signal interpolation.

## Preview

![Screenshot 1](interactive_sampling_studio/Sampling_Theory_Studio/screen_shots/image.png)
![Screenshot 2](interactive_sampling_studio/Sampling_Theory_Studio/screen_shots/image_2.png)
![Screenshot 3](interactive_sampling_studio/Sampling_Theory_Studio/screen_shots/image_3.png)
![Screenshot 4](interactive_sampling_studio/Sampling_Theory_Studio/screen_shots/image_4.png)
![Screenshot 5](interactive_sampling_studio/Sampling_Theory_Studio/screen_shots/image_5.png)

## Team Members
## Contributors <a name = "Contributors"></a>

<table>
  <tr>
    <td align="center">
      <div style="text-align:center; margin-right:20px;">
        <a href="https://github.com/OmarEmad101">
          <img src="https://github.com/OmarEmad101.png" width="100px" alt="@OmarEmad101">
          <br>
          <sub><b>Omar Emad</b></sub>
        </a>
      </div>
    </td>
    <td align="center">
      <div style="text-align:center; margin-right:20px;">
        <a href="https://github.com/Omarnbl">
          <img src="https://github.com/Omarnbl.png" width="100px" alt="@Omarnbl">
          <br>
          <sub><b>Omar Nabil</b></sub>
        </a>
      </div>
    </td>
    <td align="center">
      <div style="text-align:center; margin-right:20px;">
        <a href="https://github.com/KhaledBadr07">
          <img src="https://github.com/KhaledBadr07.png" width="100px" alt="@KhaledBadr07">
          <br>
          <sub><b>Khaled Badr</b></sub>
        </a>
      </div>
    </td>
    <td align="center">
      <div style="text-align:center; margin-right:20px;">
        <a href="https://github.com/merna-abdelmoez">
          <img src="https://github.com/merna-abdelmoez.png" width="100px" alt="@merna-abdelmoez">
          <br>
          <sub><b>Mirna Abdelmoez</b></sub>
        </a>
      </div>
    </td>
  </tr>
</table>

## Acknowledgments

**This project was supervised by Dr. Tamer Basha & Eng. Abdallah Darwish, who provided invaluable guidance and expertise throughout its development as a part of the Digital Signal Processing course at Cairo University Faculty of Engineering.**

<div style="text-align: right">
    <img src="https://imgur.com/Wk4nR0m.png" alt="Cairo University Logo" width="100" style="border-radius: 50%;"/>
</div>
