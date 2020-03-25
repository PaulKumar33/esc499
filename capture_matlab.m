%%arduino analog capture
%%

a = arduino("COM5", "uno")

analog_read = zeros(500,1);
time_ = seconds(analog_read);

t0 = datetime('now');
for i = 1:500
    analog_read(i) = readVoltage(a, "A0");
    time_ = datetime('now') - t0;
end


