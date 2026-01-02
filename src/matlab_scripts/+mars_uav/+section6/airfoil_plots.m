classdef airfoil_plots
    %AIRFOIL_PLOTS Grafici di confronto per profili alari.

    methods(Static)
        function text = get_text(key, lang)
            %GET_TEXT Recupera le stringhe tradotte per i grafici.
            if nargin < 2 || isempty(lang)
                lang = 'it';
            end
            translations = mars_uav.section6.airfoil_plots.translations();
            if isfield(translations, lang) && isfield(translations.(lang), key)
                text = translations.(lang).(key);
            else
                text = key;
            end
        end

        function polars = load_airfoil_data(yaml_path)
            %LOAD_AIRFOIL_DATA Carica i dati dei profili dal file YAML.
            if nargin < 1 || isempty(yaml_path)
                yaml_path = fullfile(mars_uav.config.get_config_dir(), 'airfoil_data.yaml');
            end
            polars = mars_uav.section6.airfoil_plots.parse_airfoil_yaml(yaml_path);
        end

        function plot_cl_alpha(save_path, show, lang, highlight_airfoil)
            %PLOT_CL_ALPHA Grafico C_L vs angolo di attacco.
            if nargin < 4 || isempty(highlight_airfoil)
                highlight_airfoil = 'e387';
            end
            if nargin < 3 || isempty(lang)
                lang = 'it';
            end
            if nargin < 2 || isempty(show)
                show = true;
            end
            if nargin < 1
                save_path = '';
            end

            polars = mars_uav.section6.airfoil_plots.load_airfoil_data();
            fig = mars_uav.visualization.plotting.create_figure(show);
            ax = axes(fig);
            hold(ax, 'on');

            for i = 1:numel(polars)
                name = polars(i).name;
                alpha = polars(i).alpha;
                cl = polars(i).cl;
                [color, style, width] = mars_uav.section6.airfoil_plots.get_style(name, highlight_airfoil);

                plot(ax, alpha, cl, style, 'Color', color, 'LineWidth', width, 'DisplayName', upper(name));

                if strcmpi(name, highlight_airfoil)
                    [cl_max, idx_max] = max(cl);
                    plot(ax, alpha(idx_max), cl_max, 'o', 'Color', color, 'MarkerSize', 8, ...
                        'HandleVisibility', 'off');
                    label = sprintf('$C_{L,%s}$ = %s', ...
                        mars_uav.section6.airfoil_plots.get_text('max_marker', lang), ...
                        mars_uav.core.format_number(cl_max, 2));
                    text(ax, alpha(idx_max) + 2, cl_max - 0.1, label, 'Interpreter', 'latex', 'FontSize', 9);
                end
            end

            xlabel(ax, mars_uav.section6.airfoil_plots.get_text('xlabel_alpha', lang), 'Interpreter', 'latex');
            ylabel(ax, mars_uav.section6.airfoil_plots.get_text('ylabel_cl', lang), 'Interpreter', 'latex');
            title(ax, mars_uav.section6.airfoil_plots.get_text('title_cl_alpha', lang), 'FontWeight', 'bold');
            grid(ax, 'on');
            xlim(ax, [-6, 14]);
            ylim(ax, [-0.5, 1.4]);

            lgd = legend(ax, 'Location', 'southeast');
            lgd.NumColumns = 2;

            subtitle = sprintf('%s', mars_uav.section6.airfoil_plots.get_text('subtitle', lang));
            text(ax, 0.5, -0.12, subtitle, 'Units', 'normalized', ...
                'HorizontalAlignment', 'center', 'FontAngle', 'italic', 'FontSize', 9);

            hold(ax, 'off');

            if ~isempty(save_path)
                mars_uav.visualization.plotting.save_figure(fig, save_path);
            end
            if ~show
                close(fig);
            end
        end

        function plot_cd_alpha(save_path, show, lang, highlight_airfoil)
            %PLOT_CD_ALPHA Grafico C_D vs angolo di attacco.
            if nargin < 4 || isempty(highlight_airfoil)
                highlight_airfoil = 'e387';
            end
            if nargin < 3 || isempty(lang)
                lang = 'it';
            end
            if nargin < 2 || isempty(show)
                show = true;
            end
            if nargin < 1
                save_path = '';
            end

            polars = mars_uav.section6.airfoil_plots.load_airfoil_data();
            fig = mars_uav.visualization.plotting.create_figure(show);
            ax = axes(fig);
            hold(ax, 'on');

            for i = 1:numel(polars)
                name = polars(i).name;
                alpha = polars(i).alpha;
                cd = polars(i).cd;
                [color, style, width] = mars_uav.section6.airfoil_plots.get_style(name, highlight_airfoil);

                plot(ax, alpha, cd, style, 'Color', color, 'LineWidth', width, 'DisplayName', upper(name));

                if strcmpi(name, highlight_airfoil)
                    [cd_min, idx_min] = min(cd);
                    plot(ax, alpha(idx_min), cd_min, 'o', 'Color', color, 'MarkerSize', 8, ...
                        'HandleVisibility', 'off');
                    label = sprintf('$C_{D,min}$ = %s', mars_uav.core.format_number(cd_min, 4));
                    text(ax, alpha(idx_min) + 2, cd_min + 0.01, label, 'Interpreter', 'latex', 'FontSize', 9);
                end
            end

            xlabel(ax, mars_uav.section6.airfoil_plots.get_text('xlabel_alpha', lang), 'Interpreter', 'latex');
            ylabel(ax, mars_uav.section6.airfoil_plots.get_text('ylabel_cd', lang), 'Interpreter', 'latex');
            title(ax, mars_uav.section6.airfoil_plots.get_text('title_cd_alpha', lang), 'FontWeight', 'bold');
            grid(ax, 'on');
            xlim(ax, [-6, 14]);
            ylim(ax, [0, 0.08]);

            lgd = legend(ax, 'Location', 'northwest');
            lgd.NumColumns = 2;

            subtitle = sprintf('%s', mars_uav.section6.airfoil_plots.get_text('subtitle', lang));
            text(ax, 0.5, -0.12, subtitle, 'Units', 'normalized', ...
                'HorizontalAlignment', 'center', 'FontAngle', 'italic', 'FontSize', 9);

            hold(ax, 'off');

            if ~isempty(save_path)
                mars_uav.visualization.plotting.save_figure(fig, save_path);
            end
            if ~show
                close(fig);
            end
        end

        function plot_drag_polar(save_path, show, lang, highlight_airfoil)
            %PLOT_DRAG_POLAR Grafico polare C_L vs C_D.
            if nargin < 4 || isempty(highlight_airfoil)
                highlight_airfoil = 'e387';
            end
            if nargin < 3 || isempty(lang)
                lang = 'it';
            end
            if nargin < 2 || isempty(show)
                show = true;
            end
            if nargin < 1
                save_path = '';
            end

            polars = mars_uav.section6.airfoil_plots.load_airfoil_data();
            fig = mars_uav.visualization.plotting.create_figure(show);
            ax = axes(fig);
            hold(ax, 'on');

            for i = 1:numel(polars)
                name = polars(i).name;
                alpha = polars(i).alpha;
                cl = polars(i).cl;
                cd = polars(i).cd;
                ld = polars(i).ld;
                [color, style, width] = mars_uav.section6.airfoil_plots.get_style(name, highlight_airfoil);

                plot(ax, cd, cl, style, 'Color', color, 'LineWidth', width, 'DisplayName', upper(name));

                if strcmpi(name, highlight_airfoil)
                    [~, idx_max] = max(ld);
                    plot(ax, cd(idx_max), cl(idx_max), 'o', 'Color', color, 'MarkerSize', 8, ...
                        'HandleVisibility', 'off');
                    text(ax, cd(idx_max) + 0.005, cl(idx_max) - 0.08, '$(L/D)_{max}$', ...
                        'Interpreter', 'latex', 'FontSize', 9);
                end
            end

            xlabel(ax, mars_uav.section6.airfoil_plots.get_text('xlabel_cd', lang), 'Interpreter', 'latex');
            ylabel(ax, mars_uav.section6.airfoil_plots.get_text('ylabel_cl', lang), 'Interpreter', 'latex');
            title(ax, mars_uav.section6.airfoil_plots.get_text('title_polar', lang), 'FontWeight', 'bold');
            grid(ax, 'on');
            xlim(ax, [0, 0.08]);
            ylim(ax, [-0.5, 1.4]);

            lgd = legend(ax, 'Location', 'southeast');
            lgd.NumColumns = 2;

            subtitle = sprintf('%s', mars_uav.section6.airfoil_plots.get_text('subtitle', lang));
            text(ax, 0.5, -0.12, subtitle, 'Units', 'normalized', ...
                'HorizontalAlignment', 'center', 'FontAngle', 'italic', 'FontSize', 9);

            hold(ax, 'off');

            if ~isempty(save_path)
                mars_uav.visualization.plotting.save_figure(fig, save_path);
            end
            if ~show
                close(fig);
            end
        end

        function plot_ld_alpha(save_path, show, lang, highlight_airfoil)
            %PLOT_LD_ALPHA Grafico L/D vs angolo di attacco.
            if nargin < 4 || isempty(highlight_airfoil)
                highlight_airfoil = 'e387';
            end
            if nargin < 3 || isempty(lang)
                lang = 'it';
            end
            if nargin < 2 || isempty(show)
                show = true;
            end
            if nargin < 1
                save_path = '';
            end

            polars = mars_uav.section6.airfoil_plots.load_airfoil_data();
            fig = mars_uav.visualization.plotting.create_figure(show);
            ax = axes(fig);
            hold(ax, 'on');

            for i = 1:numel(polars)
                name = polars(i).name;
                alpha = polars(i).alpha;
                ld = polars(i).ld;
                mask = ld > 0;
                alpha_pos = alpha(mask);
                ld_pos = ld(mask);
                [color, style, width] = mars_uav.section6.airfoil_plots.get_style(name, highlight_airfoil);

                plot(ax, alpha_pos, ld_pos, style, 'Color', color, 'LineWidth', width, 'DisplayName', upper(name));

                if strcmpi(name, highlight_airfoil) && ~isempty(ld_pos)
                    [ld_max, idx_max] = max(ld_pos);
                    plot(ax, alpha_pos(idx_max), ld_max, 'o', 'Color', color, 'MarkerSize', 8, ...
                        'HandleVisibility', 'off');
                    label = sprintf('$(L/D)_{max}$ = %s', mars_uav.core.format_number(ld_max, 1));
                    text(ax, alpha_pos(idx_max) - 3, ld_max + 3, label, 'Interpreter', 'latex', 'FontSize', 9);
                end
            end

            xlabel(ax, mars_uav.section6.airfoil_plots.get_text('xlabel_alpha', lang), 'Interpreter', 'latex');
            ylabel(ax, mars_uav.section6.airfoil_plots.get_text('ylabel_ld', lang), 'Interpreter', 'latex');
            title(ax, mars_uav.section6.airfoil_plots.get_text('title_ld_alpha', lang), 'FontWeight', 'bold');
            grid(ax, 'on');
            xlim(ax, [-2, 14]);
            ylim(ax, [0, 55]);

            lgd = legend(ax, 'Location', 'northeast');
            lgd.NumColumns = 2;

            subtitle = sprintf('%s', mars_uav.section6.airfoil_plots.get_text('subtitle', lang));
            text(ax, 0.5, -0.12, subtitle, 'Units', 'normalized', ...
                'HorizontalAlignment', 'center', 'FontAngle', 'italic', 'FontSize', 9);

            hold(ax, 'off');

            if ~isempty(save_path)
                mars_uav.visualization.plotting.save_figure(fig, save_path);
            end
            if ~show
                close(fig);
            end
        end

        function generate_all_airfoil_figures(output_dir, show, lang)
            %GENERATE_ALL_AIRFOIL_FIGURES Esporta tutte le figure dei profili.
            if nargin < 3 || isempty(lang)
                lang = 'it';
            end
            if nargin < 2 || isempty(show)
                show = false;
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

            mars_uav.section6.airfoil_plots.plot_cl_alpha( ...
                fullfile(output_dir, ['airfoil_cl_alpha' suffix '.png']), show, lang);
            mars_uav.section6.airfoil_plots.plot_cd_alpha( ...
                fullfile(output_dir, ['airfoil_cd_alpha' suffix '.png']), show, lang);
            mars_uav.section6.airfoil_plots.plot_drag_polar( ...
                fullfile(output_dir, ['airfoil_polar' suffix '.png']), show, lang);
            mars_uav.section6.airfoil_plots.plot_ld_alpha( ...
                fullfile(output_dir, ['airfoil_ld_alpha' suffix '.png']), show, lang);
        end
    end

    methods(Static, Access=private)
        function [color, style, width] = get_style(name, highlight_airfoil)
            %GET_STYLE Restituisce colore, stile e spessore linea.
            colors = mars_uav.section6.airfoil_plots.airfoil_colors();
            styles = mars_uav.section6.airfoil_plots.airfoil_styles();

            key = mars_uav.section6.airfoil_plots.normalize_name(name);

            if isfield(colors, key)
                color = colors.(key);
            else
                color = [0.2 0.2 0.2];
            end

            if isfield(styles, key)
                style = styles.(key);
            else
                style = '-';
            end

            if strcmpi(name, highlight_airfoil)
                width = 2.5;
            else
                width = 1.5;
            end
        end

        function key = normalize_name(name)
            %NORMALIZE_NAME Converte i nomi con trattini in chiavi valide.
            key = strrep(lower(name), '-', '_');
        end

        function polars = parse_airfoil_yaml(file_path)
            %PARSE_AIRFOIL_YAML Parsing minimale per airfoil_data.yaml.
            lines = readlines(file_path);

            polars = struct('name', {}, 'alpha', {}, 'cl', {}, 'cd', {}, 'ld', {});
            in_airfoils = false;
            in_ld_data = false;
            ld_indent = 0;

            current = struct();
            ld_points = struct('alpha', {}, 'cl', {}, 'cd', {}, 'ld', {});

            for i = 1:numel(lines)
                [clean_line, indent] = mars_uav.section6.airfoil_plots.clean_yaml_line(lines(i));
                if isempty(clean_line)
                    continue;
                end

                if strcmp(clean_line, 'airfoils:')
                    in_airfoils = true;
                    continue;
                end

                if ~in_airfoils
                    continue;
                end

                if startsWith(clean_line, '- name:')
                    polars = mars_uav.section6.airfoil_plots.flush_airfoil(polars, current, ld_points);
                    current = struct('name', strtrim(strrep(clean_line, '- name:', '')));
                    ld_points = struct('alpha', {}, 'cl', {}, 'cd', {}, 'ld', {});
                    in_ld_data = false;
                    continue;
                end

                if startsWith(clean_line, 'ld_data:')
                    in_ld_data = true;
                    ld_indent = indent;
                    continue;
                end

                if in_ld_data
                    if startsWith(clean_line, '- {')
                        entry = mars_uav.section6.airfoil_plots.parse_ld_inline_map(clean_line);
                        if ~isempty(entry)
                            ld_points(end+1) = entry; %#ok<AGROW>
                        end
                        continue;
                    end
                    if indent <= ld_indent
                        in_ld_data = false;
                    end
                end
            end

            polars = mars_uav.section6.airfoil_plots.flush_airfoil(polars, current, ld_points);
        end

        function [clean_line, indent] = clean_yaml_line(raw_line)
            %CLEAN_YAML_LINE Rimuove commenti e calcola l'indentazione.
            line = char(raw_line);
            hash_idx = strfind(line, '#');
            if ~isempty(hash_idx)
                line = line(1:hash_idx(1)-1);
            end
            line = regexprep(line, '\s+$', '');
            indent = length(line) - length(strtrim(line));
            clean_line = strtrim(line);
        end

        function entry = parse_ld_inline_map(line)
            %PARSE_LD_INLINE_MAP Estrae alpha, cl, cd, ld dal formato inline.
            entry = struct();
            open_idx = strfind(line, '{');
            close_idx = strfind(line, '}');
            if isempty(open_idx) || isempty(close_idx)
                return;
            end
            content = line(open_idx(1) + 1:close_idx(end) - 1);
            pairs = strsplit(content, ',');
            entry = struct('alpha', NaN, 'cl', NaN, 'cd', NaN, 'ld', NaN);
            for i = 1:numel(pairs)
                pair = strtrim(pairs{i});
                colon_idx = strfind(pair, ':');
                if isempty(colon_idx)
                    continue;
                end
                key = strtrim(pair(1:colon_idx(1)-1));
                value = str2double(strtrim(pair(colon_idx(1)+1:end)));
                if isfield(entry, key) && ~isnan(value)
                    entry.(key) = value;
                end
            end
        end

        function polars = flush_airfoil(polars, current, ld_points)
            %FLUSH_AIRFOIL Aggiunge il profilo corrente alla lista finale.
            if isempty(fieldnames(current))
                return;
            end
            if isempty(ld_points)
                current.alpha = [];
                current.cl = [];
                current.cd = [];
                current.ld = [];
            else
                current.alpha = [ld_points.alpha];
                current.cl = [ld_points.cl];
                current.cd = [ld_points.cd];
                current.ld = [ld_points.ld];
            end
            polars(end+1) = current; %#ok<AGROW>
        end

        function colors = airfoil_colors()
            %AIRFOIL_COLORS Palette coerente con lo script Python.
            colors = struct( ...
                'e387', [0.1216 0.4667 0.7059], ...
                'sd8000', [1.0000 0.4980 0.0549], ...
                's7055', [0.1725 0.6275 0.1725], ...
                'ag455ct_02r', [0.8392 0.1529 0.1569], ...
                'sd7037b', [0.5804 0.4039 0.7412], ...
                'ag12', [0.5490 0.3373 0.2941], ...
                'ag35_r', [0.8902 0.4667 0.7608] ...
            );
        end

        function styles = airfoil_styles()
            %AIRFOIL_STYLES Stili linea coerenti con lo script Python.
            styles = struct( ...
                'e387', '-', ...
                'sd8000', '--', ...
                's7055', '-.', ...
                'ag455ct_02r', ':', ...
                'sd7037b', '--', ...
                'ag12', '-.', ...
                'ag35_r', ':' ...
            );
        end

        function translations = translations()
            translations.en = struct( ...
                'title_cl_alpha', 'Lift coefficient vs angle of attack', ...
                'title_cd_alpha', 'Drag coefficient vs angle of attack', ...
                'title_polar', 'Drag polar', ...
                'title_ld_alpha', 'Lift-to-drag ratio vs angle of attack', ...
                'xlabel_alpha', 'Angle of attack $\alpha$ ($^\circ$)', ...
                'ylabel_cl', 'Lift coefficient $C_L$', ...
                'ylabel_cd', 'Drag coefficient $C_D$', ...
                'ylabel_ld', 'Lift-to-drag ratio L/D', ...
                'xlabel_cd', 'Drag coefficient $C_D$', ...
                'subtitle', 'Re ~ 60,000 (UIUC wind tunnel data)', ...
                'max_marker', 'max' ...
            );

            translations.it = struct( ...
                'title_cl_alpha', 'Coefficiente di portanza vs angolo di attacco', ...
                'title_cd_alpha', 'Coefficiente di resistenza vs angolo di attacco', ...
                'title_polar', 'Polare di resistenza', ...
                'title_ld_alpha', 'Efficienza aerodinamica vs angolo di attacco', ...
                'xlabel_alpha', 'Angolo di attacco $\alpha$ ($^\circ$)', ...
                'ylabel_cl', 'Coefficiente di portanza $C_L$', ...
                'ylabel_cd', 'Coefficiente di resistenza $C_D$', ...
                'ylabel_ld', 'Rapporto portanza/resistenza L/D', ...
                'xlabel_cd', 'Coefficiente di resistenza $C_D$', ...
                'subtitle', 'Re ~ 60,000 (dati galleria del vento UIUC)', ...
                'max_marker', 'max' ...
            );
        end
    end
end
