class SQLFilterParser:
    """
    JSON'dan gelen extracted_filters kısmını SQL sorgularına dönüştüren Regex/Parser sınıfı.
    """
    
    def parse_filters(self, extracted_filters: dict) -> tuple[str, list]:
        """
        Gelen filtre dict objesini alır, SQL WHERE cümleciği (string) ve 
        güvenli parametre listesini döner.
        """
        conditions = []
        params = []
        
        # 1. Brand (Marka) Filtresi
        brand = extracted_filters.get("brand")
        if brand and isinstance(brand, str) and brand.strip():
            # Metadata kolonu boş olsa bile başlıkta geçiyorsa kaçırmamak için OR ekliyoruz
            conditions.append("(brand ILIKE %s OR title ILIKE %s)")
            params.extend([f"%{brand.strip()}%", f"%{brand.strip()}%"])
            
        # 2. Color (Renk) Filtresi - Birden fazla olabilir
        colors = extracted_filters.get("color")
        if colors and isinstance(colors, list) and len(colors) > 0:
            color_conds = []
            for color in colors:
                if isinstance(color, str) and color.strip():
                    color_conds.append("(color ILIKE %s OR title ILIKE %s)")
                    params.extend([f"%{color.strip()}%", f"%{color.strip()}%"])
            if color_conds:
                conditions.append(f"({' OR '.join(color_conds)})")
                
        # 3. Kategori Taksonomi ID'leri (Aşama 2'den gelen matched_ids)
        category_taxonomy = extracted_filters.get("category_taxonomy")
        if category_taxonomy and isinstance(category_taxonomy, list) and len(category_taxonomy) > 0:
            # Sadece string veya integer ID'leri kabul et
            valid_ids = [str(cat_id) for cat_id in category_taxonomy if cat_id]
            if valid_ids:
                placeholders = ', '.join(['%s'] * len(valid_ids))
                # Şemaya göre ürünlerde category_id var
                conditions.append(f"category_id IN ({placeholders})")
                params.extend(valid_ids)
                
        # 4. Fiyat (Eğer ürün şemasında fiyat sütunu eklenecekse buraya min/max price eklenebilir)
        # Not: Mevcut şemada price gözükmüyor. Gözükseydi şöyle olurdu:
        # min_price = extracted_filters.get("min_price")
        # if min_price is not None:
        #     conditions.append("price >= %s")
        #     params.append(min_price)
            
        if not conditions:
            # Eğer hiçbir filtre yoksa herkes gelsin
            return "1=1", params
            
        where_clause = " AND ".join(conditions)
        return where_clause, params
