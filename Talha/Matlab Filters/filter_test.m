load log3.dat
load bump.dat
logx = log3;

figure(1)
plot(logx);
axis([0 25000 -1 5]);
title('Accelerometer Sampled Data Unfiltered');
xlabel('# of Samples');
ylabel('Acceleration(g)');





Fs = 1000;
T = 1/Fs;
L = length(logx);
Y = fft(logx);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = Fs*(0:(L/2))/L;
figure(2)
plot(f, P1);
axis([0 500 0 0.1]);
title('Frequency Spectrum of Unfiltered Accelerometer Data');
xlabel('Frequency');
ylabel('Magnitude');


% Construct an FDESIGN object and call its BUTTER method.

N   = 4;   % Order
Fc1 = 3;   % First Cutoff Frequency
Fc2 = 150;  % Second Cutoff Frequency

% Construct an FDESIGN object and call its BUTTER method.
h  = fdesign.bandpass('N,F3dB1,F3dB2', N, Fc1, Fc2, Fs);
Hd = design(h, 'butter');
y = filter(Hd, logx);
figure(3);
plot(y)
axis([0 25000 -3 3]);
title('Bandpass (3 Hz - 150 Hz) Filtered Accelerometer Data');
xlabel('# of Samples');
ylabel('Acceleration(g)');


T = 1/Fs;
L = length(y);
Y = fft(y);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = Fs*(0:(L/2))/L;
figure(4)
plot(f, P1);
axis([0 500 0 0.1])
title('Frequency Spectrum of Filtered Accelerometer Data');
xlabel('Frequency');
ylabel('Magnitude');


