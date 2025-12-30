--[[
strip_section_numbers.lua
Lua filter for Pandoc that removes section numbers from headings.

This filter works with pandoc-crossref's numberSections feature:
1. pandoc-crossref's numberSections adds section numbers to heading text
2. pandoc-crossref uses those numbers for @sec: cross-references
3. This filter (running AFTER pandoc-crossref) strips the numbers from headings
4. Word template's outline numbering provides the visible section numbers

The filter removes leading section numbers in formats like:
- "1 Title" -> "Title"
- "2.3 Title" -> "Title"
- "4.1.2 Title" -> "Title"

Usage in defaults file:
  filters:
    - pandoc-crossref
    - strip_section_numbers.lua  # Must come AFTER pandoc-crossref
    - citeproc
  metadata:
    numberSections: true
    sectionsDepth: -1
]]

function Header(el)
    if el.content and #el.content > 0 then
        -- pandoc-crossref prepends section numbers as Str elements
        -- Format: "1.2.3" followed by Space, then the title
        
        local first = el.content[1]
        
        -- Check if it's a Span with header-section-number class (Pandoc native)
        if first.t == "Span" and first.classes and first.classes:includes("header-section-number") then
            table.remove(el.content, 1)
            -- Remove following space
            if #el.content > 0 and el.content[1].t == "Space" then
                table.remove(el.content, 1)
            end
            return el
        end
        
        -- Check if it's a Str that looks like a section number (pandoc-crossref format)
        -- Section numbers match pattern: digits and dots, like "1", "2.3", "4.1.2"
        if first.t == "Str" then
            local text = first.text
            -- Match section number pattern: one or more digits, optionally followed by (.digit)+
            if text:match("^%d+[%.%d]*$") then
                table.remove(el.content, 1)
                -- Remove following space or nbsp
                if #el.content > 0 then
                    local second = el.content[1]
                    if second.t == "Space" or second.t == "Str" and second.text == "\194\160" then
                        table.remove(el.content, 1)
                    end
                end
                return el
            end
        end
    end
    return el
end
