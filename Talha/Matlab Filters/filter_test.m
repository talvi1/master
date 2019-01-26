load log7.dat
load bump.dat
log = log7;
figure(1)
plot(log);
% axis([0 5000 1.1 1.3])
% Fs = 1000;  % Sampling Frequency
Fs = 1000;
T = 1/Fs;
L = length(log);
Y = fft(log);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = Fs*(0:(L/2))/L;
figure(2)
plot(f, P1);
axis([0 500 0 0.06])
figure(2)

Fstop = 2;           % Stopband Frequency
Fpass = 2.5;           % Passband Frequency
Astop = 20;          % Stopband Attenuation (dB)
Apass = 19.9999;           % Passband Ripple (dB)
match = 'stopband';  % Band to match exactly

% Construct an FDESIGN object and call its BUTTER method.
h  = fdesign.highpass(Fstop, Fpass, Astop, Apass, Fs);
Hd = design(h, 'butter', 'MatchExactly', match);
y = filter(Hd, log);
figure(3)
plot(y)
axis([000 5000 -2.5 2.5])
B = [0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01];
A = [0.04];

f = filter(B, A, y);
figure(4)
plot(f);
axis([0 5000 -2.5 2.5])
Fs = 1000;
T = 1/Fs;
L = length(f);
Y = fft(f);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = Fs*(0:(L/2))/L;
figure(2)
plot(f, P1);
axis([0 500 0 1])



%plot(line) 