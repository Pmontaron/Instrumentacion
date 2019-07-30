%Flujo_salida1 = [86.63 75.9 84.05 85.92 82.09];
Flujo_salida2 = [72.72 67.63 64.90 56.60 80.18];
Flujo_salida3 = [109.53 102.86 109.53 108.33 112.27];
Flujo_salida4 = [104.25 94.82 103.65 107.14 107.14];
%Flujo_salida5 = [78.72 76 73.07 75.10 76.54];
%valor_caudalimetro = [10.75 13.73 53.16 31.30 18.06];
%flujo_salida = [mean(Flujo_salida1) mean(Flujo_salida2) mean(Flujo_salida3) mean(Flujo_salida4) mean(Flujo_salida5)];

valor_caudalimetro = [ 13.73 53.16 31.30 ];
flujo_salida = [ mean(Flujo_salida2) mean(Flujo_salida3) mean(Flujo_salida4) ];

p = polyfit(valor_caudalimetro,flujo_salida,1);
pend = p(1)
orden = p(2)

f = polyval(p,valor_caudalimetro);
figure(1)
plot(valor_caudalimetro,flujo_salida, 'o' , valor_caudalimetro, f, '-')
%legend('data motor A','ajuste','Location','northwest')
ylabel('flujo [L/hora]')
xlabel ('Valor caudalimetro ')
