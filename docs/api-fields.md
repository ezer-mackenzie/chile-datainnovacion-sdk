# API fields

The API uses Spanish JSON keys. `DataInnovacionProjectDTO` models that wire
format; the client converts each record to the all-English `Project` model.
Values and source fields are retained as returned by the API.

| API key | `Project` field |
|---|---|
| `codigo` | `code` |
| `foco_apoyo` | `support_focus` |
| `tipo_intervencion` | `intervention_type` |
| `instrumento` | `instrument` |
| `instrumento_homologado` | `homologated_instrument` |
| `estado_data` | `data_status` |
| `tipo_persona_beneficiario` | `beneficiary_person_type` |
| `rut_beneficiario` | `beneficiary_rut` |
| `razon` | `company_name` |
| `titulo_del_proyecto` | `project_title` |
| `objetivo_general_del_proyecto` | `general_objective` |
| `año_adjudicacion` | `award_year` |
| `aprobado_corfo` | `corfo_approved_amount` |
| `aprobado_privado` | `private_approved_amount` |
| `aprobado_privado_pecuniario` | `private_approved_cash_amount` |
| `monto_consolidado_ley` | `consolidated_law_amount` |
| `tipo_innovacion` | `innovation_type` |
| `mercado_objetivo_final` | `target_market` |
| `criterio_mujer` | `women_criterion` |
| `genero_director` | `director_gender` |
| `sostenible` | `sustainable` |
| `ods_principal_sostenible` | `primary_sustainable_development_goal` |
| `meta_principal_cod` | `primary_goal_code` |
| `economia_circular_si_no` | `circular_economy` |
| `modelo_de_circularidad` | `circularity_model` |
| `region_ejecucion` | `execution_region` |
| `tramo_ventas` | `sales_segment` |
| `inicio_actividad` | `activity_start` |
| `sector_economico` | `economic_sector` |
| `patron_principal_asociado` | `primary_associated_pattern` |
| `tipo_proyecto` | `project_type` |
| `r_principal` | `primary_r` |
| `estrategia_r_principal` | `primary_r_strategy` |
| `ley_rep_si_no` | `extended_producer_responsibility_applies` |
| `ley_rep` | `extended_producer_responsibility_law` |
| `ernc` | `non_conventional_renewable_energy` |
| `tendencia_final` | `final_trend` |
| `uso_ia` | `ai_usage` |
| `tech_ia` | `ai_technology` |
| `objetivo_ia` | `ai_objective` |

Unknown fields are preserved in both Pydantic models so API additions do not
silently disappear.

## Filters

| Python keyword | API query parameter | Documented values |
|---|---|---|
| `code` | `filter[codigo]` | A project code |
| `beneficiary_rut` | `filter[rut_beneficiario]` | Beneficiary RUT |
| `intervention_type` | `filter[tipo_intervencion]` | `Ley`, `Subsidio` |
| `data_status` | `filter[estado_data]` | `Vigente`, `Finalizado` |
| `sustainable` | `filter[sostenible]` | `Sí`, `No` |
| `award_year` | `filter[año_adjudicacion]` | A year or comma-separated years |
| `limit` | `limit` | Positive integer |

The API documentation describes the award-year range as 2010–2021. The SDK
passes the requested value to the server and does not silently clamp it.
