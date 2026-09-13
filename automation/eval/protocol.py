"""评测的最小 JSON 协议；不解释、裁剪或清洗交付正文。"""
import json
import re


PROTOCOLS = {"rewrite": "shuorenhua-rewrite-v1", "judge": "shuorenhua-judge-v1"}
DIMENSIONS = {
    "fidelity": ("pass", "fail", "review"),
    "task": ("pass", "fail", "review"),
    "quality": ("better", "same", "worse", "review"),
}


class ProtocolError(ValueError):
    """输出结构或覆盖范围不符合协议。"""


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ProtocolError("JSON 含重复字段")
        result[key] = value
    return result


def _invalid_constant(_value):
    raise ProtocolError("JSON 不允许 NaN 或 Infinity")


def strict_json(text):
    """解析标准 JSON，拒绝重复字段和非标准数字；错误不回显输入。"""
    try:
        return json.loads(text, object_pairs_hook=_unique_object, parse_constant=_invalid_constant)
    except (json.JSONDecodeError, TypeError, UnicodeError, RecursionError) as exc:
        raise ProtocolError("不是有效 JSON") from exc


def parse_response(text, phase, expected_ids):
    """校验完整且唯一的 ID，按期望顺序返回记录，text 字段逐字保留。"""
    if phase not in PROTOCOLS or not isinstance(text, str):
        raise ProtocolError("无效 phase 或响应类型")
    if (not expected_ids or any(not isinstance(cid, str) or not cid for cid in expected_ids)
            or len(expected_ids) != len(set(expected_ids))):
        raise ProtocolError("期望 ID 必须非空且唯一")
    text = text.strip()
    fence = re.fullmatch(r"```(?:json)?[ \t]*\r?\n([\s\S]*)\r?\n```", text)
    if fence:
        text = fence.group(1)
    payload = strict_json(text)
    if not isinstance(payload, dict) or set(payload) != {"cases"} or not isinstance(payload["cases"], list):
        raise ProtocolError("顶层必须只有 cases 数组")
    keys = {"id", "text"} if phase == "rewrite" else {"id", "evidence", *DIMENSIONS}
    by_id = {}
    for row in payload["cases"]:
        if not isinstance(row, dict) or set(row) != keys:
            raise ProtocolError("记录字段与协议不符")
        cid = row["id"]
        if not isinstance(cid, str) or cid not in expected_ids or cid in by_id:
            raise ProtocolError("响应 ID 未知或重复")
        if phase == "rewrite":
            if not isinstance(row["text"], str) or not row["text"].strip():
                raise ProtocolError("text 必须包含完整交付内容")
        else:
            if any(row[key] not in values for key, values in DIMENSIONS.items()):
                raise ProtocolError("判分维度取值无效")
            if not isinstance(row["evidence"], str) or not row["evidence"].strip():
                raise ProtocolError("判分必须给出原文与输出的对应依据")
        by_id[cid] = row
    if set(by_id) != set(expected_ids):
        raise ProtocolError("响应未覆盖全部期望 ID")
    return [by_id[cid] for cid in expected_ids]


def summarize_judgments(rows, expected_ids):
    """只从逐条记录计算三维计数；review 不作 pass，质量不作保真判分。"""
    checked = parse_response(json.dumps({"cases": rows}, ensure_ascii=False), "judge", expected_ids)
    result = {"total": len(checked)}
    for dimension, values in DIMENSIONS.items():
        result[dimension] = {value: sum(row[dimension] == value for row in checked) for value in values}
    result["fidelity_fail_ids"] = [row["id"] for row in checked if row["fidelity"] == "fail"]
    result["review_ids"] = [row["id"] for row in checked if any(row[key] == "review" for key in DIMENSIONS)]
    return result
