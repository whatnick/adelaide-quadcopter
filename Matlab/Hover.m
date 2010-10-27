disp('Question 1')
%define variables
I=0.1969;
Jp=0.0552;
Jr=Jp;
Jy=Jp+Jr;
Kf=0.594;
Kt=0.0180;
Kfn=Kf;
Kfc=Kf;
Ktn=-Kt;
Ktc=Kt;
disp('[I Jp Jr Jy Kf Kt Kfn Kfc Ktn Ktc]=')
[I Jp Jr Jy Kf Kt Kfn Kfc Ktn Ktc]

%state matrices
Am=[0 1 0 0 0 0;...
    0 0 0 0 0 0;...
    0 0 0 1 0 0;...
    0 0 0 0 0 0;...
    0 0 0 0 0 1;...
    0 0 0 0 0 0];
Bm=[0 0 0 0;...
    -Kt/Jy -Kt/Jy Kt/Jy Kt/Jy;...
    0 0 0 0;...
    I*Kfn/Jp -I*Kfn/Jp 0 0;...
    0 0 0 0;...
    0 0 I*Kfc/Jr -I*Kfc/Jr];
Cm=[1 0 0 0 0 0;...
    0 0 1 0 0 0;...
    0 0 0 0 1 0];
Dm=[0 0 0 0;...
    0 0 0 0;...
    0 0 0 0];

hover_model=ss(Am,Bm,Cm,Dm);
disp('Open loop poles are')
Pole(hover_model)
disp('Open loop poles are all at 0, the system only responses to a very low freq since the roll off rate is -120db/decade at the beginning');
disp(' ');
disp(' ');


disp('Question 2')
disp('Rank number is')
rank(ctrb(hover_model))
disp('Cond number is')
cond(ctrb(hover_model))
disp('full rank:controlable. cond number is reasenablly small, system can be easily controled')
disp(' ');
disp(' ');

disp('Question 3')
Cm
disp(' ');
disp(' ');

disp('Question 4')
disp('Rank number is')
rank(obsv(hover_model))
disp('Cond number is')
cond(obsv(hover_model))
disp('full rank:observable. cond number is 1, system is ideally observable')
disp(' ');
disp(' ');

disp('Question 5')
Am_agm=[Am zeros(6,3);...
    1 0 0 0 0 0 0 0 0;...
    0 0 1 0 0 0 0 0 0;...
    0 0 0 0 1 0 0 0 0];
Bm_agm=[Bm;zeros(3,4)];
Cm_agm=[Cm zeros(3)];
Dm_agm=Dm;
hover_model_agm=ss(Am_agm,Bm_agm,Cm_agm,Dm_agm);

Q=diag([10000 100 20000 500 20000 500 20000 20000 20000]);
R=eye(4);

K=lqr(Am_agm,Bm_agm,Q,R)
Km=K(:,1:6)
Ki=K(:,7:9)
disp(' ');
disp(' ');


disp('Question 6')
disp('The CL system poles are')
CLpole=eig(Am-Bm*Km)
disp(' ');
disp(' ');


disp('Question 7')
Mat_in=[zeros(6,3);eye(3)]
Am_fb_agm=[Am-Bm*Km -Bm*Ki;...
          Cm-Dm*Km -Dm*Ki];
Bm_fb_agm=Mat_in;
Cm_fb_agm=Cm_agm;
Dm_fb_agm=zeros(3);

hover_fb_agm=ss(Am_fb_agm,Bm_fb_agm,Cm_fb_agm,Dm_fb_agm)
disp(' ');
disp(' ');


disp('Question 8')
disp('Desired CL poles of hover_fb_agm')
P_desired=10*pole(hover_fb_agm)

disp('Observer gain is')
L=transpose(place(Am',Cm',CLpole))


% design the PID controller
% employ the pole placement method
% the T1 & T2 are infinite

% the Petch and roll PID controller
wp=1.8;
Zp=0.9;
ap=7.5;
Ap=0.8475;

Kpp=wp^2*(1+2*Zp*ap)/Ap
Tip=(1+2*Zp*ap)/(ap*wp)
Tdp=(ap+2*Zp)/(wp*(1+2*Zp*ap))

% the Yaw PID controller
wy=0.44;
Zy=0.707;
ay=0.2;
Ay=0.1304;

Kpy=wy^2*(1+2*Zy*ay)/Ay
Tiy=(1+2*Zy*ay)/(ay*wy)
Tdy=(ay+2*Zy)/(wy*(1+2*Zy*ay))

% Double PID controler
beta = 0.25








