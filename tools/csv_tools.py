import pandas as pd
from typing import Dict, Any, List

class CSVTools:
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)
        print(f"✅ Loaded CSV: {csv_path}")
        print(f"   Rows: {len(self.df)}, Columns: {len(self.df.columns)}")
        print(f"   Columns: {list(self.df.columns)}\n")
    
    def list_columns(self) -> Dict[str, List[str]]:
        print("🔧 TOOL CALLED: list_columns")
        result = {"columns": list(self.df.columns)}
        print(f"   Result: {result}\n")
        return result
    
    def dataset_overview(self) -> Dict[str, Any]:
        print("🔧 TOOL CALLED: dataset_overview")
        result = {"rows": len(self.df), "columns": list(self.df.columns)}
        print(f"   Result: {result}\n")
        return result
    
    def average(self, column: str) -> Dict[str, float]:
        print(f"🔧 TOOL CALLED: average")
        print(f"   Parameters: column='{column}'")
        result = {"average": float(self.df[column].mean())}
        print(f"   Result: {result}\n")
        return result
    
    def group_average(self, group_by: str, target: str) -> Dict[str, float]:
        print(f"🔧 TOOL CALLED: group_average")
        print(f"   Parameters: group_by='{group_by}', target='{target}'")
        result = (
            self.df.groupby(group_by)[target]
            .mean()
            .sort_values(ascending=False)
            .to_dict()
        )
        print(f"   Result: {result}\n")
        return result
    
    def filter_rows(self, column: str, operator: str, value: float) -> List[Dict]:
        print(f"🔧 TOOL CALLED: filter_rows")
        print(f"   Parameters: column='{column}', operator='{operator}', value={value}")
        
        if operator == ">":
            filtered = self.df[self.df[column] > value]
        elif operator == "<":
            filtered = self.df[self.df[column] < value]
        else:
            filtered = self.df[self.df[column] == value]
        
        result = filtered.head(10).to_dict(orient="records")
        print(f"   Matched rows: {len(filtered)}, Returning: {len(result)}\n")
        return result
    
    def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Any:
        """Execute a tool by name with given arguments"""
        if tool_name == "list_columns":
            return self.list_columns()
        elif tool_name == "dataset_overview":
            return self.dataset_overview()
        elif tool_name == "average":
            return self.average(args["column"])
        elif tool_name == "group_average":
            return self.group_average(args["group_by"], args["target"])
        elif tool_name == "filter_rows":
            return self.filter_rows(
                args["column"], 
                args["operator"], 
                args["value"]
            )
        else:
            print(f"❌ ERROR: Unknown tool '{tool_name}'\n")
            return {"error": f"Unknown tool: {tool_name}"}


