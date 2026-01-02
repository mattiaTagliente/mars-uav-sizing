function results = run_analysis(varargin)
%RUN_ANALYSIS Punto di ingresso per il dimensionamento UAV Marte (MATLAB).

matlab_dir = fileparts(mfilename('fullpath'));
addpath(genpath(matlab_dir));

p = inputParser;
p.addParameter('brief', false, @(x) islogical(x) || isnumeric(x));
p.addParameter('section', 'all', @(x) ischar(x) || isstring(x));
p.addParameter('analysis', '', @(x) ischar(x) || isstring(x));
p.addParameter('figures', true, @(x) islogical(x) || isnumeric(x));
p.addParameter('figures_bilingual', false, @(x) islogical(x) || isnumeric(x));
p.addParameter('figures_lang', 'it', @(x) ischar(x) || isstring(x));
p.addParameter('figures_output_dir', fullfile(matlab_dir, 'figures'), @(x) ischar(x) || isstring(x));

p.parse(varargin{:});
args = p.Results;

verbose = ~logical(args.brief);
results = struct();

if ~isempty(args.analysis)
    switch string(args.analysis)
        case 'rotorcraft'
            mars_uav.section5.rotorcraft.print_analysis();
        case 'fixed_wing'
            mars_uav.section5.fixed_wing.print_analysis();
        case 'hybrid_vtol'
            mars_uav.section5.hybrid_vtol.print_analysis();
        case 'matching_chart'
            mars_uav.section5.matching_chart.print_analysis();
        case 'comparative'
            mars_uav.section5.comparative.print_analysis();
        case 'atmosphere'
            mars_uav.section3.atmospheric_model.print_analysis();
        case 'aerodynamics'
            mars_uav.section4.aerodynamic_calculations.print_analysis();
        case 'derived_requirements'
            mars_uav.section4.derived_requirements.print_analysis();
        case 'geometry'
            mars_uav.section4.geometry_calculations.print_analysis();
        case 'airfoil'
            mars_uav.section6.airfoil_selection.print_airfoil_comparison();
        case 'solar'
            mars_uav.section8.solar_power.print_analysis();
        case 'propeller'
            mars_uav.section6.propeller_sizing.print_analysis();
        case 'tail'
            mars_uav.section6.tail_sizing.print_analysis();
        case 'mass'
            mars_uav.section7.mass_breakdown.print_mass_breakdown();
        otherwise
            error('run_analysis:UnknownAnalysis', 'Analisi sconosciuta: %s', args.analysis);
    end
    return;
end

switch string(args.section)
    case 'all'
        results = run_all_analyses(verbose);
    case '5'
        print_header();
        results.section5 = run_section5_analyses(verbose);
    case '3'
        results.section3 = run_section3_analyses(verbose);
    case '4'
        results.section4 = run_section4_analyses(verbose);
    case '6'
        print_header();
        results.section6 = run_section6_analyses(verbose);
    case '7'
        print_header();
        results.section7 = run_section7_analyses(verbose);
    case '8'
        results.section8 = run_section8_analyses(verbose);
    otherwise
        error('run_analysis:UnknownSection', 'Sezione sconosciuta: %s', args.section);
end

if logical(args.figures)
    output_dir = char(args.figures_output_dir);
    if logical(args.figures_bilingual)
        mars_uav.visualization.plotting.generate_all_figures_bilingual(output_dir);
    else
        mars_uav.visualization.plotting.generate_all_figures(output_dir, char(args.figures_lang));
    end
end

end

function print_header()
    timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');

    fprintf('\n+%s+\n', repmat('=', 1, 78));
    fprintf('|%s|\n', center_text('STUDIO DI FATTIBILITA UAV MARTE (CASO BASE)', 78));
    fprintf('|%s|\n', center_text('Sezione 5: Analisi dei vincoli', 78));
    fprintf('|%s|\n', center_text('Modalita: DISACCOPPIATA - MTOW fissato', 78));
    fprintf('+%s+\n\n', repmat('=', 1, 78));

    fprintf('  Esecuzione analisi: %s\n', timestamp);
    fprintf('  Configurazione: Parametri da file YAML in config/\n');
    fprintf('  MTOW base: %s kg\n\n', ...
        mars_uav.core.format_number(mars_uav.config.get_param('mission.mass.mtow_kg'), 2));
end

function results = run_section5_analyses(verbose)
    results = struct();

    fprintf('\n%s\n', repmat('-', 1, 80));
    fprintf(' 5.1  ANALISI VELIVOLO A ROTORE\n');
    fprintf('%s\n\n', repmat('-', 1, 80));
    results.rotorcraft = mars_uav.section5.rotorcraft.rotorcraft_feasibility_analysis();
    if verbose
        mars_uav.section5.rotorcraft.print_analysis(results.rotorcraft);
    else
        status = '[NO]';
        if results.rotorcraft.feasible
            status = '[OK]';
        end
        fprintf('  Autonomia: %s min -> %s\n', ...
            mars_uav.core.format_number(results.rotorcraft.endurance_min, 0), status);
    end

    fprintf('\n%s\n', repmat('-', 1, 80));
    fprintf(' 5.2  ANALISI ALA FISSA\n');
    fprintf('%s\n\n', repmat('-', 1, 80));
    results.fixed_wing = mars_uav.section5.fixed_wing.fixed_wing_feasibility_analysis();
    if verbose
        mars_uav.section5.fixed_wing.print_analysis(results.fixed_wing);
    else
        status = '[NO]';
        if results.fixed_wing.feasible
            status = '[OK]';
        end
        fprintf('  Autonomia: %s min (senza VTOL) -> %s\n', ...
            mars_uav.core.format_number(results.fixed_wing.endurance_min, 0), status);
    end

    fprintf('\n%s\n', repmat('-', 1, 80));
    fprintf(' 5.3  ANALISI VTOL IBRIDO\n');
    fprintf('%s\n\n', repmat('-', 1, 80));
    results.hybrid_vtol = mars_uav.section5.hybrid_vtol.hybrid_vtol_feasibility_analysis();
    if verbose
        mars_uav.section5.hybrid_vtol.print_analysis(results.hybrid_vtol);
    else
        status = '[NO]';
        if results.hybrid_vtol.feasible
            status = '[OK]';
        end
        fprintf('  Autonomia: %s min -> %s\n', ...
            mars_uav.core.format_number(results.hybrid_vtol.endurance_min, 0), status);
    end

    fprintf('\n%s\n', repmat('-', 1, 80));
    fprintf(' 5.4  ANALISI DIAGRAMMA DI MATCHING\n');
    fprintf('%s\n\n', repmat('-', 1, 80));
    results.matching_chart = mars_uav.section5.matching_chart.matching_chart_analysis();
    if verbose
        mars_uav.section5.matching_chart.print_analysis(results.matching_chart);
    else
        dp = results.matching_chart.design_point;
        fprintf('  Punto di progetto: W/S = %s N/m^2, P/W = %s W/N\n', ...
            mars_uav.core.format_number(dp.wing_loading, 1), ...
            mars_uav.core.format_number(dp.power_loading, 1));
    end

    fprintf('\n%s\n', repmat('-', 1, 80));
    fprintf(' 5.5  ANALISI COMPARATIVA\n');
    fprintf('%s\n\n', repmat('-', 1, 80));
    results.comparative = mars_uav.section5.comparative.comparative_summary();
    if verbose
        mars_uav.section5.comparative.print_analysis(results.comparative);
    else
        fprintf('  Selezionato: %s\n', upper(strrep(results.comparative.selected, '_', ' ')));
    end
end

function results = run_section3_analyses(verbose)
    results = struct();

    fprintf('\n%s\n', repmat('-', 1, 80));
    fprintf(' 3.1  MODELLO ATMOSFERICO\n');
    fprintf('%s\n\n', repmat('-', 1, 80));
    results.atmosphere = mars_uav.section3.atmospheric_model.arcadia_planitia_conditions();
    if verbose
        mars_uav.section3.atmospheric_model.print_analysis();
    else
        fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);
        fprintf('  Densita: %s kg/m^3\n', fmt(results.atmosphere.density_kg_m3, 5));
        fprintf('  Temperatura: %s K\n', fmt(results.atmosphere.temperature_k, 1));
    end
end

function results = run_section4_analyses(verbose)
    results = struct();

    fprintf('\n%s\n', repmat('-', 1, 80));
    fprintf(' 4.7  CALCOLI AERODINAMICI\n');
    fprintf('%s\n\n', repmat('-', 1, 80));
    results.aerodynamics = mars_uav.section4.aerodynamic_calculations.drag_polar_analysis();
    if verbose
        mars_uav.section4.aerodynamic_calculations.print_analysis();
    else
        fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);
        fprintf('  (L/D)_max: %s\n', fmt(results.aerodynamics.ld_max, 2));
    end

    fprintf('\n%s\n', repmat('-', 1, 80));
    fprintf(' 4.12  REQUISITI DERIVATI\n');
    fprintf('%s\n\n', repmat('-', 1, 80));
    results.derived = mars_uav.section4.derived_requirements.derived_requirements_analysis();
    if verbose
        mars_uav.section4.derived_requirements.print_analysis();
    else
        fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);
        fprintf('  W/S (stallo): %s N/m^2\n', fmt(results.derived.stall_wing_loading, 2));
    end

    fprintf('\n%s\n', repmat('-', 1, 80));
    fprintf(' 4.5  CALCOLI GEOMETRIA\n');
    fprintf('%s\n\n', repmat('-', 1, 80));
    results.geometry = mars_uav.section4.geometry_calculations.geometry_analysis();
    if verbose
        mars_uav.section4.geometry_calculations.print_analysis();
    else
        fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);
        fprintf('  Superficie alare: %s m^2\n', fmt(results.geometry.wing_area_m2, 3));
    end
end

function results = run_section6_analyses(verbose)
    results = struct();

    fprintf('\n%s\n', repmat('-', 1, 80));
    fprintf(' 6.3a  DIMENSIONAMENTO ELICHE\n');
    fprintf('%s\n\n', repmat('-', 1, 80));
    results.propeller = mars_uav.section6.propeller_sizing.propeller_sizing_analysis();
    if verbose
        mars_uav.section6.propeller_sizing.print_analysis(results.propeller);
    else
        lift = results.propeller.lift;
        cruise = results.propeller.cruise;
        fprintf('  Eliche lift:  %sx %s in (%s)\n', ...
            mars_uav.core.format_number(lift.n_motors, 0), ...
            mars_uav.core.format_number(lift.selected_diameter_in, 1), ...
            lift.selected_model);
        fprintf('  Elica crociera: %sx %s in (%s)\n', ...
            mars_uav.core.format_number(cruise.n_motors, 0), ...
            mars_uav.core.format_number(cruise.selected_diameter_in, 1), ...
            cruise.selected_model);
    end

    fprintf('\n%s\n', repmat('-', 1, 80));
    fprintf(' 6.3b  DIMENSIONAMENTO CODA\n');
    fprintf('%s\n\n', repmat('-', 1, 80));
    results.tail = mars_uav.section6.tail_sizing.vtail_sizing();
    if verbose
        mars_uav.section6.tail_sizing.print_analysis(results.tail);
    else
        fprintf('  Area V-tail:    %s m^2\n', mars_uav.core.format_number(results.tail.S_vtail_total_m2, 3));
        fprintf('  Apertura V-tail: %s m\n', mars_uav.core.format_number(results.tail.b_vtail_m, 2));
        fprintf('  Dihedro:        %s deg\n', mars_uav.core.format_number(results.tail.dihedral_deg, 0));
    end
end

function results = run_section7_analyses(verbose)
    results = struct();

    fprintf('\n%s\n', repmat('-', 1, 80));
    fprintf(' 7.1  SELEZIONE COMPONENTI\n');
    fprintf('%s\n\n', repmat('-', 1, 80));
    if verbose
        mars_uav.section7.component_selection.print_component_selection();
    else
        selected = mars_uav.section7.component_selection.get_selected_components();
        fprintf('  Motore lift:   %s\n', selected.lift_motor.model);
        fprintf('  Motore crociera: %s\n', selected.cruise_motor.model);
    end
    results.components = mars_uav.section7.component_selection.get_selected_components();

    fprintf('\n%s\n', repmat('-', 1, 80));
    fprintf(' 7.2  SUDDIVISIONE MASSE\n');
    fprintf('%s\n\n', repmat('-', 1, 80));
    results.mass = mars_uav.section7.mass_breakdown.get_propulsion_mass_breakdown();
    if verbose
        mars_uav.section7.mass_breakdown.print_mass_breakdown();
    else
        fprintf('  Massa totale propulsione: %s kg\n', ...
            mars_uav.core.format_number(results.mass.total_kg, 3));
    end
end

function results = run_section8_analyses(verbose)
    results = struct();

    fprintf('\n%s\n', repmat('-', 1, 80));
    fprintf(' 8.1  SISTEMA SOLARE\n');
    fprintf('%s\n\n', repmat('-', 1, 80));
    results.solar = mars_uav.section8.solar_power.get_solar_system_specs();
    if verbose
        mars_uav.section8.solar_power.print_analysis();
    else
        fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);
        fprintf('  Area pannelli: %s m^2\n', fmt(results.solar.panel_area_m2, 1));
        fprintf('  Energia giornaliera: %s Wh\n', fmt(results.solar.daily_energy_wh, 0));
    end
end

function results = run_all_analyses(verbose)
    print_header();

    results = struct();

    fprintf('\n%s\n', repmat('=', 1, 80));
    fprintf(' SEZIONE 5: ANALISI DEI VINCOLI\n');
    fprintf('%s\n', repmat('=', 1, 80));
    results.section5 = run_section5_analyses(verbose);

    fprintf('\n%s\n', repmat('=', 1, 80));
    fprintf(' SEZIONE 6: SCELTE DI PROGETTO\n');
    fprintf('%s\n', repmat('=', 1, 80));
    results.section6 = run_section6_analyses(verbose);

    fprintf('\n%s\n', repmat('=', 1, 80));
    fprintf(' SEZIONE 7: SELEZIONE COMPONENTI E VERIFICA\n');
    fprintf('%s\n', repmat('=', 1, 80));
    results.section7 = run_section7_analyses(verbose);

    fprintf('\n%s\n', repmat('=', 1, 80));
    fprintf(' ANALISI COMPLETATA\n');
    fprintf('%s\n\n', repmat('=', 1, 80));

    fprintf('  Sezione 5 - Risultati configurazioni:\n');
    sec5 = results.section5;
    configs = {'rotorcraft', 'fixed_wing', 'hybrid_vtol'};
    for i = 1:numel(configs)
        config = configs{i};
        if isfield(sec5, config) && isfield(sec5.(config), 'feasible')
            if sec5.(config).feasible
                status = '[FATTIBILE]';
            else
                status = '[NON FATTIBILE]';
            end
            name = config_label(config);
            fprintf('    %-20s %s\n', name, status);
        end
    end
    fprintf('    -> Selezionato: %s\n\n', upper(strrep(config_label(sec5.comparative.selected), '_', ' ')));

    fprintf('  Sezione 6 - Geometria:\n');
    sec6 = results.section6;
    dp = sec5.matching_chart.design_point;
    geom = sec5.matching_chart.geometry;
    fprintf('    Superficie alare: %s m^2\n', mars_uav.core.format_number(geom.wing_area_m2, 3));
    fprintf('    Apertura alare:   %s m\n', mars_uav.core.format_number(geom.wingspan_m, 2));
    fprintf('    Area V-tail:      %s m^2\n\n', mars_uav.core.format_number(sec6.tail.S_vtail_total_m2, 3));

    fprintf('  Sezione 7 - Bilancio massa:\n');
    sec7 = results.section7;
    mtow = mars_uav.config.get_param('mission.mass.mtow_kg');
    prop_mass = sec7.mass.total_kg;
    f_prop = mars_uav.config.get_param('mission.mass_fractions.f_propulsion');
    prop_budget = f_prop * mtow;
    margin = prop_budget - prop_mass;
    fprintf('    MTOW:               %s kg\n', mars_uav.core.format_number(mtow, 2));
    fprintf('    Massa propulsione:  %s kg (budget: %s kg)\n', ...
        mars_uav.core.format_number(prop_mass, 3), ...
        mars_uav.core.format_number(prop_budget, 2));
    margin_text = mars_uav.core.format_number(abs(margin), 3);
    if margin >= 0
        margin_text = ['+' margin_text];
    else
        margin_text = ['-' margin_text];
    end
    fprintf('    Margine:            %s kg\n\n', margin_text);
end

function text = center_text(input, width)
    if length(input) >= width
        text = input(1:width);
        return;
    end
    padding = floor((width - length(input)) / 2);
    text = [repmat(' ', 1, padding), input, repmat(' ', 1, width - length(input) - padding)];
end

function text = title_case(name)
    parts = split(strrep(name, '_', ' '), ' ');
    parts = cellfun(@(s) [upper(s(1)), lower(s(2:end))], parts, 'UniformOutput', false);
    text = strjoin(parts, ' ');
end

function label = config_label(name)
    switch char(name)
        case 'rotorcraft'
            label = 'Velivolo a rotore';
        case 'fixed_wing'
            label = 'Ala fissa';
        case 'hybrid_vtol'
            label = 'VTOL ibrido';
        otherwise
            label = strrep(char(name), '_', ' ');
    end
end
