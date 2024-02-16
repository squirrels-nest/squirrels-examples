SELECT a.*, {%- if ctx["percent_toggle"] == "Count" %}
                b.num_frauds as group_total_num_frauds
            {%- else %}
                b.percent_frauds as group_avg_percent_frauds
            {%- endif %}
FROM {{ ref("database_view2") }} a
LEFT JOIN {{ ref("database_view1_range") }} b
ON {{ ctx["join_cols"] }}
ORDER BY {{ ctx["order_by_cols"] }}