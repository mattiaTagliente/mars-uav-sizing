-- bullet_to_word_list_bullet.lua
-- Convert Pandoc BulletList blocks into Word paragraphs styled
-- "List Bullet", "List Bullet 2", "List Bullet 3" via custom-style Div wrappers.
--
-- Usage:
--   pandoc input.md -o output.docx --reference-doc=reference.docx -L bullet_to_word_list_bullet.lua
--
-- Notes:
-- - These style names must exist in the reference.docx. In non-English Word installs,
--   the built-in style display names may be localized.

local function cap_level(level)
  if level < 1 then return 1 end
  if level > 3 then return 3 end
  return level
end

local function bullet_style(level)
  level = cap_level(level)
  if level == 1 then return "List Bullet" end
  if level == 2 then return "List Bullet 2" end
  return "List Bullet 3"
end

local function as_para(block)
  if block.t == "Plain" then
    return pandoc.Para(block.content)
  end
  return block
end

local function styled_div(style_name, block)
  local attr = pandoc.Attr("", {}, { ["custom-style"] = style_name })
  return pandoc.Div({ as_para(block) }, attr)
end

-- Flatten a BulletList into a sequence of styled paragraphs (plus transformed nested lists).
local function flatten_bullet_list(bl, level)
  local out = pandoc.List:new()
  local style_name = bullet_style(level)

  for _, item in ipairs(bl.content) do
    local first_para_done = false

    for _, b in ipairs(item) do
      if b.t == "BulletList" then
        local nested = flatten_bullet_list(b, level + 1)
        for _, nb in ipairs(nested) do out:insert(nb) end

      elseif (b.t == "Para" or b.t == "Plain") and (not first_para_done) then
        out:insert(styled_div(style_name, b))
        first_para_done = true

      else
        -- Keep other blocks as-is (including additional paragraphs).
        -- If you need multi-paragraph list items to keep hanging indentation,
        -- extend this branch with "List Continue" styles.
        out:insert(b)
      end
    end
  end

  return out
end

local function transform_blocks(blocks)
  local out = pandoc.List:new()

  for _, b in ipairs(blocks) do
    if b.t == "BulletList" then
      local flat = flatten_bullet_list(b, 1)
      for _, fb in ipairs(flat) do out:insert(fb) end

    elseif b.t == "Div" then
      b.content = transform_blocks(b.content)
      out:insert(b)

    elseif b.t == "BlockQuote" then
      b.content = transform_blocks(b.content)
      out:insert(b)

    else
      out:insert(b)
    end
  end

  return out
end

function Pandoc(doc)
  doc.blocks = transform_blocks(doc.blocks)
  return doc
end
