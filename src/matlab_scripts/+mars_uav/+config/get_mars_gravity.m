function g = get_mars_gravity()
%GET_MARS_GRAVITY Gravita su Marte in m/s^2.

g = mars_uav.config.get_param('physical.mars.g');
end
