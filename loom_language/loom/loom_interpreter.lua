-- Define LoomInterpreter class
LoomInterpreter = {
    variables = {},
    functions = {},
    dependencies = {}
}

-- Define LoomInterpreter methods
function LoomInterpreternew()
    local obj = {}
    setmetatable(obj, self)
    self.__index = self
    return obj
end

function LoomInterpreterinterpret(code)
    local lines = {}
    for line in string.gmatch(code, [^rn]+) do
        table.insert(lines, line)
    end

    for _, line in ipairs(lines) do
        if string.match(linestrip(), ^function) then
            selfdefine_function(line)
        elseif string.match(line, =) then
            selfassign_variable(line)
        elseif string.match(linestrip(), ^loop) then
            selfexecute_loop(line)
        elseif string.match(line, placeholder) then
            selfhandle_placeholder(line)
        elseif string.match(linestrip(), ^require.dependency) then
            selfload_dependency(line)
        elseif string.match(linestrip(), ^debug.system.log) then
            selflog_message(line)
        elseif string.match(linestrip(), ^if) then
            selfevaluate_if_statement(line)
        elseif string.match(linestrip(), ^else) then
            selfevaluate_else_statement()
        elseif string.match(linestrip(), ^end) then
            -- Do nothing, end of block
        elseif string.match(linestrip(), ^#) or string.match(linestrip(), ^$) then
            -- Comment or empty line, skip
        else
            print(Error Unrecognized command  .. line)
        end
    end
end

function LoomInterpreterdefine_function(line)
    local func_name = string.match(line, function%s+(%w+))
    local params = string.match(line, %((.-)%))
    params = string.gmatch(params, [^,]+)
    self.functions[func_name] = function(...)
        return load(return  .. linesub(linefind(=) + 1))()(...)
    end
end

function LoomInterpreterassign_variable(line)
    local var_name, value = linematch((%w+)%s=%s(.))
    self.variables[var_name] = selfevaluate_expression(value)
end

function LoomInterpreterevaluate_expression(expr)
    if string.match(expr, %(.+%)) then
        local func_name = exprmatch((%w+)%()
        local args = exprmatch(%((.-)%))
        args = string.gmatch(args, [^,]+)
        local evaluated_args = {}
        for arg in args do
            if self.variables[arg] then
                table.insert(evaluated_args, self.variables[arg])
            else
                table.insert(evaluated_args, arg)
            end
        end
        return self.functions[func_name](table.unpack(evaluated_args))
    elseif self.variables[expr] then
        return self.variables[expr]
    else
        return expr
    end
end

function LoomInterpreterexecute_loop(line)
    local times, body = linematch(loop%s%((%d+)%)%s(.))
    for i = 1, tonumber(times) do
        selfinterpret(body)
    end
end

function LoomInterpreterhandle_placeholder(line)
    local var_name, value = linematch((%w+)%s=%s(.))
    self.variables[var_name] = selfevaluate_expression(value)
end

function LoomInterpreterload_dependency(line)
    local filename = linematch(require.dependency%s%(%s([^]+)%s%))
    if not self.dependencies[filename] then
        local file = io.open(filename, r)
        if file then
            self.dependencies[filename] = fileread(a)
            fileclose()
        else
            print(Error Dependency file ' .. filename .. ' not found.)
        end
    end
    selfinterpret(self.dependencies[filename])
end

function LoomInterpreterlog_message(line)
    local message = linematch(debug.system.log%s%(%s([^]+)%s%))
    print(log type of( .. linematch(debug.system.log%s%.(%w+)) .. )  .. message)
end

function LoomInterpreterevaluate_if_statement(line)
    local condition = linematch(if%s+(.+))
    if selfevaluate_expression(condition) then
        -- Condition is true, continue execution
    else
        local lines = {}
        for line in string.gmatch(line, [^rn]+) do
            table.insert(lines, line)
        end
        local index = 1
        local else_index = nil
        for i, l in ipairs(lines) do
            if string.match(lstrip(), ^else) then
                else_index = i
                break
            elseif string.match(lstrip(), ^end) then
                break
            end
        end
        if else_index then
            -- Jump to the 'else' statement
            selfinterpret(lines[else_index])
        end
    end
end

function LoomInterpreterevaluate_else_statement()
    -- Do nothing, skip execution of the else block
end

function LoomInterpreterrun_script(file_name)
    local script_path = Scripts .. file_name
    local file = io.open(script_path, r)
    if file then
        local script_code = fileread(a)
        fileclose()
        selfinterpret(script_code)
    else
        print(Error Script ' .. file_name .. ' not found.)
    end
end

-- Example Loom code
local loom_code = [[
debug.system.log(Starting Loom code execution)
]]

-- Create and run the interpreter
local interpreter = LoomInterpreternew()
interpreterinterpret(loom_code)
