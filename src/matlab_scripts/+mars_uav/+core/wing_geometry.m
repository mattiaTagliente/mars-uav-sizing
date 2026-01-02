function [wingspan, chord] = wing_geometry(wing_area, aspect_ratio)
%WING_GEOMETRY Calcola apertura alare e corda da area e rapporto d'aspetto.

wingspan = sqrt(aspect_ratio * wing_area);
chord = wing_area / wingspan;
end
