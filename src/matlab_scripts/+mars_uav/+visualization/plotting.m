classdef plotting
    %PLOTTING Funzioni di visualizzazione.

    methods(Static)
        function text = get_text(key, lang)
            if nargin < 2 || isempty(lang)
                lang = 'it';
            end
            translations = mars_uav.visualization.plotting.translations();
            if isfield(translations, lang) && isfield(translations.(lang), key)
                text = translations.(lang).(key);
            else
                text = key;
            end
        end

        function plot_constraint_diagram(ws_range, pw_hover, pw_cruise, ws_stall, design_point, title_text, save_path, show, lang)
            if nargin < 9 || isempty(lang)
                lang = 'it';
            end
            if nargin < 8 || isempty(show)
                show = true;
            end
            if nargin < 7
                save_path = '';
            end
            if nargin < 6 || isempty(title_text)
                title_text = mars_uav.visualization.plotting.get_text('matching_chart_title', lang);
            end
            if nargin < 1 || isempty(ws_range)
                ws_range = linspace(2, 15, 100);
            end
            if nargin < 2 || isempty(pw_hover)
                pw_hover = mars_uav.section5.matching_chart.hover_constraint();
            end
            if nargin < 3 || isempty(pw_cruise)
                pw_cruise = mars_uav.section5.matching_chart.cruise_constraint_curve(ws_range);
            end
            if nargin < 4 || isempty(ws_stall)
                ws_stall = mars_uav.section5.matching_chart.stall_constraint();
            end
            if nargin < 5 || isempty(design_point)
                dp = mars_uav.section5.matching_chart.find_design_point();
                design_point = [dp.wing_loading, dp.power_loading];
            end

            fig = mars_uav.visualization.plotting.create_figure(show);
            hold on;

            ymax = pw_hover * 1.8;
            fill([ws_range, fliplr(ws_range)], ...
                [pw_hover * ones(size(ws_range)), ymax * ones(size(ws_range))], ...
                [1 0.6 0.6], 'FaceAlpha', 0.1, 'EdgeColor', 'none', 'HandleVisibility', 'off');
            fill([ws_stall, ws_range(end), ws_range(end), ws_stall], ...
                [0, 0, ymax, ymax], [0.6 1 0.6], 'FaceAlpha', 0.1, 'EdgeColor', 'none', 'HandleVisibility', 'off');

            h_cruise = plot(ws_range, pw_cruise, 'b-', 'LineWidth', 2);
            h_hover = yline(pw_hover, 'r-', 'LineWidth', 2);
            h_stall = xline(ws_stall, 'g--', 'LineWidth', 2);
            h_design = plot(design_point(1), design_point(2), 'k*', 'MarkerSize', 12, 'LineWidth', 1.5);

            xlabel(mars_uav.visualization.plotting.get_text('wing_loading', lang));
            ylabel(mars_uav.visualization.plotting.get_text('power_loading', lang));
            title(title_text, 'FontWeight', 'bold');
            legend([h_cruise h_hover h_stall h_design], {
                mars_uav.visualization.plotting.get_text('cruise_constraint', lang), ...
                mars_uav.visualization.plotting.get_text('hover_constraint', lang), ...
                mars_uav.visualization.plotting.get_text('stall_limit', lang), ...
                mars_uav.visualization.plotting.get_text('design_point', lang)
            }, 'Location', 'northeast');
            grid on;
            xlim([0, ws_range(end) * 1.1]);
            ylim([0, ymax]);

            text(ws_stall/2, pw_hover * 1.05, mars_uav.visualization.plotting.get_text('feasible_region', lang), ...
                'HorizontalAlignment', 'center');

            hold off;

            if ~isempty(save_path)
                mars_uav.visualization.plotting.save_figure(fig, save_path);
            end
            if ~show
                close(fig);
            end
        end

        function plot_rotorcraft_matching_chart(title_text, save_path, show, lang)
            if nargin < 4 || isempty(lang)
                lang = 'it';
            end
            if nargin < 3 || isempty(show)
                show = true;
            end
            if nargin < 2
                save_path = '';
            end
            if nargin < 1 || isempty(title_text)
                title_text = mars_uav.visualization.plotting.get_text('matching_chart_rotorcraft_title', lang);
            end

            rho = mars_uav.config.get_density();
            prop = mars_uav.config.get_propulsion_efficiencies();
            eta_hover = prop.figure_of_merit * prop.eta_motor * prop.eta_esc;

            dl_range = linspace(10, 100, 100);
            pw_hover = (1 / eta_hover) * sqrt(dl_range / (2 * rho));

            dl_design = mars_uav.config.get_param('geometry.rotor.disk_loading_N_m2');
            pw_design = (1 / eta_hover) * sqrt(dl_design / (2 * rho));

            fig = mars_uav.visualization.plotting.create_figure(show);
            hold on;

            h_hover = plot(dl_range, pw_hover, 'r-', 'LineWidth', 2.5);
            h_design = plot(dl_design, pw_design, 'k*', 'MarkerSize', 12, 'LineWidth', 1.5);

            ymax = max(pw_hover) * 1.2;
            fill([dl_range, fliplr(dl_range)], ...
                [pw_hover, ymax * ones(size(dl_range))], ...
                [1 0.6 0.6], 'FaceAlpha', 0.1, 'EdgeColor', 'none', 'HandleVisibility', 'off');

            xlabel(mars_uav.visualization.plotting.get_text('disk_loading', lang));
            ylabel(mars_uav.visualization.plotting.get_text('power_loading', lang));
            title(title_text, 'FontWeight', 'bold');
            legend([h_hover h_design], {
                mars_uav.visualization.plotting.get_text('hover_constraint', lang), ...
                mars_uav.visualization.plotting.get_text('design_point', lang)
            }, 'Location', 'northwest');
            grid on;
            xlim([0, dl_range(end) * 1.1]);
            ylim([0, ymax]);

            text(dl_range(end) * 0.7, max(pw_hover) * 1.05, ...
                mars_uav.visualization.plotting.get_text('feasible_region', lang), ...
                'HorizontalAlignment', 'center');

            hold off;

            if ~isempty(save_path)
                mars_uav.visualization.plotting.save_figure(fig, save_path);
            end
            if ~show
                close(fig);
            end
        end

        function plot_fixed_wing_matching_chart(title_text, save_path, show, lang)
            if nargin < 4 || isempty(lang)
                lang = 'it';
            end
            if nargin < 3 || isempty(show)
                show = true;
            end
            if nargin < 2
                save_path = '';
            end
            if nargin < 1 || isempty(title_text)
                title_text = mars_uav.visualization.plotting.get_text('matching_chart_fixed_wing_title', lang);
            end

            rho = mars_uav.config.get_density();
            mission = mars_uav.config.get_mission_params();
            aero = mars_uav.config.get_aerodynamic_params();

            v_cruise = mission.v_cruise;
            v_stall = mission.v_stall;
            v_min_factor = mars_uav.config.get_param('mission.velocity.v_min_factor');
            v_min = v_stall * v_min_factor;
            cl_max = aero.cl_max;

            ws_range = linspace(2, 15, 100);
            pw_cruise = zeros(size(ws_range));

            for i = 1:numel(ws_range)
                cl = mars_uav.section5.fixed_wing.cruise_lift_coefficient(ws_range(i), rho, v_cruise);
                ld = mars_uav.section5.fixed_wing.lift_to_drag(cl);
                pw_cruise(i) = mars_uav.section5.fixed_wing.cruise_power_loading(v_cruise, ld);
            end

            ws_stall = mars_uav.section5.fixed_wing.stall_wing_loading_limit(rho, v_min, cl_max);
            cl_design = mars_uav.section5.fixed_wing.cruise_lift_coefficient(ws_stall, rho, v_cruise);
            ld_design = mars_uav.section5.fixed_wing.lift_to_drag(cl_design);
            pw_design = mars_uav.section5.fixed_wing.cruise_power_loading(v_cruise, ld_design);

            fig = mars_uav.visualization.plotting.create_figure(show);
            hold on;

            plot(ws_range, pw_cruise, 'b-', 'LineWidth', 2);
            xline(ws_stall, 'g--', 'LineWidth', 2);
            plot(ws_stall, pw_design, 'k*', 'MarkerSize', 12, 'LineWidth', 1.5);

            fill([ws_stall, ws_range(end), ws_range(end), ws_stall], ...
                [0, 0, max(pw_cruise) * 1.3, max(pw_cruise) * 1.3], ...
                [0.6 1 0.6], 'FaceAlpha', 0.1, 'EdgeColor', 'none');

            xlabel(mars_uav.visualization.plotting.get_text('wing_loading', lang));
            ylabel(mars_uav.visualization.plotting.get_text('power_loading', lang));
            title(title_text, 'FontWeight', 'bold');
            legend({
                mars_uav.visualization.plotting.get_text('cruise_constraint', lang), ...
                mars_uav.visualization.plotting.get_text('stall_limit', lang), ...
                mars_uav.visualization.plotting.get_text('design_point', lang)
            }, 'Location', 'northeast');
            grid on;
            xlim([0, ws_range(end) * 1.1]);
            ylim([0, max(pw_cruise) * 1.3]);

            text(ws_stall / 2, max(pw_cruise) * 0.9, ...
                mars_uav.visualization.plotting.get_text('feasible_region', lang), ...
                'HorizontalAlignment', 'center');

            hold off;

            if ~isempty(save_path)
                mars_uav.visualization.plotting.save_figure(fig, save_path);
            end
            if ~show
                close(fig);
            end
        end

        function plot_power_comparison(results, save_path, show, lang)
            if nargin < 4 || isempty(lang)
                lang = 'it';
            end
            if nargin < 3 || isempty(show)
                show = true;
            end
            if nargin < 2
                save_path = '';
            end
            if nargin < 1 || isempty(results)
                results = mars_uav.section5.comparative.run_all_analyses();
            end

            configs = { ...
                mars_uav.visualization.plotting.get_text('rotorcraft', lang), ...
                mars_uav.visualization.plotting.get_text('fixed_wing', lang), ...
                mars_uav.visualization.plotting.get_text('hybrid_vtol', lang)
            };

            hover_power = [ ...
                results.rotorcraft.hover_power_w, ...
                0, ...
                results.hybrid_vtol.hover_power_w ...
            ];

            cruise_power = [ ...
                results.rotorcraft.cruise_power_w, ...
                results.fixed_wing.cruise_power_w, ...
                results.hybrid_vtol.cruise_power_w ...
            ];

            fig = mars_uav.visualization.plotting.create_figure(show);
            hold on;

            x = 1:numel(configs);
            width = 0.35;

            b1 = bar(x - width/2, hover_power, width, 'FaceColor', [1 0.6 0.4]);
            b2 = bar(x + width/2, cruise_power, width, 'FaceColor', [0.3 0.5 0.8]);

            xlabel(mars_uav.visualization.plotting.get_text('configuration', lang));
            ylabel(mars_uav.visualization.plotting.get_text('power_ylabel', lang));
            title(mars_uav.visualization.plotting.get_text('power_title', lang), 'FontWeight', 'bold');
            set(gca, 'XTick', x, 'XTickLabel', configs);
            legend([b1 b2], {mars_uav.visualization.plotting.get_text('hover_power', lang), ...
                mars_uav.visualization.plotting.get_text('cruise_power', lang)}, 'Location', 'northwest');
            grid on;

            max_power = max([hover_power, cruise_power]);
            ylim([0, max_power * 1.25]);

            mars_uav.visualization.plotting.add_bar_labels(b1);
            mars_uav.visualization.plotting.add_bar_labels(b2);

            hold off;

            if ~isempty(save_path)
                mars_uav.visualization.plotting.save_figure(fig, save_path);
            end
            if ~show
                close(fig);
            end
        end

        function plot_endurance_comparison(results, save_path, show, lang)
            if nargin < 4 || isempty(lang)
                lang = 'it';
            end
            if nargin < 3 || isempty(show)
                show = true;
            end
            if nargin < 2
                save_path = '';
            end
            if nargin < 1 || isempty(results)
                results = mars_uav.section5.comparative.run_all_analyses();
            end

            configs = { ...
                mars_uav.visualization.plotting.get_text('rotorcraft', lang), ...
                mars_uav.visualization.plotting.get_text('fixed_wing_no_vtol', lang), ...
                mars_uav.visualization.plotting.get_text('hybrid_vtol', lang)
            };

            endurance = [ ...
                results.rotorcraft.endurance_min, ...
                results.fixed_wing.endurance_min, ...
                results.hybrid_vtol.endurance_min ...
            ];

            colors = [1 0.6 0.6; 1 0.6 0.6; 0.6 1 0.6];

            fig = mars_uav.visualization.plotting.create_figure(show);
            bar_handle = bar(endurance, 'FaceColor', 'flat');
            bar_handle.CData = colors;

            hold on;
            yline(60, 'r--', 'LineWidth', 2);
            hold off;

            ylabel(mars_uav.visualization.plotting.get_text('endurance_ylabel', lang));
            title(mars_uav.visualization.plotting.get_text('endurance_title', lang), 'FontWeight', 'bold');
            set(gca, 'XTick', 1:numel(configs), 'XTickLabel', configs);
            grid on;

            max_endurance = max(endurance);
            ylim([0, max_endurance * 1.15]);

            if ~isempty(save_path)
                mars_uav.visualization.plotting.save_figure(fig, save_path);
            end
            if ~show
                close(fig);
            end
        end

        function plot_energy_budget(results, save_path, show, lang)
            if nargin < 4 || isempty(lang)
                lang = 'it';
            end
            if nargin < 3 || isempty(show)
                show = true;
            end
            if nargin < 2
                save_path = '';
            end
            if nargin < 1 || isempty(results)
                results = mars_uav.section5.comparative.run_all_analyses();
            end

            hyb = results.hybrid_vtol;

            hover_energy = hyb.hover_energy_wh;
            cruise_energy = hyb.cruise_energy_wh;
            reserve_energy = hyb.reserve_energy_wh;
            available_energy = hyb.usable_energy_wh;

            fig = mars_uav.visualization.plotting.create_figure(show);
            hold on;

            categories = { ...
                mars_uav.visualization.plotting.get_text('required', lang), ...
                mars_uav.visualization.plotting.get_text('available', lang)
            };

            bar_data = [hover_energy, cruise_energy, reserve_energy, 0; ...
                        0, 0, 0, available_energy];

            b = bar(bar_data, 'stacked');
            b(1).FaceColor = [1 0.6 0.4];
            b(2).FaceColor = [0.3 0.5 0.8];
            b(3).FaceColor = [0.95 0.8 0.2];
            b(4).FaceColor = [0.6 1 0.6];

            set(gca, 'XTick', 1:2, 'XTickLabel', categories);
            ylabel(mars_uav.visualization.plotting.get_text('energy_ylabel', lang));
            title(mars_uav.visualization.plotting.get_text('energy_budget_title', lang), 'FontWeight', 'bold');
            legend(b, { ...
                mars_uav.visualization.plotting.get_text('hover_label', lang), ...
                mars_uav.visualization.plotting.get_text('cruise', lang), ...
                mars_uav.visualization.plotting.get_text('reserve_label', lang), ...
                mars_uav.visualization.plotting.get_text('available', lang) ...
            }, 'Location', 'northwest');
            grid on;

            max_energy = max(available_energy, hover_energy + cruise_energy + reserve_energy);
            ylim([0, max_energy * 1.25]);

            total_required = hover_energy + cruise_energy + reserve_energy;
            text(1, total_required, sprintf('%s Wh', mars_uav.core.format_number(total_required, 0)), ...
                'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom', 'FontWeight', 'bold');
            text(2, available_energy, sprintf('%s Wh', mars_uav.core.format_number(available_energy, 0)), ...
                'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom', 'FontWeight', 'bold');

            margin_pct = (available_energy - total_required) / total_required * 100;
            margin_text = mars_uav.core.format_number(abs(margin_pct), 0);
            if margin_pct >= 0
                margin_text = ['+' margin_text];
            else
                margin_text = ['-' margin_text];
            end
            text(1.5, (total_required + available_energy) / 2, ...
                sprintf('%s: %s%%', mars_uav.visualization.plotting.get_text('margin', lang), margin_text), ...
                'HorizontalAlignment', 'center', 'FontWeight', 'bold');

            hold off;

            if ~isempty(save_path)
                mars_uav.visualization.plotting.save_figure(fig, save_path);
            end
            if ~show
                close(fig);
            end
        end

        function plot_ld_comparison(results, save_path, show, lang)
            if nargin < 4 || isempty(lang)
                lang = 'it';
            end
            if nargin < 3 || isempty(show)
                show = true;
            end
            if nargin < 2
                save_path = '';
            end
            if nargin < 1 || isempty(results)
                results = mars_uav.section5.comparative.run_all_analyses();
            end

            configs = { ...
                mars_uav.visualization.plotting.get_text('rotorcraft_equiv', lang), ...
                mars_uav.visualization.plotting.get_text('fixed_wing_pure', lang), ...
                mars_uav.visualization.plotting.get_text('hybrid_vtol_qp', lang)
            };
            ld_values = [ ...
                results.rotorcraft.ld_effective, ...
                results.fixed_wing.ld_max, ...
                results.hybrid_vtol.ld_quadplane ...
            ];

            fig = mars_uav.visualization.plotting.create_figure(show);
            bar_handle = bar(ld_values, 'FaceColor', 'flat');
            bar_handle.CData = [1 0.6 0.6; 0.6 1 0.6; 0.3 0.5 0.8];

            ylabel(mars_uav.visualization.plotting.get_text('ld_ylabel', lang));
            title(mars_uav.visualization.plotting.get_text('ld_title', lang), 'FontWeight', 'bold');
            set(gca, 'XTick', 1:numel(configs), 'XTickLabel', configs);
            grid on;

            max_ld = max(ld_values);
            ylim([0, max_ld * 1.15]);

            for i = 1:numel(ld_values)
                text(i, ld_values(i), mars_uav.core.format_number(ld_values(i), 1), ...
                    'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom', 'FontWeight', 'bold');
            end

            if ~isempty(save_path)
                mars_uav.visualization.plotting.save_figure(fig, save_path);
            end
            if ~show
                close(fig);
            end
        end

        function generate_all_figures(output_dir, lang)
            if nargin < 2 || isempty(lang)
                lang = 'it';
            end
            if nargin < 1 || isempty(output_dir)
                output_dir = fullfile(pwd, 'figures');
            end

            if exist(output_dir, 'dir') ~= 7
                mkdir(output_dir);
            end

            suffix = '';
            if ~strcmp(lang, 'en')
                suffix = ['_' lang];
            end

            fprintf('Generazione figure (%s)...\n', upper(lang));

            mars_uav.visualization.plotting.plot_constraint_diagram([], [], [], [], [], [], ...
                fullfile(output_dir, ['matching_chart' suffix '.png']), false, lang);

            mars_uav.visualization.plotting.plot_rotorcraft_matching_chart([], ...
                fullfile(output_dir, ['matching_chart_rotorcraft' suffix '.png']), false, lang);

            mars_uav.visualization.plotting.plot_fixed_wing_matching_chart([], ...
                fullfile(output_dir, ['matching_chart_fixed_wing' suffix '.png']), false, lang);

            mars_uav.visualization.plotting.plot_power_comparison([], ...
                fullfile(output_dir, ['power_comparison' suffix '.png']), false, lang);

            mars_uav.visualization.plotting.plot_endurance_comparison([], ...
                fullfile(output_dir, ['endurance_comparison' suffix '.png']), false, lang);

            mars_uav.visualization.plotting.plot_energy_budget([], ...
                fullfile(output_dir, ['energy_budget' suffix '.png']), false, lang);

            mars_uav.visualization.plotting.plot_ld_comparison([], ...
                fullfile(output_dir, ['ld_comparison' suffix '.png']), false, lang);

            mars_uav.section6.airfoil_plots.generate_all_airfoil_figures(output_dir, false, lang);

            fprintf('Tutte le figure (%s) salvate in %s\n', upper(lang), output_dir);
        end

        function generate_all_figures_bilingual(output_dir)
            if nargin < 1 || isempty(output_dir)
                output_dir = fullfile(pwd, 'figures');
            end
            mars_uav.visualization.plotting.generate_all_figures(output_dir, 'en');
            mars_uav.visualization.plotting.generate_all_figures(output_dir, 'it');
            fprintf('Generazione figure bilingue completata.\n');
        end

        function fig = create_figure(show)
            if show
                fig = figure('Color', 'w');
            else
                fig = figure('Visible', 'off', 'Color', 'w');
            end
        end

        function save_figure(fig, save_path)
            [folder, name, ext] = fileparts(save_path);
            if isempty(folder)
                folder = pwd;
            end
            if exist(folder, 'dir') ~= 7
                mkdir(folder);
            end

            if isempty(ext)
                png_path = fullfile(folder, [name '.png']);
            else
                png_path = save_path;
                name = name;
            end
            fig_path = fullfile(folder, [name '.fig']);

            if exist('exportgraphics', 'file') == 2
                exportgraphics(fig, png_path, 'Resolution', 300);
            else
                saveas(fig, png_path);
            end
            savefig(fig, fig_path);

            fprintf('Salvato: %s\n', png_path);
            fprintf('Salvato: %s\n', fig_path);
        end

        function add_bar_labels(bar_handle)
            for i = 1:numel(bar_handle)
                b = bar_handle(i);
                x = b.XEndPoints;
                y = b.YEndPoints;
                for j = 1:numel(x)
                    if y(j) > 0
                        text(x(j), y(j), mars_uav.core.format_number(y(j), 0), ...
                            'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom');
                    end
                end
            end
        end

        function translations = translations()
            translations.en = struct( ...
                'matching_chart_title', 'Matching Chart - Mars UAV', ...
                'matching_chart_rotorcraft_title', 'Matching Chart - Rotorcraft', ...
                'matching_chart_fixed_wing_title', 'Matching Chart - Fixed-Wing', ...
                'hover_constraint', 'Hover constraint', ...
                'stall_limit', 'Stall limit', ...
                'cruise_constraint', 'Cruise constraint', ...
                'design_point', 'Design point', ...
                'feasible_region', 'Feasible Region', ...
                'wing_loading', 'Wing Loading W/S (N/m^2)', ...
                'power_loading', 'Power Loading P/W (W/N)', ...
                'disk_loading', 'Disk Loading DL (N/m^2)', ...
                'power_title', 'Power Requirements by Configuration', ...
                'hover_power', 'Hover Power', ...
                'cruise_power', 'Cruise Power', ...
                'power_ylabel', 'Power (W)', ...
                'configuration', 'Configuration', ...
                'endurance_title', 'Endurance by Configuration', ...
                'endurance_ylabel', 'Endurance (min)', ...
                'requirement', 'Requirement', ...
                'energy_budget_title', 'Hybrid VTOL Energy Budget', ...
                'energy_ylabel', 'Energy (Wh)', ...
                'hover_label', 'Hover', ...
                'cruise', 'Cruise', ...
                'reserve_label', 'Reserve', ...
                'available', 'Available', ...
                'required', 'Required', ...
                'margin', 'Margin', ...
                'ld_title', 'Aerodynamic Efficiency by Configuration', ...
                'ld_ylabel', 'Lift-to-Drag Ratio (L/D)', ...
                'rotorcraft', 'Rotorcraft', ...
                'fixed_wing', 'Fixed-Wing', ...
                'fixed_wing_no_vtol', 'Fixed-Wing (no VTOL)', ...
                'hybrid_vtol', 'Hybrid VTOL', ...
                'rotorcraft_equiv', 'Rotorcraft (equivalent)', ...
                'fixed_wing_pure', 'Fixed-Wing (pure)', ...
                'hybrid_vtol_qp', 'Hybrid VTOL (QuadPlane)' ...
            );

            translations.it = struct( ...
                'matching_chart_title', 'Diagramma di Matching - UAV Marte', ...
                'matching_chart_rotorcraft_title', 'Diagramma di Matching - Velivolo a rotore', ...
                'matching_chart_fixed_wing_title', 'Diagramma di Matching - Ala fissa', ...
                'hover_constraint', 'Vincolo di hovering', ...
                'stall_limit', 'Limite di stallo', ...
                'cruise_constraint', 'Vincolo crociera', ...
                'design_point', 'Punto di progetto', ...
                'feasible_region', 'Regione ammissibile', ...
                'wing_loading', 'Carico alare W/S (N/m^2)', ...
                'power_loading', 'Carico di potenza P/W (W/N)', ...
                'disk_loading', 'Carico del disco DL (N/m^2)', ...
                'power_title', 'Requisiti di potenza per configurazione', ...
                'hover_power', 'Potenza hovering', ...
                'cruise_power', 'Potenza crociera', ...
                'power_ylabel', 'Potenza (W)', ...
                'configuration', 'Configurazione', ...
                'endurance_title', 'Autonomia per configurazione', ...
                'endurance_ylabel', 'Autonomia (min)', ...
                'requirement', 'Requisito', ...
                'energy_budget_title', 'Budget energetico VTOL ibrido', ...
                'energy_ylabel', 'Energia (Wh)', ...
                'hover_label', 'Hovering', ...
                'cruise', 'Crociera', ...
                'reserve_label', 'Riserva', ...
                'available', 'Disponibile', ...
                'required', 'Richiesta', ...
                'margin', 'Margine', ...
                'ld_title', 'Efficienza aerodinamica per configurazione', ...
                'ld_ylabel', 'Rapporto portanza/resistenza (L/D)', ...
                'rotorcraft', 'Velivolo a rotore', ...
                'fixed_wing', 'Ala fissa', ...
                'fixed_wing_no_vtol', 'Ala fissa (senza VTOL)', ...
                'hybrid_vtol', 'VTOL ibrido', ...
                'rotorcraft_equiv', 'Velivolo a rotore (equivalente)', ...
                'fixed_wing_pure', 'Ala fissa (pura)', ...
                'hybrid_vtol_qp', 'VTOL ibrido (QuadPlane)' ...
            );
        end
    end
end

