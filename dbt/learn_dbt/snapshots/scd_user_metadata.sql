{% snapshot scd_user_metadata %}
{{
 config(
 target_schema='gracia10',
 unique_key='user_id',
 strategy='timestamp',
 updated_at='updated_at',
 invalidate_hard_deletes=True
 )
}}
SELECT * FROM {{ source('gracia10', 'metadata') }}
{% endsnapshot %}