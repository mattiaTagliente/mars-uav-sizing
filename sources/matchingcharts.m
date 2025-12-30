close all 
clear
clc

%% definizione delle variabili da ottimizzare attraverso la routine fsolve
%ottenute dal metodo statistico(input iniziale)

W=optimvar('W');
lam = optimvar('lam','LowerBound',6,'UpperBound',12); %allungamento alare vincolato
S_W=optimvar('S_W');
T_S = optimvar('T_S');
k = optimvar('k');

%% definizione dei coefficienti vari da inserire nelle equazioni

g = 9.81;
Nult = 1.5*3.8; %carico ultimo che da normativa è pari a nmax*1.5 fare riferimento a CS 25

% formule proposte per valutazione dati fusoliera come riportato nelle slide dedicate
npax=100;
nrow=25;
npaxperrow=npax/nrow;
% Rfuso = sqrt(((npaxperrow*0.46+0.96)/2)^2+0.46^2);
%0.46 larghezza media sedile, 0.96 larghezza media corridoio
% Lfus = npax/npaxperrow*1.2*1.1;
%1.2 è la lunghezza(profondità) di una fila, 1.1 fattore di correzione che
%tiene conto di pareti aggiuntive,cabine...
% %parametri fusoliera valutati secondo procedura illustrata in 2.2.1
Lfus = 36.0; %lunghezza totale compresa di cono anteriore e posteriore
Rfuso = 1.46;

%% contributi di massa suddivisi
% Parametri per massa ala (Sadraey Eq. 10.3)
tc = 0.14;             % [-] spessore relativo massimo
rho_mat = 2711;        % [kg/m^3] materiale (alluminio aeronautico)
K_rho = 0.0035;        % [-] fattore densità ala (transport, motori su ala)
sweep25_deg = 25;      % [deg] freccia al 25% corda
lambda_taper = 0.4;    % [-] rapporto di rastremazione
S = S_W*W;             % [m^2] superficie alare
% MAC trapezoidale in funzione di S, lam e lambda_taper
b_expr = sqrt(S*lam);
c_root_expr = 2*S/(b_expr*(1+lambda_taper));
c_mac_expr = (2/3)*c_root_expr*((1+lambda_taper+lambda_taper^2)/(1+lambda_taper));
Qala = ( S * c_mac_expr * tc * rho_mat * K_rho * ((lam * Nult)/cosd(sweep25_deg))^0.6 * (lambda_taper)^0.04 );
Qfus = 1/1000*Nult*(W/g)*Lfus;
Qimp = 3.5*S_W*W;
Qcarr = 0.03*W/g;
Qmot = 0.2*T_S/g*S_W*W;
Qimpianti=0.2*W/g;
Qfisso = 200 + 110*npax + 1.9*npax + 4*110;
Qf = k*W/g;

Clmaxto = 2.3; %CLmax take off che viene posto per noi pari a quello di landing
Lto = 1400;    %lunghezza di take off in metri
rhoto = 1.225; % densità di take off

Lland = 1250;  %lunghezza landing
abb = 1.9;     %decelerazione in m/s^2
V = 221.2;     % velocità di crociera con Mach 0.7 fuoriuscita da interpolazione su excell
nu = 2.4384*10^-5; %viscosità

% proprietà geometriche dell'ala
b = sqrt(S_W*W*lam);
c_root = 2*(S_W*W)/(b*(1+lambda_taper));
c = (2/3)*c_root*((1+lambda_taper+lambda_taper^2)/(1+lambda_taper));

%Valutazione coefficienti di attrito e calcolo e caricamento di tutti i
%parametri rimanenti che servono per le 5 equazioni del matching charts
Rewing = V*c/nu;
finterferenza = 1.2;
fpressione = 1.2; % fattori di correzione dati in input
tc = 0.14; %spessore massimo su corda 
fspessore = 1 + 2*tc+60*(tc)^4;
M = 0.7;
Cfwing = 0.455/(((log(Rewing)/log(10))^2.58)*(1 + 0.144*M^2)^0.65); %coefficiente attrito ala
Sfuso = 6.28*Rfuso*Lfus;
Refuso = V*Lfus/nu;
Cffuso = 0.455/(((log(Refuso)/log(10))^2.58)*(1 + 0.144*M^2)^0.65); %coefficiente attrito fusoliera
Cdovelivolo = ((2*Cfwing*fspessore*fpressione*1.2)+Cffuso*Sfuso/(S_W*W))*finterferenza;
osw = 0.93;
A = 1852*1000; %range traformato da miglie nautiche a metri 
zeta = 0.685; % manetta tutta spinta
psi = 0.5951; %funzione di quota che dipende da rapporti di pressione e temperatura
rho = 0.6527; % densità in crociera
cs = 0.7/3600*psi; %consumo specifico effettivo=cso*psi dove cs0 è il consumo specifico iniziale
% di carburante, diviso per 3600 per avere il consumo al secondo anzichè
% orario

Cl = (1/S_W)/(0.5*rho*V^2);
Cd = Cdovelivolo + Cl^2/(osw*pi*lam);
Eff = Cl/Cd;
a=0.8; %parametro che tiene conto della riserva
xfr=0.7; %coefficiente che tiene conto della resistenza e dell'attrito in fase di accelerazione

% equazioni di cui bisogna trovare la soluzione
% equazione dei pesi:
equ1 = (Qala + Qfus + Qimp + Qcarr + Qmot + Qfisso + Qf+ Qimpianti)*g -W ==0;
% equazione decollo:
equ2 = (1/S_W)^2*(1/g)*(1.75/(Clmaxto*xfr*Lto*rhoto)) - T_S == 0; % take-off: forma T/S ∝ (W/S)^2
% equazione atterraggio:
equ3 = (Lland/1.66)*abb*rhoto*Clmaxto/(1 - a*k) - 1/S_W== 0;
% equazione crociera:
equ4 = 1/(psi*zeta)*0.5*rho*V^2*Cd -T_S == 0;
% equazione di Breget semplificata:
equ5 = (Eff/cs)*V*log(1/(1 - a*k)) - A == 0;

%inizializzazione delle variabili utilizzando dati di indagine statistica
%se si usa levenberg-marquardt anche se si sbaglia l'inizializzazione la
%convergenza di solito avviene. se non converge guardare parametri di
%ingresso
x0.W = 45342.69*9.81;
x0.lam = 9.168;
x0.S_W = 85.45 / x0.W;
x0.T_S = 143132.5 / 85.45;
x0.k = 0.3496;

% Definizione delle equazioni
prob = eqnproblem;
prob.Equations.eq1 = equ1;
prob.Equations.eq2 = equ2;
prob.Equations.eq3 = equ3;
prob.Equations.eq4 = equ4;
prob.Equations.eq5 = equ5;
show(prob)

% Specifica le opzioni di ottimizzazione
options = optimoptions('fsolve','MaxFunctionEvaluations',10000,'MaxIterations', 10000,'FunctionTolerance',1e-9,'StepTolerance',1e-9,'Algorithm','levenberg-marquardt');

% Risolvi il problema utilizzando le opzioni
[sol, fval, exitflag] = solve(prob, x0, 'Options', options);
sol
T_S=sol.T_S;
S_W=sol.S_W;
W=sol.W;
k=sol.k;
lam=sol.lam;

% nota la soluzione si valutano tutti i parametri
g = 9.81;
Nult = 1.5*3.8;
npax=100;
nrow=25;
npaxperrow=npax/nrow;
% Rfuso = sqrt(((npaxperrow*0.9+1.2)/2)^2+0.9^2);
% Lfus = npax/npaxperrow*1.2*1.1;

Lfus=36;
Rfuso=1.46;
% Massa ala (Sadraey Eq. 10.3, ricalcolo post-soluzione)
rho_mat = 2711;        % [kg/m^3]
K_rho = 0.0035;        % [-]
sweep25_deg = 25;      % [deg]
lambda_taper = 0.4;    % [-]
S = S_W*W;             % [m^2]
c_wing = sqrt(S_W*W/lam); % [m]
Qala = ( S * c_wing * tc * rho_mat * K_rho * ((lam * Nult)/cosd(sweep25_deg))^0.6 * (lambda_taper)^0.04 );
Qfus = 1/1000*Nult*(W/g)*Lfus;
Qimp = 3.5*S_W*W;
Qcarr = 0.03*W/g;
Qmot = 0.2*T_S/g*S_W*W;
Qimpianti=0.2*W/g;
Qfisso = 200 + 110*npax + 1.9*npax + 4*110;
Qf = k*W/g;
Clmaxto = 2.3;
Lto = 1400;
rhoto = 1.225;

Lland = 1250;
abb = 1.9;
V = 221.2;
nu = 2.4384*10^-5;
b = sqrt (S_W*W*lam);
c_root = 2*(S_W*W)/(b*(1+lambda_taper));
c = (2/3)*c_root*((1+lambda_taper+lambda_taper^2)/(1+lambda_taper));
Rewing = V*c/nu;
finterferenza = 1.2;
fpressione = 1.2;
tc = 0.14;
fspessore = 1 + 2*tc+60*(tc)^4;
M = 0.7;
Cfwing = 0.455/(((log(Rewing)/log(10))^2.58)*(1 + 0.144*M^2)^0.65);
Sfuso = 6.28*Rfuso*Lfus;
Refuso = V*Lfus/nu;
Cffuso = 0.455/(((log(Refuso)/log(10))^2.58)*(1 + 0.144*M^2)^0.65);
Cdovelivolo = ((2*Cfwing*fspessore*fpressione*1.2)+Cffuso*Sfuso/(S_W*W))*finterferenza;
osw = 0.93;
A = 1852*1000;
zeta = 0.685;
psi = 0.5951;
rho = 0.6527;
cs = 0.7/3600*psi;
Cl = (1/S_W)/(0.5*rho*V^2);
Cd = Cdovelivolo + Cl^2/(osw*pi*lam);
Eff = Cl/Cd;
a=0.8;
S=S_W*W;
T=T_S*S;

Cd0_ala = (2*Cfwing*fspessore*fpressione*1.2)*finterferenza;
Cd_ala = Cd0_ala + Cl^2/(osw*pi*lam);
E_ala = Cl/Cd_ala;

%% salvataggio dei risultati in un file di testo leggibile
resultsFile = 'matchingcharts_results.txt';
fid = fopen(resultsFile,'w');
assert(fid ~= -1, 'Impossibile creare %s', resultsFile);
fprintf(fid, "Wing Design Key Results\n");
fprintf(fid, "=======================\n\n");
fprintf(fid, "Geometria ala\n");
fprintf(fid, "-------------\n");
fprintf(fid, "Superficie alare S         : %.4f m^2\n", S);
fprintf(fid, "Apertura alare b           : %.4f m\n", b);
fprintf(fid, "Corda media aerodinamica c : %.4f m\n", c);
fprintf(fid, "Allungamento lambda        : %.4f (-)\n\n", lam);

fprintf(fid, "Prestazioni aerodinamiche\n");
fprintf(fid, "-------------------------\n");
fprintf(fid, "Cl (cro ciera)             : %.4f (-)\n", Cl);
fprintf(fid, "Cd (cro ciera)             : %.5f (-)\n", Cd);
fprintf(fid, "Efficienza Cl/Cd           : %.4f (-)\n", Eff);
fprintf(fid, "Cd0 ala (profilo)          : %.5f (-)\n", Cd0_ala);
fprintf(fid, "Cd ala                     : %.5f (-)\n", Cd_ala);
fprintf(fid, "E ala (Cl/Cd_ala)          : %.4f (-)\n\n", E_ala);

fprintf(fid, "Bilancio pesi\n");
fprintf(fid, "--------------\n");
fprintf(fid, "Peso totale W              : %.4f N\n", W);
fprintf(fid, "Spinta specifica T/S       : %.4f N/m^2\n", T_S);
fprintf(fid, "Spinta totale T            : %.4f N\n\n", T);

fprintf(fid, "Numeri adimensionali\n");
fprintf(fid, "---------------------\n");
fprintf(fid, "Reynolds ala (Rewing)      : %.4e (-)\n", Rewing);
fprintf(fid, "Mach di progetto           : %.2f (-)\n", M);
fprintf(fid, "Spessore relativo t/c      : %.2f (-)\n\n", tc);

fprintf(fid, "Note\n");
fprintf(fid, "----\n");
fprintf(fid, "I risultati sono stati aggiornati automaticamente dallo script matchingcharts.m.\n");
fclose(fid);



