from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})  # Allow specific origin

# In-memory storage for rules
rules = []

# Define the Node for AST
class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left       # left child node
        self.right = right     # right child node
        self.value = value     # value for operand nodes

    def to_dict(self):
        return {
            "type": self.type,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
            "value": self.value
        }

    @staticmethod
    def from_dict(data):
        if not data:
            return None
        node_type = data['type']
        left = Node.from_dict(data['left']) if data['left'] else None
        right = Node.from_dict(data['right']) if data['right'] else None
        value = data['value']
        return Node(node_type, left, right, value)

# Utility function to parse rule string into AST (simplified parser)
def parse_rule(rule_string):
    # For demonstration, we'll mock a simple parsing mechanism
    if "AND" in rule_string:
        left, right = rule_string.split("AND")
        return Node("operator", left=Node("operand", value=left.strip()), right=Node("operand", value=right.strip()))
    elif "OR" in rule_string:
        left, right = rule_string.split("OR")
        return Node("operator", left=Node("operand", value=left.strip()), right=Node("operand", value=right.strip()))
    else:
        return Node("operand", value=rule_string.strip())

# Route to create a new rule
@app.route('/api/rules', methods=['POST'])
def create_rule():
    data = request.get_json()
    rule_string = data.get('rule_string')
    if not rule_string:
        return jsonify({"error": "Rule string is required"}), 400

    ast = parse_rule(rule_string)
    rules.append({"rule_string": rule_string, "ast": ast.to_dict()})  # Store in memory

    return jsonify({"message": "Rule created", "rule": ast.to_dict()})

# Route to combine multiple rules
@app.route('/api/rules/combine', methods=['POST'])
def combine_rules():
    data = request.get_json()
    rule_strings = data.get('rules')
    if not rule_strings or len(rule_strings) < 2:
        return jsonify({"error": "At least two rules are required"}), 400

    combined_ast = Node("operator", value="AND")
    for rule_string in rule_strings:
        ast = parse_rule(rule_string)
        if not combined_ast.left:
            combined_ast.left = ast
        else:
            combined_ast.right = ast

    return jsonify({"message": "Rules combined", "combined_rule": combined_ast.to_dict()})

def evaluate(node, data):
    if node is None:
        return False  # Handle None node gracefully
    if node.type == "operand":
        condition = node.value
        key, operator, value = condition.split()  # Simplified logic
        if key not in data:
            return False  # Key does not exist in user data
        if operator == '>':
            return data[key] > int(value)
        elif operator == '<':
            return data[key] < int(value)
        elif operator == '=':
            return data[key] == value.strip("'")
    elif node.type == "operator":
        if node.value == "AND":
            return evaluate(node.left, data) and evaluate(node.right, data)
        elif node.value == "OR":
            return evaluate(node.left, data) or evaluate(node.right, data)
    return False

# Route to evaluate a rule
@app.route('/api/rules/evaluate', methods=['POST'])
def evaluate_rule():
    data = request.get_json()
    user_data = data.get('user_data')
    ast_data = data.get('json_data')

    if not user_data or not ast_data:
        return jsonify({"error": "User data and AST are required"}), 400

    try:
        ast = Node.from_dict(ast_data)
    except Exception as e:
        return jsonify({"error": f"Invalid AST provided: {str(e)}"}), 400

    result = evaluate(ast, user_data)
    return jsonify({"result": result})

@app.errorhandler(Exception)
def handle_exception(e):
    # Log the error details
    print(f"Error: {e}")
    return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
