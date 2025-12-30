-- after_table_spacer.lua
-- Inserts a styled spacer paragraph after every table.

local SPACER_STYLE = "AfterTableSpacer"

local function spacer_block()
  local attr = pandoc.Attr("", {}, { ["custom-style"] = SPACER_STYLE })
  -- NBSP ensures the paragraph is kept; it won't render as visible text.
  local nbsp = pandoc.Str("\u{00A0}")
  return pandoc.Div({ pandoc.Para({ nbsp }) }, attr)
end

function Table(tbl)
  return { tbl, spacer_block() }
end
