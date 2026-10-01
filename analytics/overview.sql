/*
    CommerceIQ
    Overview Analytics

    Purpose:
    Provides the core business metrics used by
    the CommerceIQ executive overview dashboard.
*/


/* ============================================================
   1. OVERVIEW KPIs
   ============================================================ */

SELECT
    COUNT(*) FILTER (
        WHERE is_valid_sale = TRUE
    ) AS valid_sale_rows,

    COUNT(DISTINCT order_id) FILTER (
        WHERE is_valid_sale = TRUE
    ) AS orders,

    SUM(quantity) FILTER (
        WHERE is_valid_sale = TRUE
    ) AS units_sold,

    SUM(revenue) FILTER (
        WHERE is_valid_sale = TRUE
    ) AS gross_sales,

    SUM(revenue) FILTER (
        WHERE is_cancelled = TRUE
    ) AS cancellation_value,

    SUM(revenue) FILTER (
        WHERE is_valid_sale = TRUE
    )
    +
    SUM(revenue) FILTER (
        WHERE is_cancelled = TRUE
    ) AS net_revenue,

    (
        SUM(revenue) FILTER (
            WHERE is_valid_sale = TRUE
        )
        +
        SUM(revenue) FILTER (
            WHERE is_cancelled = TRUE
        )
    )
    /
    NULLIF(
        COUNT(DISTINCT order_id) FILTER (
            WHERE is_valid_sale = TRUE
        ),
        0
    ) AS average_order_value

FROM fact_sales;


/* ============================================================
   2. MONTHLY NET REVENUE TREND
   ============================================================ */

SELECT
    d.year,
    d.month,
    d.month_name,

    SUM(
        CASE
            WHEN f.is_valid_sale = TRUE
            THEN f.revenue
            ELSE 0
        END
    )
    +
    SUM(
        CASE
            WHEN f.is_cancelled = TRUE
            THEN f.revenue
            ELSE 0
        END
    ) AS net_revenue

FROM fact_sales AS f

INNER JOIN dim_date AS d
    ON f.date_key = d.date_key

GROUP BY
    d.year,
    d.month,
    d.month_name

ORDER BY
    d.year,
    d.month;

/* ============================================================
   3. MONTHLY REVENUE GROWTH
   ============================================================ */

WITH monthly_revenue AS (
    SELECT
        d.year,
        d.month,
        d.month_name,

        SUM(
            CASE
                WHEN f.is_valid_sale = TRUE
                THEN f.revenue
                ELSE 0
            END
        )
        +
        SUM(
            CASE
                WHEN f.is_cancelled = TRUE
                THEN f.revenue
                ELSE 0
            END
        ) AS net_revenue

    FROM fact_sales AS f

    INNER JOIN dim_date AS d
        ON f.date_key = d.date_key

    GROUP BY
        d.year,
        d.month,
        d.month_name
)

SELECT
    year,
    month,
    month_name,
    net_revenue,

    LAG(net_revenue) OVER (
        ORDER BY year, month
    ) AS previous_month_revenue,

    (
        (
            net_revenue
            -
            LAG(net_revenue) OVER (
                ORDER BY year, month
            )
        )
        /
        NULLIF(
            LAG(net_revenue) OVER (
                ORDER BY year, month
            ),
            0
        )
    ) * 100 AS revenue_growth_percent

FROM monthly_revenue

ORDER BY
    year,
    month;

/* ============================================================
   4. CUSTOMER OVERVIEW
   ============================================================ */

WITH customer_metrics AS (
    SELECT
        customer_id,

        COUNT(DISTINCT order_id) AS order_count,

        SUM(revenue) AS customer_revenue

    FROM fact_sales

    WHERE
        is_valid_sale = TRUE
        AND customer_id IS NOT NULL

    GROUP BY
        customer_id
)

SELECT
    COUNT(*) AS identified_customers,

    COUNT(*) FILTER (
        WHERE order_count > 1
    ) AS returning_customers,

    (
        COUNT(*) FILTER (
            WHERE order_count > 1
        )::NUMERIC
        /
        NULLIF(COUNT(*), 0)
    ) * 100 AS returning_customer_percent,

    SUM(customer_revenue) AS identified_customer_revenue,

    AVG(customer_revenue) AS average_revenue_per_customer

FROM customer_metrics;