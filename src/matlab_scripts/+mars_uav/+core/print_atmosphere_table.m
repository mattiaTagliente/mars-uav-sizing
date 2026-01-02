function print_atmosphere_table(altitudes)
%PRINT_ATMOSPHERE_TABLE Stampa proprieta atmosferiche a varie quote.

if nargin < 1 || isempty(altitudes)
    altitudes = [-5, -3, 0, 5, 10, 15, 20];
end

atm = mars_uav.core.MarsAtmosphere();
fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);

fprintf('%s\n', repmat('=', 1, 80));
fprintf('MODELLO ATMOSFERICO MARTE (Sezione 3.1)\n');
fprintf('%s\n', repmat('=', 1, 80));
fprintf('Calcolato: %s\n', datestr(now, 'yyyy-mm-dd HH:MM:SS'));
fprintf('Config:    Parametri da config/physical_constants.yaml e mars_environment.yaml\n\n');

fprintf('%10s %10s %10s %12s %12s %10s\n', ...
    'Quota (km)', 'T (K)', 'P (Pa)', 'rho (kg/m3)', 'mu (Pa s)', 'a (m/s)');
fprintf('%s\n', repmat('-', 1, 80));

for i = 1:numel(altitudes)
    h = altitudes(i);
    state = atm.get_state(h);
    fprintf('%10s %10s %10s %12s %12s %10s\n', ...
        fmt(h, 1), ...
        fmt(state.temperature_K, 1), ...
        fmt(state.pressure_Pa, 1), ...
        fmt(state.density_kg_m3, 4), ...
        sprintf('%.2e', state.viscosity_Pa_s), ...
        fmt(state.speed_of_sound_m_s, 1));
end

fprintf('%s\n', repmat('-', 1, 80));

arcadia = mars_uav.core.get_arcadia_conditions();
fprintf('\nARCADIA PLANITIA (h = %s km):\n', fmt(arcadia.altitude_km, 1));
fprintf('  Temperatura:     %s K\n', fmt(arcadia.temperature_K, 1));
fprintf('  Pressione:       %s Pa\n', fmt(arcadia.pressure_Pa, 1));
fprintf('  Densita:         %s kg/m3\n', fmt(arcadia.density_kg_m3, 4));
fprintf('  Viscosita:       %.2e Pa s\n', arcadia.viscosity_Pa_s);
fprintf('  Velocita suono:  %s m/s\n', fmt(arcadia.speed_of_sound_m_s, 1));

config_rho = mars_uav.config.get_param('environment.arcadia_planitia.density_kg_m3');
fprintf('\n  Densita config: %s kg/m3\n', fmt(config_rho, 5));
fprintf('  Differenza:     %s kg/m3\n', fmt(abs(arcadia.density_kg_m3 - config_rho), 6));

fprintf('%s\n', repmat('=', 1, 80));
end
