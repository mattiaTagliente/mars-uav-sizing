-- table_body_style.lua
-- Apply Word paragraph styles to *paragraphs inside table cells* in DOCX output.
-- Define these paragraph styles in reference.docx to control formatting:
--   - "Table Body"
--   - (optional) "Table Header"

local BODY_STYLE   = "Table Body"
local HEADER_STYLE = "Table Header"

local function para_from_plain(b)
  return pandoc.Para(b.content)
end

local function style_paragraph_blocks(blocks, style_name)
  if not blocks then return blocks end
  local out = pandoc.List:new()
  local attr = pandoc.Attr("", {}, { ["custom-style"] = style_name })

  for _, b in ipairs(blocks) do
    if b.t == "Plain" then
      out:insert(pandoc.Div({ para_from_plain(b) }, attr))
    elseif b.t == "Para" then
      out:insert(pandoc.Div({ b }, attr))
    else
      -- leave BulletList, CodeBlock, Table, etc. unchanged
      out:insert(b)
    end
  end

  return out
end

local function get_cell_blocks(cell)
  if cell.contents ~= nil then return cell.contents, "contents" end
  if cell.content  ~= nil then return cell.content,  "content"  end
  -- very old representations sometimes use the cell itself as list of blocks
  return cell, nil
end

local function set_cell_blocks(cell, which, blocks)
  if which == "contents" then
    cell.contents = blocks
    return cell
  elseif which == "content" then
    cell.content = blocks
    return cell
  else
    return blocks
  end
end

local function style_cell(cell, style_name)
  local blocks, which = get_cell_blocks(cell)
  if blocks then
    blocks = style_paragraph_blocks(blocks, style_name)
  end
  return set_cell_blocks(cell, which, blocks)
end

local function iter_rows(rows, style_name)
  if not rows then return end
  for _, row in ipairs(rows) do
    -- modern pandoc: row.cells
    if row.cells ~= nil then
      for i, cell in ipairs(row.cells) do
        row.cells[i] = style_cell(cell, style_name)
      end
    else
      -- fallback: row is a plain list of cells
      for i, cell in ipairs(row) do
        row[i] = style_cell(cell, style_name)
      end
    end
  end
end

function Table(tbl)
  -- Table head
  if tbl.head ~= nil then
    local head_rows = tbl.head.rows or tbl.head
    iter_rows(head_rows, HEADER_STYLE)
  end

  -- Table bodies
  if tbl.bodies ~= nil then
    for _, body in ipairs(tbl.bodies) do
      iter_rows(body.head, HEADER_STYLE) -- intermediate head (if any)
      iter_rows(body.body, BODY_STYLE)   -- main body rows
    end
  end

  -- Table foot
  if tbl.foot ~= nil then
    local foot_rows = tbl.foot.rows or tbl.foot
    iter_rows(foot_rows, BODY_STYLE)
  end

  return tbl
end
