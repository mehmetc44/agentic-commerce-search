class SQLFilterParser:
    """
    Gelen filtre dict objesini SQL WHERE cümleciğine dönüştürür.
    Catalog API içinde ürün araması için kullanılır.
    """

    def parse_filters(self, extracted_filters: dict) -> tuple[str, list]:
        """
        Args:
            extracted_filters: brand, color, category_taxonomy, min_price, max_price gibi
                               alanları içerebilecek filtre sözlüğü.
        Returns:
            (where_clause: str, params: list) tuple'ı
        """
        conditions = []
        params = []

        # 1. Brand (Marka) Filtresi
        brand = extracted_filters.get("brand")
        if brand and isinstance(brand, str) and brand.strip():
            conditions.append("(brand ILIKE %s OR title ILIKE %s)")
            params.extend([f"%{brand.strip()}%", f"%{brand.strip()}%"])

        # 2. Color (Renk) Filtresi — birden fazla olabilir
        colors = extracted_filters.get("color")
        if colors and isinstance(colors, list) and len(colors) > 0:
            color_conds = []
            for color in colors:
                if isinstance(color, str) and color.strip():
                    color_conds.append("(color ILIKE %s OR title ILIKE %s)")
                    params.extend([f"%{color.strip()}%", f"%{color.strip()}%"])
            if color_conds:
                conditions.append(f"({' OR '.join(color_conds)})")

        # 3. Kategori ID'leri
        category_taxonomy = extracted_filters.get("category_taxonomy")
        if (
            category_taxonomy
            and isinstance(category_taxonomy, list)
            and len(category_taxonomy) > 0
        ):
            valid_ids = [str(cat_id) for cat_id in category_taxonomy if cat_id]
            if valid_ids:
                placeholders = ", ".join(["%s"] * len(valid_ids))
                conditions.append(f"category_id IN ({placeholders})")
                params.extend(valid_ids)

        # 4. Fiyat Filtresi (şemada price sütunu eklendiğinde aktive edilebilir)
        # min_price = extracted_filters.get("min_price")
        # if min_price is not None:
        #     conditions.append("price >= %s")
        #     params.append(min_price)

        if not conditions:
            return "1=1", params

        where_clause = " AND ".join(conditions)
        return where_clause, params
