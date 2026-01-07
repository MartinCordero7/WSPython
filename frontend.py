from html import escape

class Frontend:
    def render(self, items: list[dict]) -> str:
        column_keys = ["id", "fullName", "email", "type", "discount", "totalSale"]
        header_map = {
            "id": "ID",
            "fullName": "Nombre",
            "email": "Email",
            "type": "Tipo",
            "discount": "Descuento",
            "totalSale": "Total Venta",
        }

        def fmt(key: str, value):
            if value is None:
                return ""
            if key == "discount" and isinstance(value, (int, float)):
                pct = value if value > 1 else value * 100
                return f"{pct:.0f}%"
            if key == "totalSale" and isinstance(value, (int, float)):
                return f"${value:,.2f}"
            return escape(str(value))

        thead = "".join(f"<th>{header_map[k]}</th>" for k in column_keys)
        rows = "".join(
            "<tr>"
            + "".join(
                f"<td{' class=\"num\"' if k in ('discount','totalSale') else ''}>{fmt(k, item.get(k))}</td>"
                for k in column_keys
            )
            + "</tr>"
            for item in items
        )
        if not rows:
            rows = f"<tr><td colspan='{len(column_keys)}'>Sin datos</td></tr>"

        return f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <title>Datos de MongoDB</title>
    <style>
      body {{ font-family: Arial, sans-serif; margin: 2rem; }}
      table {{ border-collapse: collapse; width: 100%; }}
      th, td {{ border: 1px solid #ccc; padding: .5rem; text-align: left; }}
      thead {{ background: #f5f5f5; }}
      td.num {{ text-align: right; }}
    </style>
  </head>
  <body>
    <h1>Datos de MongoDB</h1>
    <table>
      <thead><tr>{thead}</tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </body>
</html>"""
