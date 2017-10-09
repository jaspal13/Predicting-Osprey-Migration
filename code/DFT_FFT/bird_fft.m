function T = bird_fft(y, t_type, y_type, type)
% Compute the fft for data y and return the period T

n = length(y);
time = linspace(1,n,n)'/n;

% plot the original data
% figure
% plot(time,y)
% xlabel(t_type)
% ylabel(y_type)
% title([type,' ',y_type])

movavg = 0;
smth = 0;

%% moving average
% apply a moving average filter

if movavg == 1
    y = mov_avg(10,y,y_type,t_type,type,time);
end


%% smooth the signal
% this is done by setting each latitude to be the average of its neighbours

if smth == 1
    y = smooth(1000,y,y_type,t_type,type,time);
end


%% do fft

% set parameters for fft
Fs = n; % sampling frequency
L = n; % length

figure
plot(Fs*time,y)
xlabel(t_type)
ylabel(y_type)
title([type,' ',y_type])

% subtract mean
y = detrend(y);
% find fft
Y = fft(y);
% magnitude of fft
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
% frequency for plotting
f = Fs*(0:(L/2))/L;

figure
subplot(2,1,1)
stem(f,P1)
title(['Single-Sided Amplitude Spectrum of the ',y_type])
xlabel('f (Hz)')
ylabel('FFT Magnitude')

subplot(2,1,2)
stem(f(1:50),P1(1:50))
title(['Single-Sided Amplitude Spectrum of the ',y_type])
xlabel('f (Hz)')
ylabel('FFT Magnitude')

% find the max of the fft
x_dft = 0:(Fs/L):(Fs/2-Fs/L);
dft = P1(1:L/2,1);
% find the corresponding frequency
max_fft = max(dft);
freq = find(dft==max(dft));
freq = x_dft(freq);
% find the period
T = n/freq;

% if minutes, convert to days
if strcmp(t_type,'minutes') == 1
    % the period of migration in days
    T = T/24;
end

end

