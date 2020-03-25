%% for simulation

%% instrumentation amplifier

R2 = 47000;
R1 = R2;

R5 = 100000;
Rg = 2000;

gain = R2/R1 * (1+ 2*R5/Rg);

t = linspace(0,10,1000);
y1 = (12E-5)*sin(2*pi*72*t - pi/2);
y2 = (12E-5)*sin(2*pi*83*t + pi/32);

v_out = (y2-y1)*gain;

plot(t, v_out)