import sys
import enum
import argparse
from dataclasses import dataclass, field
from typing import Dict, Set, List, Optional, Union

# --- 1. CORE TYPES & AST ---
class Stage(enum.Enum):
    GHOST = 0
    REAL = 1

@dataclass(frozen=True)
class Type:
    name: str
    is_linear: bool = False
    stage: Stage = Stage.REAL

@dataclass
class Expr: pass

@dataclass
class Var(Expr):
    name: str

@dataclass
class App(Expr):
    func_name: str
    args: List[Expr]
    capability: Optional[str] = None

# --- 2. THE VERIFICATION KERNEL ---
class TotalLCPKernel:
    def __init__(self, capabilities: Set[str], gamma: Dict[str, Type]):
        self.kappa = capabilities 
        self.gamma = gamma 

    def verify(self, expr: Expr, delta: Dict[str, Type]) -> Dict[str, Type]:
        if isinstance(expr, Var):
            if expr.name in delta:
                t = delta[expr.name]
                if t.is_linear:
                    del delta[expr.name] # Linear Consumption
                return delta
            if expr.name in self.gamma:
                return delta
            raise Exception(f"Linearity Violation: '{expr.name}' is unavailable.")

        if isinstance(expr, App):
            if expr.capability and expr.capability not in self.kappa:
                raise Exception(f"Security Violation: Requires '{expr.capability}'")
            
            current_delta = delta
            for arg in expr.args:
                current_delta = self.verify(arg, current_delta)
            return current_delta
        return delta

# --- 3. REPL & FILE PARSER MOCK ---
def parse_simple(line: str) -> Expr:
    """A tiny parser for REPL commands like: func(var1, var2) [Cap]"""
    line = line.strip()
    if "(" not in line: return Var(line)
    
    name = line.split("(")[0]
    rest = line.split("(")[1]
    args_str = rest.split(")")[0]
    args = [Var(a.strip()) for a in args_str.split(",") if a.strip()]
    
    cap = None
    if "[" in line:
        cap = line.split("[")[1].split("]")[0].strip()
        
    return App(name, args, cap)

def run_repl(kernel, delta):
    print("λ_total^LCP Interactive REPL")
    print("Context Δ:", list(delta.keys()))
    print("Caps    Κ:", list(kernel.kappa))
    print("Type 'exit' to quit.\n")
    
    current_delta = delta.copy()
    while True:
        try:
            user_input = input("λ> ")
            if user_input.lower() == 'exit': break
            if not user_input: continue
            
            ast = parse_simple(user_input)
            current_delta = kernel.verify(ast, current_delta)
            print(f"Success. Remaining Δ: {list(current_delta.keys())}")
        except Exception as e:
            print(f"Error: {e}")

def run_file(filename, kernel, delta):
    print(f"Verifying {filename}...")
    try:
        with open(filename, 'r') as f:
            current_delta = delta.copy()
            for line in f:
                if line.strip() and not line.startswith("//"):
                    ast = parse_simple(line)
                    current_delta = kernel.verify(ast, current_delta)
            print("Verification Complete: System is Sound.")
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except Exception as e:
        print(f"Verification Failed: {e}")

# --- 4. CLI ARGUMENT HANDLING ---
if __name__ == "__main__":
    # Setup a mock environment for demonstration
    T_Linear = Type("Resource", is_linear=True)
    mock_gamma = {"print": Type("Fn")}
    mock_delta = {"wallet": T_Linear, "key": T_Linear}
    mock_kappa = {"Admin", "IO"}

    parser = argparse.ArgumentParser(description="λ_total^LCP Kernel CLI")
    parser.add_argument("filename", nargs="?", help="The .lcp file to verify")
    parser.add_argument("--repl", action="store_true", help="Start interactive REPL")
    
    args = parser.parse_args()
    kernel = TotalLCPKernel(mock_kappa, mock_gamma)

    if args.repl:
        run_repl(kernel, mock_delta)
    elif args.filename:
        run_file(args.filename, kernel, mock_delta)
    else:
        parser.print_help()
