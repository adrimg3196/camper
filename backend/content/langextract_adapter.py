import os
from typing import Any, Dict, List, Optional

try:
    import langextract as lx
except ImportError:
    lx = None


PROMPT_DESCRIPTION = (
    """
    Extrae señales de producto para ecommerce.
    Clases permitidas: brand, product_type, key_feature, use_case, target_user.
    Reglas:
    - Usa texto exacto del input.
    - Mantén el orden de aparición.
    - No inventes marcas o atributos que no estén en el texto.
    """
)


def _build_example() -> Optional["lx.data.ExampleData"]:
    if lx is None:
        return None

    return lx.data.ExampleData(
        text=(
            "Mochila trekking Deuter 65L impermeable con respaldo Aircomfort, "
            "ideal para rutas de montaña de varios días"
        ),
        extractions=[
            lx.data.Extraction(
                extraction_class="brand",
                extraction_text="Deuter",
                attributes={"confidence": "alta"},
            ),
            lx.data.Extraction(
                extraction_class="product_type",
                extraction_text="Mochila trekking",
                attributes={"category": "mochilas"},
            ),
            lx.data.Extraction(
                extraction_class="key_feature",
                extraction_text="65L impermeable",
                attributes={"benefit": "capacidad y protección"},
            ),
            lx.data.Extraction(
                extraction_class="key_feature",
                extraction_text="respaldo Aircomfort",
                attributes={"benefit": "ventilación"},
            ),
            lx.data.Extraction(
                extraction_class="use_case",
                extraction_text="rutas de montaña de varios días",
                attributes={"duration": "multi-day"},
            ),
        ],
    )


def _to_dict(extraction: Any) -> Dict[str, Any]:
    if isinstance(extraction, dict):
        return extraction

    if hasattr(extraction, "model_dump"):
        return extraction.model_dump()

    return {
        "extraction_class": getattr(extraction, "extraction_class", "unknown"),
        "extraction_text": getattr(extraction, "extraction_text", ""),
        "attributes": getattr(extraction, "attributes", {}) or {},
    }


def _build_summary(entities: List[Dict[str, Any]]) -> Dict[str, Any]:
    grouped: Dict[str, List[str]] = {}
    for entity in entities:
        cls = entity.get("class", "unknown")
        text = entity.get("text", "")
        if not text:
            continue
        grouped.setdefault(cls, []).append(text)

    summary_parts = []
    for cls in ["brand", "product_type", "key_feature", "use_case", "target_user"]:
        values = grouped.get(cls, [])
        if values:
            summary_parts.append(f"{cls}: {', '.join(values[:4])}")

    keywords = sorted(
        {
            value.strip().lower()
            for values in grouped.values()
            for value in values
            if isinstance(value, str) and value.strip()
        }
    )

    return {
        "summary": " | ".join(summary_parts),
        "keywords": keywords[:12],
    }


def extract_product_signals(
    product_data: Dict[str, Any],
    model_id: str = "gemini-2.5-flash",
    api_key: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    if lx is None:
        return None

    title = str(product_data.get("title") or "").strip()
    description = str(product_data.get("description") or "").strip()
    category = str(product_data.get("category") or "").strip()

    content = ". ".join(part for part in [title, description, category] if part)
    if not content:
        return None

    examples = [_build_example()]
    examples = [example for example in examples if example is not None]

    effective_api_key = api_key or os.environ.get("LANGEXTRACT_API_KEY") or os.environ.get("GOOGLE_AI_API_KEY")

    kwargs: Dict[str, Any] = {
        "text_or_documents": content,
        "prompt_description": PROMPT_DESCRIPTION,
        "examples": examples,
        "model_id": model_id,
    }

    if effective_api_key:
        kwargs["api_key"] = effective_api_key

    if model_id.startswith("gpt-") or model_id.startswith("o1") or model_id.startswith("o3"):
        kwargs["fence_output"] = True
        kwargs["use_schema_constraints"] = False

    result = lx.extract(**kwargs)

    document = result[0] if isinstance(result, list) and result else result
    raw_extractions = getattr(document, "extractions", []) or []

    entities: List[Dict[str, Any]] = []
    for extraction in raw_extractions:
        item = _to_dict(extraction)
        extraction_class = str(item.get("extraction_class") or "unknown").strip()
        extraction_text = str(item.get("extraction_text") or "").strip()
        attributes = item.get("attributes") if isinstance(item.get("attributes"), dict) else {}

        if extraction_text:
            entities.append(
                {
                    "class": extraction_class,
                    "text": extraction_text,
                    "attributes": attributes,
                }
            )

    summary_data = _build_summary(entities)

    return {
        "entities": entities,
        "summary": summary_data["summary"],
        "keywords": summary_data["keywords"],
    }
