-- subfig_grid_tblstyle.lua
local STYLE = "SubfigGridBottom"

local function has_class(attr, cls)
  if not attr or not attr.classes then return false end
  for _, c in ipairs(attr.classes) do
    if c == cls then return true end
  end
  return false
end

local function set_table_style(tbl)
  tbl.attr.attributes = tbl.attr.attributes or {}
  tbl.attr.attributes["custom-style"] = STYLE
  return tbl
end

local walker = { Table = set_table_style }

function Div(div)
  if has_class(div.attr, "subfigures") then
    return pandoc.walk_block(div, walker)
  end
end

function Figure(fig)
  if has_class(fig.attr, "subfigures") then
    return pandoc.walk_block(fig, walker)
  end
end
