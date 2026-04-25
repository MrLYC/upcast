"""CST (ast-grep / tree-sitter) 与 AST (astroid) 双向节点映射工具。

本模块提供 CSTASTMapper 类，用于在 ast-grep（基于 tree-sitter 的具体语法树）
和 astroid（抽象语法树）之间进行双向节点映射和模式搜索。

核心映射原则：
- 使用行列坐标范围（lineno, col_offset, end_lineno, end_col_offset）作为映射基准。
- 对于精确坐标匹配的节点，直接返回对应节点。
- 对于 tree-sitter 的 CST 特有节点（如 argument_list、block），
  寻找最小包含该范围的 astroid 父节点（b_contains_a 策略）。
- 对于 astroid 的无坐标节点（如 Arguments、Comprehension、MatchCase、Module），
  递归映射其子节点或父节点。

坐标约定（两侧统一）：
- lineno / end_lineno: 1-based 行号
- col_offset / end_col_offset: 0-based 列偏移（exclusive 结尾，与 tree-sitter 一致）
"""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import TYPE_CHECKING

from astroid import nodes

if TYPE_CHECKING:
    from ast_grep_py import SgNode, SgRoot

logger = logging.getLogger(__name__)

# 坐标范围类型：(start_line, start_col, end_line, end_col)，均为 int
_Range = tuple[int, int, int, int]


# ============================================================
# 节点类型映射表（基于双向映射实验数据）
# ============================================================

# tree-sitter kind -> 对应的 astroid 节点类型列表（按优先级排序）
_TS_TO_ASTROID: dict[str, list[str]] = {
    # 定义与声明
    "class_definition": ["ClassDef"],
    "function_definition": ["FunctionDef", "AsyncFunctionDef"],
    "decorated_definition": ["FunctionDef", "AsyncFunctionDef", "ClassDef"],
    "decorator": ["Decorators"],
    # 赋值
    "assignment": ["Assign", "AnnAssign"],
    "augmented_assignment": ["AugAssign"],
    "expression_statement": ["Assign", "AnnAssign", "AugAssign", "Expr", "Call", "Yield", "YieldFrom", "Await"],
    # 控制流
    "if_statement": ["If"],
    "for_statement": ["For"],
    "while_statement": ["While"],
    "try_statement": ["Try"],
    "with_statement": ["With"],
    "break_statement": ["Break"],
    "continue_statement": ["Continue"],
    "pass_statement": ["Pass"],
    "return_statement": ["Return"],
    "raise_statement": ["Raise"],
    "delete_statement": ["Delete"],
    "assert_statement": ["Assert"],
    "global_statement": ["Global"],
    "nonlocal_statement": ["Nonlocal"],
    # 表达式
    "binary_operator": ["BinOp"],
    "boolean_operator": ["BoolOp"],
    "unary_operator": ["UnaryOp"],
    "not_operator": ["UnaryOp"],
    "comparison_operator": ["Compare"],
    "conditional_expression": ["IfExp"],
    "named_expression": ["NamedExpr"],
    "call": ["Call"],
    "attribute": ["Attribute", "AssignAttr"],
    "subscript": ["Subscript"],
    "slice": ["Slice"],
    "identifier": ["Name", "AssignName", "DelName"],
    # 数据结构
    "list": ["List"],
    "tuple": ["Tuple"],
    "set": ["Set"],
    "dictionary": ["Dict"],
    "list_comprehension": ["ListComp"],
    "set_comprehension": ["SetComp"],
    "dictionary_comprehension": ["DictComp"],
    "generator_expression": ["GeneratorExp"],
    # 常量与字符串
    "integer": ["Const"],
    "string": ["Const", "JoinedStr", "FormattedValue"],
    "true": ["Const"],
    "false": ["Const"],
    "none": ["Const"],
    # 其他
    "lambda": ["Lambda"],
    "import_statement": ["Import"],
    "import_from_statement": ["ImportFrom"],
    "except_clause": ["ExceptHandler"],
    "keyword_argument": ["Keyword"],
    "await": ["Await"],
    "yield": ["Yield", "YieldFrom"],
    "match_statement": ["Match"],
    "case_pattern": ["MatchValue", "MatchAs", "Const"],
}

# astroid 节点类型 -> 对应的 tree-sitter kind 列表（按优先级排序）
_ASTROID_TO_TS: dict[str, list[str]] = {
    # 定义与声明
    "ClassDef": ["class_definition"],
    "FunctionDef": ["function_definition", "decorated_definition"],
    "AsyncFunctionDef": ["function_definition"],
    "Decorators": ["decorator"],
    # 赋值
    "Assign": ["assignment", "expression_statement"],
    "AnnAssign": ["assignment", "expression_statement"],
    "AugAssign": ["augmented_assignment", "expression_statement"],
    # 控制流
    "If": ["if_statement"],
    "For": ["for_statement"],
    "While": ["while_statement"],
    "Try": ["try_statement"],
    "With": ["with_statement"],
    "Break": ["break_statement"],
    "Continue": ["continue_statement"],
    "Pass": ["pass_statement"],
    "Return": ["return_statement"],
    "Raise": ["raise_statement"],
    "Delete": ["delete_statement"],
    "Assert": ["assert_statement"],
    "Global": ["global_statement"],
    "Nonlocal": ["nonlocal_statement"],
    # 表达式
    "BinOp": ["binary_operator"],
    "BoolOp": ["boolean_operator"],
    "UnaryOp": ["unary_operator", "not_operator"],
    "Compare": ["comparison_operator"],
    "IfExp": ["conditional_expression"],
    "NamedExpr": ["named_expression"],
    "Call": ["call"],
    "Attribute": ["attribute"],
    "AssignAttr": ["attribute"],
    "Subscript": ["subscript"],
    "Slice": ["slice"],
    "Name": ["identifier"],
    "AssignName": ["identifier"],
    "DelName": ["identifier"],
    # 数据结构
    "List": ["list"],
    "Tuple": ["tuple"],
    "Set": ["set"],
    "Dict": ["dictionary"],
    "ListComp": ["list_comprehension"],
    "SetComp": ["set_comprehension"],
    "DictComp": ["dictionary_comprehension"],
    "GeneratorExp": ["generator_expression"],
    # 常量与字符串
    "Const": ["integer", "string", "true", "false", "none"],
    "JoinedStr": ["string"],
    "FormattedValue": ["string"],
    # 其他
    "Lambda": ["lambda"],
    "Import": ["import_statement"],
    "ImportFrom": ["import_from_statement"],
    "ExceptHandler": ["except_clause"],
    "Keyword": ["keyword_argument"],
    "Await": ["await"],
    "Yield": ["yield"],
    "YieldFrom": ["yield"],
    "Match": ["match_statement"],
    "MatchValue": ["case_pattern"],
    "MatchAs": ["case_pattern"],
    "Expr": ["expression_statement"],
}

# astroid 中天生缺失完整坐标的节点类型（不可直接用于坐标映射）
_ASTROID_NO_COORDS: frozenset[str] = frozenset({"Arguments", "Comprehension", "MatchCase", "Module"})


def _get_ast_range(node: nodes.NodeNG) -> _Range | None:
    """获取 astroid 节点的坐标范围，若坐标不完整则返回 None。"""
    for attr in ("lineno", "col_offset", "end_lineno", "end_col_offset"):
        if getattr(node, attr, None) is None:
            return None
    return (node.lineno, node.col_offset, node.end_lineno, node.end_col_offset)  # type: ignore[return-value]


def _range_contains(outer: _Range, inner: _Range) -> bool:
    """判断 outer 范围是否完全包含 inner 范围。"""
    return (outer[0], outer[1]) <= (inner[0], inner[1]) and (outer[2], outer[3]) >= (inner[2], inner[3])


def _range_size(rng: _Range) -> tuple[int, int]:
    """返回范围大小（行跨度，列跨度），用于排序找最小包含节点。"""
    return (rng[2] - rng[0], rng[3] - rng[1])


class CSTASTMapper:
    """ast-grep (tree-sitter CST) 与 astroid (AST) 双向节点映射器。

    在初始化时遍历两棵树并建立坐标索引，后续所有映射和搜索操作均基于索引进行，
    不需要重复遍历树结构。

    Examples:
        >>> import astroid
        >>> from ast_grep_py import SgRoot
        >>> source = "class MyModel(BaseModel): pass"
        >>> mapper = CSTASTMapper(SgRoot(source, "python"), astroid.parse(source))
        >>> ts_nodes = mapper.search_cst("class $NAME($$$BASES): $$$BODY")
        >>> ast_nodes = mapper.search_ast("class $NAME($$$BASES): $$$BODY")
    """

    def __init__(self, sg_root: SgRoot, astroid_tree: nodes.Module) -> None:
        """初始化映射器并建立坐标索引。

        Args:
            sg_root: ast-grep SgRoot 对象（通过 SgRoot(source, "python") 创建）。
            astroid_tree: astroid 解析树（通过 astroid.parse(source) 创建）。
        """
        self.sg_root = sg_root
        self.astroid_tree = astroid_tree

        # 坐标索引：_Range -> 节点列表
        self._ts_by_range: dict[_Range, list[SgNode]] = defaultdict(list)
        self._ast_by_range: dict[_Range, list[nodes.NodeNG]] = defaultdict(list)

        self._build_indices()

    # ============================================================
    # 索引构建
    # ============================================================

    def _build_indices(self) -> None:
        """遍历两棵树，建立坐标索引。"""
        self._index_ts(self.sg_root.root())
        self._index_ast(self.astroid_tree)

    def _index_ts(self, node: SgNode) -> None:
        """递归索引 tree-sitter 节点（仅索引 named 节点）。"""
        if node.is_named():
            rng = node.range()
            # tree-sitter 使用 0-based 行号，统一转为 1-based
            key: _Range = (rng.start.line + 1, rng.start.column, rng.end.line + 1, rng.end.column)
            self._ts_by_range[key].append(node)
        for child in node.children():
            self._index_ts(child)

    def _index_ast(self, node: nodes.NodeNG) -> None:
        """递归索引 astroid 节点（仅索引坐标完整的节点）。"""
        rng = _get_ast_range(node)
        if rng is not None:
            self._ast_by_range[rng].append(node)
        for child in node.get_children():
            self._index_ast(child)

    # ============================================================
    # 内部辅助方法
    # ============================================================

    def _ts_range(self, node: SgNode) -> _Range:
        """获取 tree-sitter 节点的坐标范围（1-based 行，0-based 列）。"""
        rng = node.range()
        return (rng.start.line + 1, rng.start.column, rng.end.line + 1, rng.end.column)

    def _find_min_containing_ast(self, ts_rng: _Range) -> nodes.NodeNG | None:
        """寻找最小包含指定 tree-sitter 范围的 astroid 节点。

        用于处理 CST 特有节点（如 argument_list）无法精确匹配时的降级策略。
        """
        best: tuple[_Range, nodes.NodeNG] | None = None
        for ast_rng, ast_nodes in self._ast_by_range.items():
            if _range_contains(ast_rng, ts_rng):
                if best is None or _range_size(ast_rng) < _range_size(best[0]):
                    best = (ast_rng, ast_nodes[0])
        return best[1] if best else None

    def _find_min_containing_ts(self, ast_rng: _Range) -> SgNode | None:
        """寻找最小包含指定 astroid 范围的 tree-sitter 节点。

        用于处理 astroid 无坐标节点的降级策略。
        """
        best: tuple[_Range, SgNode] | None = None
        for ts_rng, ts_nodes in self._ts_by_range.items():
            if _range_contains(ts_rng, ast_rng):
                if best is None or _range_size(ts_rng) < _range_size(best[0]):
                    best = (ts_rng, ts_nodes[0])
        return best[1] if best else None

    # ============================================================
    # 公开 API
    # ============================================================

    def cst_to_ast(self, sg_node: SgNode) -> nodes.NodeNG | None:
        """将 tree-sitter 节点映射到最匹配的 astroid 节点。

        映射策略（按优先级）：
        1. 精确坐标匹配 + 类型匹配。
        2. 精确坐标匹配（忽略类型）。
        3. 寻找最小包含该范围的 astroid 父节点（处理 CST 特有节点）。

        Args:
            sg_node: tree-sitter 节点（ast_grep_py.SgNode）。

        Returns:
            对应的 astroid 节点，无法映射时返回 None。
        """
        if not sg_node.is_named():
            return None

        ts_rng = self._ts_range(sg_node)

        # 精确坐标匹配
        if ts_rng in self._ast_by_range:
            candidates = self._ast_by_range[ts_rng]
            expected_types = _TS_TO_ASTROID.get(sg_node.kind(), [])
            # 优先返回类型匹配的节点
            for node in candidates:
                if type(node).__name__ in expected_types:
                    return node
            return candidates[0]

        # 降级：寻找最小包含父节点
        return self._find_min_containing_ast(ts_rng)

    def ast_to_cst(self, ast_node: nodes.NodeNG) -> SgNode | None:
        """将 astroid 节点映射到最匹配的 tree-sitter 节点。

        映射策略（按优先级）：
        1. 对于无坐标节点（Arguments、Comprehension 等），递归映射子节点或父节点。
        2. 精确坐标匹配 + 类型匹配。
        3. 精确坐标匹配（忽略类型）。
        4. 寻找最小包含该范围的 tree-sitter 父节点。

        Args:
            ast_node: astroid 节点（astroid.nodes.NodeNG）。

        Returns:
            对应的 tree-sitter 节点，无法映射时返回 None。
        """
        node_type = type(ast_node).__name__

        # 无坐标节点：递归映射子节点，再尝试父节点
        if node_type in _ASTROID_NO_COORDS:
            for child in ast_node.get_children():
                result = self.ast_to_cst(child)
                if result is not None:
                    return result
            if ast_node.parent is not None:
                return self.ast_to_cst(ast_node.parent)
            return None

        ast_rng = _get_ast_range(ast_node)
        if ast_rng is None:
            return None

        # 精确坐标匹配
        if ast_rng in self._ts_by_range:
            candidates = self._ts_by_range[ast_rng]
            expected_kinds = _ASTROID_TO_TS.get(node_type, [])
            for node in candidates:
                if node.kind() in expected_kinds:
                    return node
            return candidates[0]

        # 降级：寻找最小包含父节点
        return self._find_min_containing_ts(ast_rng)

    def search_cst(self, pattern: str) -> list[SgNode]:
        """使用 ast-grep 模式字符串搜索 tree-sitter 节点。

        Args:
            pattern: ast-grep 模式字符串，例如 ``"class $NAME($$$BASES): $$$BODY"``。

        Returns:
            所有匹配的 tree-sitter 节点列表。
        """
        try:
            return list(self.sg_root.root().find_all(pattern=pattern))
        except Exception:
            logger.exception("ast-grep 模式搜索失败: pattern=%r", pattern)
            return []

    def search_ast(self, pattern: str) -> list[nodes.NodeNG]:
        """使用 ast-grep 模式字符串搜索，并将结果映射为 astroid 节点。

        先调用 :meth:`search_cst` 获取 tree-sitter 节点，再通过 :meth:`cst_to_ast`
        逐一映射，对结果进行去重后返回。

        Args:
            pattern: ast-grep 模式字符串，例如 ``"def $NAME($$$PARAMS): $$$BODY"``。

        Returns:
            对应的 astroid 节点列表（已去重，保持原始顺序）。
        """
        ts_nodes = self.search_cst(pattern)
        result: list[nodes.NodeNG] = []
        seen: set[int] = set()

        for ts_node in ts_nodes:
            ast_node = self.cst_to_ast(ts_node)
            if ast_node is not None:
                node_id = id(ast_node)
                if node_id not in seen:
                    seen.add(node_id)
                    result.append(ast_node)

        return result
