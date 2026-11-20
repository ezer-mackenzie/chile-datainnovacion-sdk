from hypothesis import given
from hypothesis import strategies as st

from chile_datainnovacion_sdk.models import Project

json_values = st.recursive(
    st.none()
    | st.booleans()
    | st.integers()
    | st.floats(allow_nan=False, allow_infinity=False)
    | st.text(),
    lambda children: (
        st.lists(children, max_size=5) | st.dictionaries(st.text(), children, max_size=5)
    ),
    max_leaves=20,
)


@given(value=json_values)
def test_unknown_json_fields_survive_api_mapping(value: object) -> None:
    project = Project.from_api({"codigo": "property-test", "future_api_field": value})

    assert project.code == "property-test"
    assert project.future_api_field == value
