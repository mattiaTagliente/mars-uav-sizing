-- equation_block_style.lua
-- Apply Word paragraph style to any paragraph that contains DisplayMath.
-- Inline math is not affected.

local STYLE = "Equation Block"

local function has_display_math(inlines)
  for _, x in ipairs(inlines) do
    if x.t == "Math" and x.mathtype == "DisplayMath" then
      return true
    end
    -- recurse into common inline containers
    if x.content and type(x.content) == "table" then
      if has_display_math(x.content) then return true end
    end
  end
  return false
end

local function wrap_para(para)
  local attr = pandoc.Attr("", {}, { ["custom-style"] = STYLE })
  return pandoc.Div({ para }, attr)
end

function Para(el)
  if has_display_math(el.content) then
    return wrap_para(el)
  end
end

function Plain(el)
  if has_display_math(el.content) then
    return wrap_para(pandoc.Para(el.content))
  end
end
