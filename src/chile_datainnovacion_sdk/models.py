from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field


class DataInnovacionProjectDTO(BaseModel):
    """Wire model that mirrors the Spanish JSON keys returned by the API."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    codigo: str | None = None
    foco_apoyo: str | None = None
    tipo_intervencion: str | None = None
    instrumento: str | None = None
    instrumento_homologado: str | None = None
    estado_data: str | None = None
    tipo_persona_beneficiario: str | None = None
    rut_beneficiario: str | None = None
    razon: str | None = None
    titulo_del_proyecto: str | None = None
    objetivo_general_del_proyecto: str | None = None
    ano_adjudicacion: int | str | None = Field(default=None, alias="año_adjudicacion")
    aprobado_corfo: int | float | str | None = None
    aprobado_privado: int | float | str | None = None
    aprobado_privado_pecuniario: int | float | str | None = None
    monto_consolidado_ley: int | float | str | None = None
    tipo_innovacion: str | None = None
    mercado_objetivo_final: str | None = None
    criterio_mujer: str | None = None
    genero_director: str | None = None
    sostenible: str | None = None
    ods_principal_sostenible: str | None = None
    meta_principal_cod: str | None = None
    economia_circular_si_no: str | None = None
    modelo_de_circularidad: str | None = None
    region_ejecucion: str | None = None
    tramo_ventas: str | None = None
    inicio_actividad: str | None = None
    sector_economico: str | None = None
    patron_principal_asociado: str | None = None
    tipo_proyecto: str | None = None
    r_principal: str | None = None
    estrategia_r_principal: str | None = None
    ley_rep_si_no: str | None = None
    ley_rep: str | None = None
    ernc: str | None = None
    tendencia_final: str | None = None
    uso_ia: str | None = None
    tech_ia: str | None = None
    objetivo_ia: str | None = None


API_TO_ENGLISH: dict[str, str] = {
    "codigo": "code",
    "foco_apoyo": "support_focus",
    "tipo_intervencion": "intervention_type",
    "instrumento": "instrument",
    "instrumento_homologado": "homologated_instrument",
    "estado_data": "data_status",
    "tipo_persona_beneficiario": "beneficiary_person_type",
    "rut_beneficiario": "beneficiary_rut",
    "razon": "company_name",
    "titulo_del_proyecto": "project_title",
    "objetivo_general_del_proyecto": "general_objective",
    "año_adjudicacion": "award_year",
    "ano_adjudicacion": "award_year",
    "aprobado_corfo": "corfo_approved_amount",
    "aprobado_privado": "private_approved_amount",
    "aprobado_privado_pecuniario": "private_approved_cash_amount",
    "monto_consolidado_ley": "consolidated_law_amount",
    "tipo_innovacion": "innovation_type",
    "mercado_objetivo_final": "target_market",
    "criterio_mujer": "women_criterion",
    "genero_director": "director_gender",
    "sostenible": "sustainable",
    "ods_principal_sostenible": "primary_sustainable_development_goal",
    "meta_principal_cod": "primary_goal_code",
    "economia_circular_si_no": "circular_economy",
    "modelo_de_circularidad": "circularity_model",
    "region_ejecucion": "execution_region",
    "tramo_ventas": "sales_segment",
    "inicio_actividad": "activity_start",
    "sector_economico": "economic_sector",
    "patron_principal_asociado": "primary_associated_pattern",
    "tipo_proyecto": "project_type",
    "r_principal": "primary_r",
    "estrategia_r_principal": "primary_r_strategy",
    "ley_rep_si_no": "extended_producer_responsibility_applies",
    "ley_rep": "extended_producer_responsibility_law",
    "ernc": "non_conventional_renewable_energy",
    "tendencia_final": "final_trend",
    "uso_ia": "ai_usage",
    "tech_ia": "ai_technology",
    "objetivo_ia": "ai_objective",
}


class Project(BaseModel):
    """Public English project model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    code: str | None = None
    support_focus: str | None = None
    intervention_type: str | None = None
    instrument: str | None = None
    homologated_instrument: str | None = None
    data_status: str | None = None
    beneficiary_person_type: str | None = None
    beneficiary_rut: str | None = None
    company_name: str | None = None
    project_title: str | None = None
    general_objective: str | None = None
    award_year: int | str | None = None
    corfo_approved_amount: int | float | str | None = None
    private_approved_amount: int | float | str | None = None
    private_approved_cash_amount: int | float | str | None = None
    consolidated_law_amount: int | float | str | None = None
    innovation_type: str | None = None
    target_market: str | None = None
    women_criterion: str | None = None
    director_gender: str | None = None
    sustainable: str | None = None
    primary_sustainable_development_goal: str | None = None
    primary_goal_code: str | None = None
    circular_economy: str | None = None
    circularity_model: str | None = None
    execution_region: str | None = None
    sales_segment: str | None = None
    activity_start: str | None = None
    economic_sector: str | None = None
    primary_associated_pattern: str | None = None
    project_type: str | None = None
    primary_r: str | None = None
    primary_r_strategy: str | None = None
    extended_producer_responsibility_applies: str | None = None
    extended_producer_responsibility_law: str | None = None
    non_conventional_renewable_energy: str | None = None
    final_trend: str | None = None
    ai_usage: str | None = None
    ai_technology: str | None = None
    ai_objective: str | None = None

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    @classmethod
    def from_api(cls, payload: dict[str, Any]) -> Self:
        dto = DataInnovacionProjectDTO.model_validate(payload)
        dto_data = dto.model_dump(by_alias=True)
        english_data: dict[str, Any] = {}
        for api_name, value in dto_data.items():
            english_data[API_TO_ENGLISH.get(api_name, api_name)] = value
        return cls.model_validate(english_data)
