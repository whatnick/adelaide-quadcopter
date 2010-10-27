% generate a ITAE robust PID controller
wn=10;
k1=0.8475;
k2=0.1304;

Kpip=2.15*wn^2/k1;
Kiip=wn^3/k1;
Kdip=1.75*wn/k1;

Gcip=tf([Kdip Kpip Kiip],[1 0])
Titaep=feedback(TFp*Gcip,1)


Kpiy=2.15*wn^2/k2;
Kiiy=wn^3/k2;
Kdiy=1.75*wn/k2;

Gciy=tf([Kdiy Kpiy Kiiy],[1 0])
Titaey=feedback(TFy*Gciy,1)