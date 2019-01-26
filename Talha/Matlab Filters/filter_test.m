load log3.dat
load bump.dat
logx = log3;
n = 10;
b = arrayfun(@(i) mean(logx(i:i+n-1)),1:n:length(logx)-n+1)';
logx = b;
figure(1)
plot(log3);
axis([0 25000 -2 4]);
% axis([0 5000 1.1 1.3])
% Fs = 1000;  % Sampling Frequency
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
axis([0 500 0 0.06])

  % Sampling Frequency

% Construct an FDESIGN object and call its BUTTER method.


N   = 2;   % Order
Fc1 = 3;   % First Cutoff Frequency
Fc2 = 80;  % Second Cutoff Frequency

% Construct an FDESIGN object and call its BUTTER method.
h  = fdesign.bandpass('N,F3dB1,F3dB2', N, Fc1, Fc2, Fs);
Hd = design(h, 'butter');
y = filter(Hd, logx);
figure(3)
plot(y)
axis([0 3000 -1 1]);


Fs = 1000;
T = 1/Fs;
L = length(y);
Y = fft(y);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = Fs*(0:(L/2))/L;
figure(4)
plot(f, P1);
axis([0 500 0 0.06])



%plot(line) 