% Motor A y motor B, calibracion

pwm = [90 110 120 140 160 180 200 220 240 255];
flujo_a = [ 27 35.37 48.82 59.60 68.5 75.30 80.92 87.5 92.35 98.9];
flujo_b = [17.94 25.25 34.84 42.84 49.54 53.15 59.57 60.93 64.20 71.63];

p_a = polyfit(pwm,flujo_a,1);
p_b = polyfit(pwm,flujo_b,1);
pend_a = p_a(1)
orden_a = p_a(2)
pend_b = p_b(1)
orden_b = p_b(2)

f = polyval(p_a,pwm);
figure(1)
plot(pwm,flujo_a, 'o' , pwm, f, '-')
legend('data motor A','ajuste','Location','northwest')
ylabel('flujo [L/hora]')
xlabel ('Valor PWM ')

g = polyval(p_b,pwm);
figure(2)
plot(pwm,flujo_b, 'o' , pwm, g, '-')
legend('data motor B','ajuste','Location','northwest')
ylabel('flujo [L/hora]')
xlabel ('Valor PWM ')