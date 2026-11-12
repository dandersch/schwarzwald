require("colorbuddy").colorscheme('theme')

local colorbuddy = require('colorbuddy')
local Color      = colorbuddy.Color
local Group      = colorbuddy.Group
local colors     = colorbuddy.colors
local groups     = colorbuddy.groups
local styles     = colorbuddy.styles

-- the main colors
Color.new('white',      '#ffffff')
Color.new('green',      '#99BB66')
Color.new('yellow',     '#ECBE7B')
Color.new('blue',       '#4DB5BD') -- '#46D0FF' '#0170BF'
Color.new('darkblue',   '#003c64')
Color.new('brown',      '#B4916D')
Color.new('grey',       '#404940')
Color.new('background', '#18191b')
Color.new('bg2',        '#1f1f1f')
Color.new('gray0',      '#18191b') -- BUG: 'background' doesnt set bg, this does

-- these colors are defined just in case
Color.new('red',        '#ff0000')
Color.new('pink',       '#ff3090')
Color.new('aqua',       '#0000ff')
Color.new('cyan',       '#1fffff')
Color.new('purple',     '#a00090')
Color.new('violet',     '#af6ff0')
Color.new('orange',     '#ffaf0f')
Color.new('seagreen',   '#698b69')

Group.new('Normal',      colors.white,  colors.bg)
Group.new('NormalFloat', colors.white,  colors.bg2) -- bg for floating windows like :Lazy
Group.new("Visual",      colors.NONE,   colors.darkblue,    styles.NONE)
Group.new("Search",      colors.black,  colors.yellow)
Group.new("MatchParen",  colors.NONE,   colors.darkblue,    styles.NONE)
Group.new("Whitespace",  colors.grey,   colors.bg)

-- not sure what these change
Group.new('FloatBorder', colors.blue, colors.bg2)
Group.new('Pmenu', colors.white, colors.bg2) -- popup menu (?)
Group.new('PmenuSel', colors.white, colors.darkblue)

-- programming
Group.new('Function',    colors.white,     colors.background , styles.NONE)
Group.new('Variable',    colors.white,     colors.background , styles.NONE)
Group.new('Comment',     colors.green,     colors.none--[[,    styles.italic--]])
Group.new("Identifier",  colors.white,     colors.none,        styles.NONE)
Group.new("Keyword",     colors.yellow,    colors.none,        styles.NONE)
Group.new("String",      colors.brown,     colors.none,        styles.NONE)
Group.new("Structure",   colors.yellow,    colors.none,        styles.NONE) -- struct, union, enum
Group.new("Todo",        colors.yellow,    colors.NONE,        styles.bold)
Group.new("Type",        colors.blue)
Group.new("Number",      colors.brown)
Group.new("Include",     colors.yellow)
Group.new("PreProc",     colors.yellow,    colors.NONE--[[,    styles.bold--]])
Group.new("Statement",   colors.yellow)
Group.new("Constant",    colors.yellow,    colors.NONE,        styles.NONE)
Group.new("Special",     colors.brown,     colors.NONE,        styles.NONE)
Group.new("Conditional", colors.yellow)
Group.new("Operator",    colors.white)
Group.new("Repeat",      colors.yellow)

-- C/C++
Group.new("cType",          colors.blue)
Group.new("cTypedef",       colors.yellow)
Group.new("cStructure",     colors.yellow) -- struct, union, enum
Group.new("cConditional",   colors.yellow) -- if else
Group.new("cRepeat",        colors.yellow) -- for while
Group.new("cCharacter",     colors.brown,  colors.none, styles.NONE)
Group.new("cBlock",         colors.brown,  colors.NONE, styles.bold)
Group.new("cblock",         colors.white,  colors.NONE, styles.bold)
Group.new("cParen",         colors.white,  colors.NONE, styles.bold)
Group.new("cFormat",        colors.white,  colors.NONE, styles.bold) -- %s
Group.new("cSpecial",       colors.white,  colors.NONE, styles.bold) -- \n
Group.new("cCppOutWrapper", colors.yellow, colors.NONE)
--Group.new("cCppOutIf",      colors.grey,   colors.NONE)
--Group.new("cCppOutIf2",     colors.grey,   colors.NONE)
--Group.new("cCppOutElse",    colors.grey,   colors.NONE)
--Group.new("cCppOutSkip",    colors.grey,   colors.NONE)
Group.new("cppBoolean",     colors.brown,  colors.NONE, styles.bold)
Group.new("cppFloat",       colors.brown,  colors.NONE, styles.bold)
Group.new("cppNumber",      colors.brown,  colors.NONE, styles.bold)
Group.new("cppNumbers",     colors.brown,  colors.NONE, styles.bold)
Group.new("cErrInParen",    colors.white,  colors.NONE, styles.NONE)
Group.new("cErrInBracket",  colors.white,  colors.NONE, styles.NONE)

-- Tree-sitter
Group.new("TSConstant",       colors.white,  colors.NONE, styles.NONE)
Group.new("TSPunctBracket",   colors.white,  colors.NONE, styles.NONE)
Group.new("TSPunctDelimiter", colors.white,  colors.NONE, styles.NONE)
Group.new("TSOperator",       colors.white,  colors.NONE, styles.NONE)
Group.new("TSFuncMacro",      colors.yellow, colors.NONE, styles.NONE)
Group.new("TSNumber",         colors.brown,  colors.NONE, styles.BOLD)
Group.new("TSBoolean",        colors.brown,  colors.NONE, styles.BOLD)
Group.new("TSCharacter",      colors.brown,  colors.NONE, styles.BOLD)
Group.new("TSConditional",    colors.yellow, colors.NONE, styles.NONE)
Group.new("TSRepeat",         colors.yellow, colors.NONE, styles.NONE)
Group.new("TSKeyword",        colors.yellow, colors.NONE, styles.NONE)
Group.new("cppTSKeyword",     colors.yellow, colors.NONE, styles.NONE)
Group.new("TSConstMacro",     colors.yellow, colors.NONE, styles.NONE)
Group.new("TSNote",           colors.green,  colors.NONE, styles.BOLD)

-- Org-mode
Group.new("Title",                    colors.blue)
Group.new("Folded",                   colors.grey,  colors.background, styles.NONE)
Group.new("org_properties_delimiter", colors.grey)
Group.new("org_property",             colors.grey)
Group.new("org_property_value",       colors.grey)
Group.new("OrgHeadlineLevel1",        colors.yellow)
Group.new("OrgHeadlineLevel2",        colors.yellow)
Group.new("OrgHeadlineLevel3",        colors.yellow)
Group.new("OrgHeadlineLevel4",        colors.yellow)
Group.new("OrgHeadlineLevel5",        colors.yellow)

-- which-key
--Group.new('WhichKey',            colors.white, colors.bg)
--Group.new('WhichKeyGroup',       colors.white, colors.bg)
Group.new('WhichKeyNormal',      colors.white, colors.bg2)
--Group.new('WhichKeyBorder',      colors.white, colors.bg)
--Group.new('WhichKeyDesc',        colors.white, colors.bg)
--Group.new('WhichKeyTitle',       colors.white, colors.bg)
--Group.new('WhichKeyValue',       colors.white, colors.bg)
--Group.new('WhichKeySeparator',   colors.white, colors.bg)
--Group.new('WhichKeyDesc',        colors.white, colors.bg)


-- plain lua colorscheme:
-- -- colors/theme.lua
-- 
-- vim.cmd("highlight clear")
-- if vim.fn.exists("syntax_on") == 1 then
--   vim.cmd("syntax reset")
-- end
-- vim.g.colors_name = "theme"
-- vim.o.termguicolors = true
-- 
-- local hl = function(group, opts)
--   vim.api.nvim_set_hl(0, group, opts)
-- end
-- 
-- local p = {
--   white      = "#ffffff",
--   green      = "#99BB66",
--   yellow     = "#ECBE7B",
--   blue       = "#4DB5BD",
--   darkblue   = "#003c64",
--   brown      = "#B4916D",
--   grey       = "#404940",
--   background = "#18191b",
--   bg2        = "#1f1f1f",
-- }
-- 
-- -- Core
-- hl("Normal",      { fg = p.white, bg = p.background })
-- hl("NormalFloat", { fg = p.white, bg = p.bg2 })
-- hl("Visual",      { bg = p.darkblue })
-- hl("Search",      { fg = "#000000", bg = p.yellow })
-- hl("MatchParen",  { bg = p.darkblue })
-- hl("Whitespace",  { fg = p.grey, bg = p.background })
-- hl("FloatBorder", { fg = p.blue, bg = p.bg2 })
-- hl("Pmenu",       { fg = p.white, bg = p.bg2 })
-- hl("PmenuSel",    { fg = p.white, bg = p.darkblue })
-- 
-- -- Syntax
-- hl("Function",    { fg = p.white })
-- hl("Variable",    { fg = p.white })
-- hl("Comment",     { fg = p.green })
-- hl("Identifier",  { fg = p.white })
-- hl("Keyword",     { fg = p.yellow })
-- hl("String",      { fg = p.brown })
-- hl("Structure",   { fg = p.yellow })
-- hl("Todo",        { fg = p.yellow, bold = true })
-- hl("Type",        { fg = p.blue })
-- hl("Number",      { fg = p.brown })
-- hl("Include",     { fg = p.yellow })
-- hl("PreProc",     { fg = p.yellow })
-- hl("Statement",   { fg = p.yellow })
-- hl("Constant",    { fg = p.yellow })
-- hl("Special",     { fg = p.brown })
-- hl("Conditional", { fg = p.yellow })
-- hl("Operator",    { fg = p.white })
-- hl("Repeat",      { fg = p.yellow })
-- 
-- -- C/C++
-- hl("cType",          { fg = p.blue })
-- hl("cTypedef",       { fg = p.yellow })
-- hl("cStructure",     { fg = p.yellow })
-- hl("cConditional",   { fg = p.yellow })
-- hl("cRepeat",        { fg = p.yellow })
-- hl("cCharacter",     { fg = p.brown })
-- hl("cBlock",         { fg = p.brown, bold = true })
-- hl("cblock",         { fg = p.white, bold = true })
-- hl("cParen",         { fg = p.white, bold = true })
-- hl("cFormat",        { fg = p.white, bold = true })
-- hl("cSpecial",       { fg = p.white, bold = true })
-- hl("cCppOutWrapper", { fg = p.yellow })
-- hl("cppBoolean",     { fg = p.brown, bold = true })
-- hl("cppFloat",       { fg = p.brown, bold = true })
-- hl("cppNumber",      { fg = p.brown, bold = true })
-- hl("cppNumbers",     { fg = p.brown, bold = true })
-- hl("cErrInParen",    { fg = p.white })
-- hl("cErrInBracket",  { fg = p.white })
-- 
-- -- Treesitter (legacy TSFoo names, still work via compatibility layer)
-- hl("TSConstant",       { fg = p.white })
-- hl("TSPunctBracket",   { fg = p.white })
-- hl("TSPunctDelimiter", { fg = p.white })
-- hl("TSOperator",       { fg = p.white })
-- hl("TSFuncMacro",      { fg = p.yellow })
-- hl("TSNumber",         { fg = p.brown, bold = true })
-- hl("TSBoolean",        { fg = p.brown, bold = true })
-- hl("TSCharacter",      { fg = p.brown, bold = true })
-- hl("TSConditional",    { fg = p.yellow })
-- hl("TSRepeat",         { fg = p.yellow })
-- hl("TSKeyword",        { fg = p.yellow })
-- hl("cppTSKeyword",     { fg = p.yellow })
-- hl("TSConstMacro",     { fg = p.yellow })
-- hl("TSNote",           { fg = p.green, bold = true })
-- 
-- -- Org-mode
-- hl("Title",                    { fg = p.blue })
-- hl("Folded",                   { fg = p.grey, bg = p.background })
-- hl("org_properties_delimiter", { fg = p.grey })
-- hl("org_property",             { fg = p.grey })
-- hl("org_property_value",       { fg = p.grey })
-- hl("OrgHeadlineLevel1",        { fg = p.yellow })
-- hl("OrgHeadlineLevel2",        { fg = p.yellow })
-- hl("OrgHeadlineLevel3",        { fg = p.yellow })
-- hl("OrgHeadlineLevel4",        { fg = p.yellow })
-- hl("OrgHeadlineLevel5",        { fg = p.yellow })
-- 
-- -- which-key
-- hl("WhichKeyNormal", { fg = p.white, bg = p.bg2 })
