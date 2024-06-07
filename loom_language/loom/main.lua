-- main.lua

local LoomInterpreter = require("loom_interpreter")
print("code started!")
-- Example Loom code
local loom_code = [[
debug.system.log("Starting Loom code execution")
]]

-- Create and run the interpreter
local interpreter = LoomInterpreter:new()
interpreter:interpret(loom_code)
