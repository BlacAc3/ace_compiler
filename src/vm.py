class VirtualMachine:
    def __init__(self):
        self.stack = []
        self.memory = {}

    def execute(self, bytecode):
        location = None
        index = 0
        code_blocks={}

        # First pass to find all code block labels and their indices
        print("--- Pre-processing: Finding code blocks ---")
        temp_index = 0
        for instruction in bytecode:
            if instruction.endswith(":"):
                label = instruction
                code_blocks[label] = temp_index + 1 # Store index of instruction *after* label
                print(f"  Found label '{label}' at index {temp_index + 1}")
            temp_index += 1
        print("--- Finished Pre-processing ---")
        print(f"Code blocks found: {code_blocks}")
        print("\n--- Starting Execution ---")


        while index < len(bytecode):
            instruction = bytecode[index]
            print(f"\n--- Executing instruction at index {index}: {instruction} ---")
            print(f"  Current Stack (before): {self.stack}")
            print(f"  Current Memory (before): {self.memory}")
            print(f"  Current Target Location: {location}")

            original_index = index # Store index before potential jump
            index += 1 # Increment index *before* processing instruction
            parts = instruction.split()

            # Handle labels first - they are markers, not executable instructions themselves
            if instruction.endswith(":") and instruction in code_blocks and "GOTO" != parts[0] and "JUMP" not in parts[0]:
                print(f"  Encountered label '{instruction}', continuing execution.")
                # If we were seeking this location, we've found it.
                if location and location == instruction:
                    print(f"  Matched sought location: '{location}'")
                    location = None # Clear the seek target
                continue # Move to the next instruction

            # Check if we are seeking a location
            if location and location not in code_blocks:
                print(f"  Seeking location '{location}', skipping instruction '{instruction}'")
                continue # Skip instruction if we are seeking a specific label


            # --- Instruction Execution ---
            op = parts[0]

            if op == "PUSH":
                value = int(parts[1])
                self.stack.append(value)
                print(f"  PUSH: Pushed {value} onto the stack.")

            elif op == "LOAD":
                var_name = parts[1]
                if var_name in self.memory:
                    value = self.memory[var_name]
                    self.stack.append(value)
                    print(f"  LOAD: Loaded value {value} from variable '{var_name}' onto the stack.")
                else:
                    print(f"  ERROR: Undefined variable: {var_name}")
                    raise RuntimeError(f"Undefined variable: {var_name}")

            elif op == "STORE":
                var_name = parts[1]
                if not self.stack:
                     print(f"  ERROR: Stack underflow during STORE '{var_name}'")
                     raise RuntimeError(f"Stack underflow during STORE '{var_name}'")
                value = self.stack.pop()
                self.memory[var_name] = value
                print(f"  STORE: Stored value {value} into variable '{var_name}'. Popped from stack.")

            elif op in {"ADD", "SUB", "MUL", "DIV", "GT", "LT", "EQUAL"}:
                if len(self.stack) < 2:
                    print(f"  ERROR: Stack underflow during {op}")
                    raise RuntimeError(f"Stack underflow during {op}")
                b = self.stack.pop()
                a = self.stack.pop()
                result = None
                op_symbol = ""
                if op == "ADD":
                    result = a + b
                    op_symbol = "+"
                elif op == "SUB":
                    result = a - b
                    op_symbol = "-"
                elif op == "MUL":
                    result = a * b
                    op_symbol = "*"
                elif op == "DIV":
                    if b == 0:
                        print(f"  ERROR: Division by zero during DIV")
                        raise RuntimeError("Division by zero")
                    result = a // b  # Integer division
                    op_symbol = "//"
                elif op == "GT":
                    result = a > b
                    op_symbol = ">"
                elif op == "LT":
                    result = a < b
                    op_symbol = "<"
                elif op == "EQUAL":
                    result = a == b
                    op_symbol = "=="

                print(f"  {op}: {a} {op_symbol} {b} = {result}. Popped {a}, {b}. Pushing result.")
                self.stack.append(result)


            elif op == "JUMP_IF_FALSE":
                if not self.stack:
                    print(f"  ERROR: Stack underflow during JUMP_IF_FALSE")
                    raise RuntimeError(f"Stack underflow during JUMP_IF_FALSE")
                condition = self.stack.pop()
                target_label = parts[1] + ":"
                print(f"  JUMP_IF_FALSE: Condition = {condition} (popped from stack). Target = '{target_label}'.")
                if condition is False: # Explicitly check for False
                    if target_label in code_blocks:
                        location = target_label
                        index = code_blocks[target_label] # Set index directly
                        print(f"  JUMP_IF_FALSE: Condition is False. Jumping to '{location}' at index {index}.")
                        # No 'continue' here, the loop will use the new index
                    else:
                         print(f"  ERROR: Unknown jump target label: {target_label}")
                         raise RuntimeError(f"Unknown jump target label: {target_label}")
                else:
                    print(f"  JUMP_IF_FALSE: Condition is not False. No jump.")


            elif op == "GOTO":
                target_label = parts[1]
                print(f"  GOTO: Target = '{target_label}'.")
                if target_label in code_blocks:
                    location = target_label
                    index = code_blocks[target_label] # Set index directly
                    print(f"  GOTO: Jumping to '{location}' at index {index}.")
                     # No 'continue' here, the loop will use the new index
                else:
                    print(f"  ERROR: Unknown jump target label: {target_label}")
                    raise RuntimeError(f"Unknown jump target label: {target_label}")

            else:
                # This handles the case where an instruction is not a label and not a known operation
                # It might also catch labels if the pre-processing logic fails or isn't comprehensive
                if not instruction.endswith(":"): # Avoid raising error for labels missed in pre-processing if any
                    print(f"  ERROR: Unknown instruction: {instruction}")
                    raise RuntimeError(f"Unknown instruction: {instruction}")
                else:
                    # If it's a label we somehow missed or are seeking, handle it gracefully
                    print(f"  Skipping potential label '{instruction}' encountered during execution phase.")
                    # If we were seeking this, mark it as found
                    if location and location == instruction:
                        print(f"  Matched sought location: '{location}'")
                        location = None


            print(f"  Current Stack (after): {self.stack}")
            print(f"  Current Memory (after): {self.memory}")
            # Check if a jump occurred by comparing original_index and current index
            if index != original_index + 1 and location: # Check if index was changed by a jump
                 print(f"  Jump occurred. Next instruction will be at index {index} (target: '{location}').")
            else:
                 print(f"  Proceeding sequentially. Next instruction index: {index}")
                 location = None # Ensure location seeking is reset if we didn't jump


        print("\n--- Execution Finished ---")
        print(f"Final Stack: {self.stack}")
        self.print_memory()


    def filter_memory(self):
        # This filtering is usually for final output, keep internal memory complete
        print("--- Filtering Memory for Output ---")
        filtered_memory = {k: v for k, v in self.memory.items() if not k.startswith('t')}
        print(f"  Original Memory: {self.memory}")
        print(f"  Filtered Memory: {filtered_memory}")
        return filtered_memory

    def print_memory(self):
        # Print memory, possibly filtering temporary variables for clarity
        # For debugging, maybe show all memory first?
        print("--- Final Memory State ---")
        print(f"  Raw Memory: {self.memory}")
        filtered_memory = {k: v for k, v in self.memory.items() if not k.startswith('t')}
        print(f"  Filtered Memory (no 't' vars): {filtered_memory}")
