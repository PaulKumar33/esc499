%% this is the filter simulation script
% the script is to simulate the effects of the filter
% this filter is to test the effects of filter order and cutoff
hold off
clear all 

file_input = "C:\Users\paulk\OneDrive - University of Toronto\engsci 1t9\year 4 fall\ESC499\Data\amp_sys_6.m4a";
[fileIn, Fs] = audioread(file_input);

figure(1)
fc = 1000;
order = 4;
[b,a] = butter(order, 1000/(Fs/2));
[b2, a2] = butter(order,750/(Fs/2));
[bbs, abs] = butter(order, 20/(Fs/2), 'high');
freqz(b,a)

figure(2)
f = filter(b,a,fileIn(:,1)); 
f = filter(bbs,abs,f);

%amplify the signal
%f = f.*10;
f = filter(b2,a2, f);
subplot(2,1,1)
plot(f)
title("filtered signal")
xlabel("samples")
ylabel("Signal [mV]")

hold on
subplot(2,1,2)
plot(fileIn(:,1))
title("unfiltered signal")
xlabel("samples")
ylabel("Signal [mV]")

final = zeros(length(f), 2);
t = linspace(0, length(f)/Fs, length(f));

final(:, 1) = t;
final(:,2) = f;

filename = "lpf_4_1000_750.csv";

writematrix(final, filename);
%audiowrite(filename, f, Fs);
