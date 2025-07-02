# Overview
- File contains serial-port I/O utilizing .NET's [System.IO.Ports.SerialPort] (https://learn.microsoft.com/en-us/dotnet/api/system.io.ports.serialport?view=net-9.0-pp)

- Uses real-time FFT/DFT tot process incoming samples: [FFT/DFT] (https://en.wikipedia.org/wiki/Fast_Fourier_transform)

- charting the live sifgnal with the WinForms Chart control [winForms] (https://learn.microsoft.com/en-us/visualstudio/ide/create-a-visual-basic-winform-in-visual-studio?view=vs-2022)

- loging to and rotating capture0-files

- multithreaded producer/consumer loop that keeps the UI responsive

- Several Helper math routines 
    - Windowing
    - RMS
    - phase
    - averaging
    - peak-hold
    - UI formatting
    