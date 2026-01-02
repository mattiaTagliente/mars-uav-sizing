classdef comparative
    %COMPARATIVE Analisi comparativa tra configurazioni.

    methods(Static)
        function results = run_all_analyses()
            results = struct( ...
                'rotorcraft', mars_uav.section5.rotorcraft.rotorcraft_feasibility_analysis(), ...
                'fixed_wing', mars_uav.section5.fixed_wing.fixed_wing_feasibility_analysis(), ...
                'hybrid_vtol', mars_uav.section5.hybrid_vtol.hybrid_vtol_feasibility_analysis() ...
            );
        end

        function comparison = create_comparison_table(results)
            if nargin < 1 || isempty(results)
                results = mars_uav.section5.comparative.run_all_analyses();
            end

            rot = results.rotorcraft;
            fw = results.fixed_wing;
            hyb = results.hybrid_vtol;
            fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);

            comparison = struct();

            comparison.Capacita_VTOL = struct( ...
                'Rotorcraft', struct('value', 'Si', 'ok', true), ...
                'Fixed_Wing', struct('value', 'No', 'ok', false), ...
                'Hybrid_VTOL', struct('value', 'Si', 'ok', true) ...
            );

            comparison.Autonomia_min = struct( ...
                'Rotorcraft', struct('value', fmt(rot.endurance_min, 0), 'ok', rot.feasible), ...
                'Fixed_Wing', struct('value', fmt(fw.endurance_min, 0), 'ok', fw.endurance_passes), ...
                'Hybrid_VTOL', struct('value', fmt(hyb.endurance_min, 0), 'ok', hyb.endurance_passes) ...
            );

            comparison.Raggio_km = struct( ...
                'Rotorcraft', struct('value', fmt(rot.range_km, 0), 'ok', rot.range_km >= 100), ...
                'Fixed_Wing', struct('value', fmt(fw.range_km, 0), 'ok', fw.range_km >= 100), ...
                'Hybrid_VTOL', struct('value', fmt(hyb.range_km, 0), 'ok', hyb.range_km >= 100) ...
            );

            comparison.Potenza_crociera_W = struct( ...
                'Rotorcraft', struct('value', fmt(rot.cruise_power_w, 0), 'ok', []), ...
                'Fixed_Wing', struct('value', fmt(fw.cruise_power_w, 0), 'ok', []), ...
                'Hybrid_VTOL', struct('value', fmt(hyb.cruise_power_w, 0), 'ok', []) ...
            );

            comparison.Potenza_hover_W = struct( ...
                'Rotorcraft', struct('value', fmt(rot.hover_power_w, 0), 'ok', []), ...
                'Fixed_Wing', struct('value', 'N/A', 'ok', []), ...
                'Hybrid_VTOL', struct('value', fmt(hyb.hover_power_w, 0), 'ok', []) ...
            );

            comparison.LD_crociera = struct( ...
                'Rotorcraft', struct('value', fmt(rot.ld_effective, 1), 'ok', []), ...
                'Fixed_Wing', struct('value', fmt(fw.ld_max, 1), 'ok', []), ...
                'Hybrid_VTOL', struct('value', fmt(hyb.ld_quadplane, 1), 'ok', []) ...
            );

            if rot.feasible
                rot_feas = 'Marginale';
            else
                rot_feas = 'No';
            end

            comparison.Fattibilita_complessiva = struct( ...
                'Rotorcraft', struct('value', rot_feas, 'ok', rot.feasible), ...
                'Fixed_Wing', struct('value', 'No', 'ok', false), ...
                'Hybrid_VTOL', struct('value', 'Si', 'ok', hyb.feasible) ...
            );
        end

        function ranking = configuration_ranking(results)
            if nargin < 1 || isempty(results)
                results = mars_uav.section5.comparative.run_all_analyses();
            end

            names = {'rotorcraft', 'fixed_wing', 'hybrid_vtol'};
            scores = zeros(size(names));

            for i = 1:numel(names)
                name = names{i};
                res = results.(name);
                score = 0;

                if ~strcmp(name, 'fixed_wing')
                    score = score + 100;
                end

                if isfield(res, 'endurance_min')
                    score = score + res.endurance_min;
                end

                if isfield(res, 'range_km')
                    score = score + res.range_km / 10;
                end

                if isfield(res, 'margin_percent') && res.margin_percent > 0
                    score = score + res.margin_percent;
                end

                scores(i) = score;
            end

            [~, idx] = sort(scores, 'descend');
            ranking = names(idx);
        end

        function rationale = elimination_rationale(results)
            if nargin < 1 || isempty(results)
                results = mars_uav.section5.comparative.run_all_analyses();
            end

            rot = results.rotorcraft;
            fw = results.fixed_wing;
            hyb = results.hybrid_vtol;
            fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);

            rationale = struct();

            if rot.feasible && rot.margin_percent >= 10
                rationale.rotorcraft = sprintf('IDONEO: Requisiti rispettati con margine %s%%.', ...
                    fmt(rot.margin_percent, 0));
            elseif rot.feasible
                rationale.rotorcraft = sprintf([ ...
                    'ELIMINATO: Autonomia al limite (%s min) con margine %s%%. ', ...
                    'Insufficiente per missione senza capacita di abort.'], ...
                    fmt(rot.endurance_min, 0), fmt(rot.margin_percent, 0));
            else
                rationale.rotorcraft = sprintf([ ...
                    'ELIMINATO: Requisito autonomia non soddisfatto (%s min vs 60 min). ', ...
                    'L/D equivalente basso (%s) limita l''efficienza in avanti.'], ...
                    fmt(rot.endurance_min, 0), fmt(rot.ld_effective, 1));
            end

            rationale.fixed_wing = sprintf([ ...
                'ELIMINATO: Requisito VTOL non soddisfatto. Nonostante autonomia elevata ', ...
                '(%s min, +%s%% margine), la corsa al suolo di %s m richiede pista.'], ...
                fmt(fw.endurance_min, 0), ...
                fmt((fw.endurance_min / fw.requirement_min - 1) * 100, 0), ...
                fmt(fw.takeoff_distance_m, 0));

            if hyb.feasible
                margin = (hyb.endurance_min / hyb.requirement_min - 1) * 100;
                rationale.hybrid_vtol = sprintf([ ...
                    'SELEZIONATO: Requisiti soddisfatti. Capacita VTOL con %s min ', ...
                    'autonomia (%s%% margine). Unisce VTOL a rotore e efficienza ala fissa in crociera.'], ...
                    fmt(hyb.endurance_min, 0), fmt(margin, 0));
            else
                rationale.hybrid_vtol = sprintf([ ...
                    'ELIMINATO: Requisiti non rispettati nonostante architettura ibrida. ', ...
                    'Autonomia: %s min.'], fmt(hyb.endurance_min, 0));
            end
        end

        function summary = comparative_summary()
            results = mars_uav.section5.comparative.run_all_analyses();
            comparison = mars_uav.section5.comparative.create_comparison_table(results);
            ranking = mars_uav.section5.comparative.configuration_ranking(results);
            rationale = mars_uav.section5.comparative.elimination_rationale(results);

            summary = struct( ...
                'results', results, ...
                'comparison', comparison, ...
                'ranking', {ranking}, ...
                'rationale', rationale, ...
                'selected', ranking{1} ...
            );
        end

        function print_analysis(summary)
            if nargin < 1 || isempty(summary)
                summary = mars_uav.section5.comparative.comparative_summary();
            end

            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('ANALISI COMPARATIVA CONFIGURAZIONI\n');
            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('Calcolato: %s\n', datestr(now, 'yyyy-mm-dd HH:MM:SS'));
            fprintf('Config:    Valori da file YAML in config/\n\n');

            fprintf('TABELLA COMPARATIVA CONFIGURAZIONI\n');
            fprintf('%s\n', repmat('-', 1, 80));
            header_rot = mars_uav.section5.comparative.label('rotorcraft');
            header_fw = mars_uav.section5.comparative.label('fixed_wing');
            header_hyb = mars_uav.section5.comparative.label('hybrid_vtol');
            fprintf('%-23s %18s %18s %18s\n', 'Metrica', header_rot, header_fw, header_hyb);
            fprintf('%s\n', repmat('-', 1, 80));

            metrics = fieldnames(summary.comparison);
            for i = 1:numel(metrics)
                metric = metrics{i};
                values = summary.comparison.(metric);

                rot = values.Rotorcraft;
                fw = values.Fixed_Wing;
                hyb = values.Hybrid_VTOL;

                rot_str = mars_uav.section5.comparative.decorate_value(rot);
                fw_str = mars_uav.section5.comparative.decorate_value(fw);
                hyb_str = mars_uav.section5.comparative.decorate_value(hyb);

                metric_label = strrep(metric, '_', ' ');
                metric_label = strrep(metric_label, 'hover', 'hovering');
                fprintf('%-23s %18s %18s %18s\n', metric_label, rot_str, fw_str, hyb_str);
            end

            fprintf('%s\n\n', repmat('-', 1, 80));

            fprintf('CLASSIFICA CONFIGURAZIONI\n');
            fprintf('%s\n', repmat('-', 1, 50));
            for i = 1:numel(summary.ranking)
                name = summary.ranking{i};
                fprintf('  %d. %s\n', i, mars_uav.section5.comparative.label(name));
            end
            fprintf('\n');

            fprintf('MOTIVAZIONE ELIMINAZIONE\n');
            fprintf('%s\n', repmat('-', 1, 80));
            configs = fieldnames(summary.rationale);
            for i = 1:numel(configs)
                config = configs{i};
                fprintf('\n%s:\n', upper(strrep(mars_uav.section5.comparative.label(config), '_', ' ')));
                fprintf('  %s\n', summary.rationale.(config));
            end
            fprintf('\n');

            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('RACCOMANDAZIONE\n');
            fprintf('%s\n', repmat('=', 1, 80));
            selected = summary.selected;
            fprintf('Configurazione selezionata: %s\n\n', upper(strrep(mars_uav.section5.comparative.label(selected), '_', ' ')));
            fprintf('%s\n', summary.rationale.(selected));
            fprintf('%s\n', repmat('=', 1, 80));
        end

        function text = decorate_value(entry)
            text = entry.value;
            if islogical(entry.ok) && ~isempty(entry.ok)
                if entry.ok
                    text = sprintf('%s [+]', entry.value);
                else
                    text = sprintf('%s [-]', entry.value);
                end
            end
        end

        function text = label(name)
            switch char(name)
                case 'rotorcraft'
                    text = 'Velivolo a rotore';
                case 'fixed_wing'
                    text = 'Ala fissa';
                case 'hybrid_vtol'
                    text = 'VTOL ibrido';
                otherwise
                    text = strrep(char(name), '_', ' ');
            end
        end
    end
end

