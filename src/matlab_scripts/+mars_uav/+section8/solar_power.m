classdef solar_power
    %SOLAR_POWER Dimensionamento sistema solare (Sezione 8.1.4).

    methods(Static)
        function params = get_solar_irradiance_params()
            %GET_SOLAR_IRRADIANCE_PARAMS Parametri di irraggiamento su Marte.
            params = struct( ...
                'solar_constant_w_m2', mars_uav.config.get_param('environment.solar.constant_mars'), ...
                'perihelion_w_m2', mars_uav.config.get_param('environment.solar.perihelion'), ...
                'aphelion_w_m2', mars_uav.config.get_param('environment.solar.aphelion'), ...
                'surface_clear_w_m2', mars_uav.config.get_param('environment.solar.surface_clear_noon'), ...
                'design_irradiance_w_m2', mars_uav.config.get_param('environment.solar.surface_aphelion_dusty'), ...
                'effective_sun_hours', mars_uav.config.get_param('environment.solar.effective_sun_hours'), ...
                'avg_incidence_factor', mars_uav.config.get_param('environment.solar.avg_incidence_factor') ...
            );
        end

        function capacity_wh = get_uav_battery_capacity()
            %GET_UAV_BATTERY_CAPACITY Capacita batteria UAV da config.
            mtow = mars_uav.config.get_param('mission.mass.mtow_kg');
            f_battery = mars_uav.config.get_param('mission.mass_fractions.f_battery');
            battery_mass = f_battery * mtow;
            specific_energy = mars_uav.config.get_param('battery.specifications.specific_energy_Wh_kg');
            capacity_wh = battery_mass * specific_energy;
        end

        function panel = get_solar_panel_sizing()
            %GET_SOLAR_PANEL_SIZING Dimensionamento pannelli solari.
            cell_efficiency = 0.33;
            cell_mass_kg_m2 = 0.49;

            irrad = mars_uav.section8.solar_power.get_solar_irradiance_params();
            surface_irradiance = irrad.design_irradiance_w_m2;

            peak_power_w_m2 = cell_efficiency * surface_irradiance;
            daily_energy_wh_m2 = peak_power_w_m2 * irrad.effective_sun_hours * irrad.avg_incidence_factor;

            batt_capacity = mars_uav.section8.solar_power.get_uav_battery_capacity();
            depth_of_discharge = mars_uav.config.get_param('battery.utilization.depth_of_discharge');
            charger_efficiency = 0.90;

            energy_per_charge = batt_capacity * depth_of_discharge;
            energy_required = energy_per_charge / charger_efficiency;

            panel_area_min = energy_required / daily_energy_wh_m2;
            design_margin = 1.5;
            panel_area_design = panel_area_min * design_margin;
            panel_area_design = ceil(panel_area_design * 2) / 2;

            panel_mass = panel_area_design * cell_mass_kg_m2;

            panel = struct( ...
                'cell_efficiency', cell_efficiency, ...
                'surface_irradiance_w_m2', surface_irradiance, ...
                'peak_power_w_m2', peak_power_w_m2, ...
                'daily_energy_wh_m2', daily_energy_wh_m2, ...
                'energy_required_wh', energy_required, ...
                'panel_area_min_m2', panel_area_min, ...
                'design_margin', design_margin, ...
                'panel_area_design_m2', panel_area_design, ...
                'panel_mass_kg', panel_mass ...
            );
        end

        function buffer = get_buffer_battery_sizing()
            %GET_BUFFER_BATTERY_SIZING Dimensionamento batteria buffer.
            batt_capacity = mars_uav.section8.solar_power.get_uav_battery_capacity();
            depth_of_discharge = mars_uav.config.get_param('battery.utilization.depth_of_discharge');

            energy_per_charge = batt_capacity * depth_of_discharge;
            charger_efficiency = 0.90;
            energy_from_buffer = energy_per_charge / charger_efficiency;

            night_reserve_factor = 1.5;
            buffer_capacity = energy_from_buffer * night_reserve_factor;

            battery_energy_density = mars_uav.config.get_param('battery.specifications.specific_energy_Wh_kg');
            buffer_mass = buffer_capacity / battery_energy_density;

            rationale = [ ...
                'Stessa tecnologia batteria UAV (solid-state Li-ion, 270 Wh/kg) ', ...
                'per semplificare logistica e compatibilita termica.' ...
            ];

            buffer = struct( ...
                'uav_battery_capacity_wh', batt_capacity, ...
                'energy_per_charge_wh', energy_per_charge, ...
                'charger_efficiency', charger_efficiency, ...
                'energy_from_buffer_wh', energy_from_buffer, ...
                'night_reserve_factor', night_reserve_factor, ...
                'buffer_capacity_wh', buffer_capacity, ...
                'battery_energy_density_wh_kg', battery_energy_density, ...
                'buffer_mass_kg', buffer_mass, ...
                'rationale', rationale ...
            );
        end

        function charging = get_charging_infrastructure()
            %GET_CHARGING_INFRASTRUCTURE Specifiche di ricarica.
            batt_capacity = mars_uav.section8.solar_power.get_uav_battery_capacity();
            depth_of_discharge = mars_uav.config.get_param('battery.utilization.depth_of_discharge');

            energy_to_replenish = batt_capacity * depth_of_discharge;
            target_charge_time_h = 2.0;

            charger_power_0_5c = batt_capacity * 0.5;
            charger_power_1c = batt_capacity * 1.0;
            specified_charger_w = 1000.0;

            charging = struct( ...
                'uav_battery_capacity_wh', batt_capacity, ...
                'energy_to_replenish_wh', energy_to_replenish, ...
                'target_charge_time_h', target_charge_time_h, ...
                'charger_power_0_5c_w', charger_power_0_5c, ...
                'charger_power_1c_w', charger_power_1c, ...
                'specified_charger_w', specified_charger_w ...
            );
        end

        function specs = get_solar_system_specs()
            %GET_SOLAR_SYSTEM_SPECS Specifiche complete sistema solare.
            panel = mars_uav.section8.solar_power.get_solar_panel_sizing();
            buffer = mars_uav.section8.solar_power.get_buffer_battery_sizing();

            peak_power = panel.panel_area_design_m2 * panel.peak_power_w_m2;
            daily_energy = panel.panel_area_design_m2 * panel.daily_energy_wh_m2;
            excess_energy = daily_energy - buffer.buffer_capacity_wh;

            specs = struct( ...
                'cell_technology', 'SolAero IMM-3J', ...
                'cell_efficiency_pct', panel.cell_efficiency * 100, ...
                'cell_mass_kg_m2', 0.49, ...
                'panel_area_m2', panel.panel_area_design_m2, ...
                'peak_power_w', peak_power, ...
                'daily_energy_wh', daily_energy, ...
                'panel_mass_kg', panel.panel_mass_kg, ...
                'buffer_capacity_wh', buffer.buffer_capacity_wh, ...
                'buffer_mass_kg', buffer.buffer_mass_kg, ...
                'buffer_technology', 'Solid-state Li-ion (come UAV)', ...
                'mounting', 'Tetto habitat, tilt fisso', ...
                'excess_energy_wh', excess_energy ...
            );
        end

        function print_analysis()
            %PRINT_ANALYSIS Stampa analisi completa sistema solare.
            fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);
            timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');

            fprintf('%s\n', repmat('=', 1, 70));
            fprintf('ANALISI SISTEMA SOLARE (Sezione 8.1.4)\n');
            fprintf('%s\n', repmat('=', 1, 70));
            fprintf('Calcolato: %s\n', timestamp);
            fprintf('Config:    Parametri da file YAML in config/\n');

            irrad = mars_uav.section8.solar_power.get_solar_irradiance_params();
            fprintf('\nIRRAGGIAMENTO SOLARE MARTE\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Costante solare Marte:    %s W/m^2\n', fmt(irrad.solar_constant_w_m2, 0));
            fprintf('  Perielio:                 %s W/m^2\n', fmt(irrad.perihelion_w_m2, 0));
            fprintf('  Afelio:                   %s W/m^2\n', fmt(irrad.aphelion_w_m2, 0));
            fprintf('  Superficie sereno:        %s W/m^2 (non per progetto)\n', fmt(irrad.surface_clear_w_m2, 0));
            fprintf('  Irraggiamento progetto:   %s W/m^2 (base sizing)\n', fmt(irrad.design_irradiance_w_m2, 0));
            fprintf('  Ore sole efficaci:        %s h/sol\n', fmt(irrad.effective_sun_hours, 0));
            fprintf('  Fattore incidenza medio:  %s\n', fmt(irrad.avg_incidence_factor, 1));

            panel = mars_uav.section8.solar_power.get_solar_panel_sizing();
            fprintf('\nDIMENSIONAMENTO PANNELLI\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Tecnologia celle:         SolAero IMM-3J\n');
            fprintf('  Efficienza celle:         %s %%\n', fmt(panel.cell_efficiency * 100, 0));
            fprintf('  Irraggiamento progetto:   %s W/m^2\n', fmt(panel.surface_irradiance_w_m2, 0));
            fprintf('  Potenza di picco:         %s W/m^2\n', fmt(panel.peak_power_w_m2, 1));
            fprintf('  Energia giornaliera:      %s Wh/m^2/sol\n', fmt(panel.daily_energy_wh_m2, 1));
            fprintf('  Energia richiesta:        %s Wh\n', fmt(panel.energy_required_wh, 0));
            fprintf('  Area minima:              %s m^2\n', fmt(panel.panel_area_min_m2, 2));
            fprintf('  Margine progetto:         x%s\n', fmt(panel.design_margin, 2));
            fprintf('  Area progetto:            %s m^2\n', fmt(panel.panel_area_design_m2, 1));
            fprintf('  Massa pannelli:           %s kg\n', fmt(panel.panel_mass_kg, 2));

            buffer = mars_uav.section8.solar_power.get_buffer_battery_sizing();
            fprintf('\nBATTERIA BUFFER\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Capacita batteria UAV:    %s Wh\n', fmt(buffer.uav_battery_capacity_wh, 0));
            fprintf('  Energia per carica:       %s Wh\n', fmt(buffer.energy_per_charge_wh, 0));
            fprintf('  Efficienza caricatore:    %s %%\n', fmt(buffer.charger_efficiency * 100, 0));
            fprintf('  Energia da buffer:        %s Wh\n', fmt(buffer.energy_from_buffer_wh, 0));
            fprintf('  Fattore riserva notte:    x%s\n', fmt(buffer.night_reserve_factor, 1));
            fprintf('  Capacita buffer:          %s Wh\n', fmt(buffer.buffer_capacity_wh, 0));
            fprintf('  Densita energia:          %s Wh/kg\n', fmt(buffer.battery_energy_density_wh_kg, 0));
            fprintf('  Massa buffer:             %s kg\n', fmt(buffer.buffer_mass_kg, 2));
            fprintf('  Decisione: %s\n', buffer.rationale);

            charging = mars_uav.section8.solar_power.get_charging_infrastructure();
            fprintf('\nINFRASTRUTTURA RICARICA\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Capacita batteria UAV:    %s Wh\n', fmt(charging.uav_battery_capacity_wh, 0));
            fprintf('  Energia da reintegrare:   %s Wh\n', fmt(charging.energy_to_replenish_wh, 0));
            fprintf('  Tempo carica target:      %s h\n', fmt(charging.target_charge_time_h, 1));
            fprintf('  Potenza @0.5C:            %s W\n', fmt(charging.charger_power_0_5c_w, 0));
            fprintf('  Potenza @1C:              %s W\n', fmt(charging.charger_power_1c_w, 0));
            fprintf('  Caricatore specificato:   %s W\n', fmt(charging.specified_charger_w, 0));

            specs = mars_uav.section8.solar_power.get_solar_system_specs();
            fprintf('\nSINTESI SISTEMA\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Tecnologia celle:         %s\n', specs.cell_technology);
            fprintf('  Efficienza celle:         %s %%\n', fmt(specs.cell_efficiency_pct, 0));
            fprintf('  Area pannelli:            %s m^2\n', fmt(specs.panel_area_m2, 1));
            fprintf('  Potenza picco:            %s W\n', fmt(specs.peak_power_w, 0));
            fprintf('  Energia giornaliera:      %s Wh/sol\n', fmt(specs.daily_energy_wh, 0));
            fprintf('  Massa pannelli:           %s kg\n', fmt(specs.panel_mass_kg, 2));
            fprintf('  Capacita buffer:          %s Wh\n', fmt(specs.buffer_capacity_wh, 0));
            fprintf('  Massa buffer:             %s kg\n', fmt(specs.buffer_mass_kg, 2));
            fprintf('  Tecnologia buffer:        %s\n', specs.buffer_technology);
            fprintf('  Montaggio:                %s\n', specs.mounting);
            fprintf('  Energia in eccesso:       %s Wh/sol\n', fmt(specs.excess_energy_wh, 0));

            fprintf('\nBILANCIO ENERGETICO GIORNALIERO\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Generazione:              %s Wh\n', fmt(specs.daily_energy_wh, 0));
            fprintf('  Accumulo buffer:          %s Wh\n', fmt(specs.buffer_capacity_wh, 0));
            fprintf('  Energia a UAV:            %s Wh\n', fmt(buffer.energy_from_buffer_wh, 0));
            fprintf('  Eccesso verso habitat:    %s Wh\n', fmt(specs.excess_energy_wh, 0));
            fprintf('%s\n', repmat('=', 1, 70));
        end
    end
end
